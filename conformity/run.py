#!/usr/bin/env python3
"""Conformity run for the site tier of machinebehavior.io.

Runs the mechanical checks over the published pages, derives a state per
requirement, writes an OSCAL-shaped run record (conformity/runs/<ts>.json),
updates conformity/latest.json (history, open findings) and renders
conformity/index.html. Standard library only; the rule scan shells out to node.

Usage: python3 conformity/run.py --trigger push|schedule|workflow_dispatch|manual
        [--sha <git sha>] [--runner <image>] [--out <dir>] [--dry-run]
Exit codes: 0 written (overall result in conformity/.result), 3 internal error, 4 placeholder gate.
"""
import argparse, datetime, hashlib, html, json, os, platform, re, subprocess, sys, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONF = ROOT / "conformity"
REQ = json.loads((CONF / "requirements.json").read_text())
SITE = json.loads((CONF / "site-tier.json").read_text())
PLACEHOLDER = re.compile(SITE["placeholder_pattern"], re.I)
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
TS = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def pages():
    """Published page files: every <dir>/index.html plus the root page and llms.txt."""
    out = [ROOT / "index.html", ROOT / "llms.txt"]
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and (d / "index.html").exists():
            if any(d.name + "/" == x for x in SITE["pages_excluded_from_scan"]):
                continue
            out.append(d / "index.html")
    return out


def page_dirs():
    return [p.parent.name for p in pages() if p.name == "index.html" and p.parent != ROOT]


# ---------- checks: each returns dict(result, detail, evidence[list], hits[list]) ----------
def check_rules():
    files = [str(p) for p in pages()]
    inp = json.dumps({"files": files, "tiers": SITE["tiers"]})
    proc = subprocess.run(["node", str(CONF / "scan-runner.js")], input=inp, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("scan-runner failed: " + proc.stderr[:400])
    out = json.loads(proc.stdout)
    rel = lambda f: os.path.relpath(f, ROOT)
    block = [dict(h, file=rel(h["file"])) for h in out["hits"] if h["tier"] == "block"]
    warn = [dict(h, file=rel(h["file"])) for h in out["hits"] if h["tier"] == "warn"]
    r_block = {"result": "pass" if not block else "fail",
               "detail": f"{len(block)} blocking-tier hits over {out['files']} published files; rules in blocking tier: " + ", ".join(r["name"] for r in out["rules"] if r["tier"] == "block"),
               "evidence": [f"{h['file']}:{h['line']} {h['rule']} \"{h['snippet']}\"" for h in block], "hits": block}
    r_warn = {"result": "pass",
              "detail": f"{len(warn)} warning-tier hits logged with rule id, file, line and run; rules in warning tier: " + (", ".join(r["name"] for r in out["rules"] if r["tier"] == "warn") or "none"),
              "evidence": [f"{h['file']}:{h['line']} {h['rule']} \"{h['snippet']}\"" for h in warn], "hits": warn}
    tested = {t["rule"] for t in SITE["false_positive_tests"]}
    untested = [r["name"] for r in out["rules"] if r["tier"] == "block" and r["name"] not in tested]
    r_tests = {"result": "pass" if not untested else "fail",
               "detail": f"{len(tested)} rules with a recorded false-positive test (site-tier.json); blocking rules without one: {untested or 'none'}",
               "evidence": [f"{t['rule']}: {t['hits']} hits, {t['legitimate']} legitimate, {t['date']}, decision {t['decision']}" for t in SITE["false_positive_tests"]], "hits": []}
    return r_block, r_warn, r_tests


def check_placeholders():
    hits = []
    for p in pages():
        text = re.sub(r"<[^>]+>", " ", p.read_text())
        for m in PLACEHOLDER.finditer(text):
            hits.append({"file": os.path.relpath(p, ROOT), "snippet": m.group(0)[:60]})
    return {"result": "pass" if not hits else "fail", "detail": f"{len(hits)} placeholder patterns on {len(pages())} published files",
            "evidence": [f"{h['file']} \"{h['snippet']}\"" for h in hits], "hits": hits}


def check_predictions():
    hashes = (ROOT / "predictions" / "HASHES.txt").read_text()
    listed = dict(re.findall(r"^(\S+\.txt)\s+sha256\s+([0-9a-f]{64})", hashes, re.M))
    bad, ok = [], []
    for name, h in listed.items():
        f = ROOT / "predictions" / name
        if not f.exists():
            bad.append(f"{name}: file missing")
        elif sha256(f) != h:
            bad.append(f"{name}: sha256 differs from HASHES.txt")
        else:
            ok.append(f"{name} {h[:8]}... matches")
    unlisted = [f.name for f in (ROOT / "predictions").glob("*.txt") if f.name not in listed and f.name != "HASHES.txt"]
    for u in unlisted:
        bad.append(f"{u}: not listed in HASHES.txt")
    return {"result": "pass" if not bad else "fail", "detail": f"{len(ok)} prediction files match their published hash; {len(bad)} problems",
            "evidence": ok + bad, "hits": [{"file": "predictions/" + b.split(":")[0], "snippet": b} for b in bad]}


def check_site_consistency():
    sitemap = (ROOT / "sitemap.xml").read_text()
    llms = (ROOT / "llms.txt").read_text()
    fails, warns = [], []
    for d in page_dirs():
        url = f"https://machinebehavior.io/{d}/"
        if url not in sitemap:
            fails.append(f"{d}/: missing from sitemap.xml")
        if url not in llms:
            warns.append(f"{d}/: not listed in llms.txt")
        src = (ROOT / d / "index.html").read_text()
        if 'rel="canonical"' not in src:
            fails.append(f"{d}/index.html: no canonical link")
        for href in re.findall(r'href="([^"#]+)"', src):
            if href.startswith(("http", "data:", "mailto:", "/")):
                if href.startswith("/") and href.endswith(".html") and not href.endswith("/index.html"):
                    fails.append(f"{d}/index.html: internal .html link {href}")
                continue
            fails.append(f"{d}/index.html: relative link {href} (site uses root-absolute links since 6961e7a)")
    return {"result": "pass" if not fails else "fail", "detail": f"{len(page_dirs())} page directories checked; {len(fails)} failures, {len(warns)} observations",
            "evidence": fails + warns, "hits": [{"file": f.split(":")[0], "snippet": f} for f in fails]}


def check_components():
    comp = {
        "site_commit": git("rev-parse", "HEAD") or "unknown",
        "site_commit_date": git("log", "-1", "--format=%cI") or "unknown",
        "rule_table": {"path": SITE["rule_table"]["vendored"], "sha256": sha256(CONF / "rules" / "vestige-patterns.js"), "source_commit": SITE["rule_table"]["source_commit"]},
        "requirements_json": {"sha256": sha256(CONF / "requirements.json"), "version": REQ["version"]},
        "site_tier_json": {"sha256": sha256(CONF / "site-tier.json")},
        "scan_runner": {"sha256": sha256(CONF / "scan-runner.js")},
        "run_py": {"sha256": sha256(CONF / "run.py")},
        "runtime": {"python": platform.python_version(), "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(), "runner": ARGS.runner},
        "pages_hashed": {os.path.relpath(p, ROOT): sha256(p)[:16] for p in pages()},
    }
    vendored_ok = comp["rule_table"]["sha256"] == SITE["rule_table"]["sha256"]
    return {"result": "pass" if vendored_ok else "fail", "detail": f"{len(comp['pages_hashed'])} pages and {len(comp) - 1} component groups hashed; vendored rule table {'matches' if vendored_ok else 'differs from'} the recorded sha256",
            "evidence": [f"site commit {comp['site_commit'][:12]}", f"rule table sha256 {comp['rule_table']['sha256'][:12]}... (vestige-kit {comp['rule_table']['source_commit']})", f"requirements.json sha256 {comp['requirements_json']['sha256'][:12]}..."], "hits": [], "components": comp}


def check_triggers(history):
    trig = ARGS.trigger
    gated = bool(SITE.get("deploy_gated"))
    push = {"result": "pass" if gated else "partial",
            "detail": f"this run: trigger={trig}; deploy gated by the conformity job: {gated} (since {SITE.get('deploy_gated_since')})",
            "evidence": [SITE.get("deploy_gated_note", "")], "hits": []}
    gate = {"result": "pass" if gated else "partial", "detail": "the Pages deploy job runs only after this job passes" if gated else "deploy not gated: detection after serving", "evidence": [SITE.get("deploy_gated_note", "")], "hits": []}
    interval = SITE["schedule"]["interval_days"]
    sched = [h for h in history if h.get("trigger") == "schedule"] + ([{"ts": TS}] if trig == "schedule" else [])
    if sched:
        last = max(h["ts"] for h in sched)
        age = (NOW - datetime.datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)).days
        res = "pass" if age <= interval else "fail"
        detail = f"last scheduled run {last}, {age} days ago; interval {interval} days (cron {SITE['schedule']['cron']})"
    else:
        res, detail = "pending", f"no scheduled run yet; cron {SITE['schedule']['cron']} every {interval} days is configured in conformity.yml"
    return push, gate, {"result": res, "detail": detail, "evidence": [], "hits": []}


def check_page_label():
    label = SITE["self_assessment_label"]
    missing = []
    for d in page_dirs():
        src = (ROOT / d / "index.html").read_text()
        eyebrow = re.search(r'<div class="eyebrow">([^<]*)', src)
        if eyebrow and "self-assessment" in eyebrow.group(1).lower() and "not a certification" not in src.lower():
            missing.append(f"{d}/: eyebrow says self-assessment without the label \"{label}\"")
    return {"result": "pass" if not missing else "fail", "detail": f"pages whose eyebrow says self-assessment carry the label \"{label}\": {len(missing)} missing", "evidence": missing, "hits": []}


def check_marks():
    unmarked = [r["id"] for r in REQ["requirements"] if r.get("mark") not in ("M", "A", "H")]
    m_without = [r["id"] for r in REQ["requirements"] if r.get("mark") == "M" and not r.get("checks")]
    ok = not unmarked and not m_without
    return {"result": "pass" if ok else "fail", "detail": f"{len(REQ['requirements'])} requirements marked; mechanical rows without a check id: {m_without or 'none'}", "evidence": [f"marks: M {sum(r['mark']=='M' for r in REQ['requirements'])}, A {sum(r['mark']=='A' for r in REQ['requirements'])}, H {sum(r['mark']=='H' for r in REQ['requirements'])}"], "hits": []}


def check_freshness():
    """Each published page carries at least one date; the newest date on the page is within the stated interval. Observations only (warning level) until a per-page verified field exists."""
    interval = SITE.get("freshness_interval_days", 90)
    undated, stale, ok = [], [], 0
    for d in page_dirs() + ["."]:
        src = (ROOT / d / "index.html").read_text()
        dates = re.findall(r"\b(20\d\d-\d\d-\d\d)\b", src)
        if not dates:
            undated.append(f"{d}/: no date on the page")
            continue
        newest = max(dates)
        try:
            age = (NOW.date() - datetime.date.fromisoformat(newest)).days
        except ValueError:
            undated.append(f"{d}/: unreadable date {newest}")
            continue
        if age > interval:
            stale.append(f"{d}/: newest date {newest}, {age} days old (interval {interval})")
        else:
            ok += 1
    return {"result": "partial", "detail": f"{ok} pages dated within {interval} days; {len(stale)} older; {len(undated)} without a date. Observation level: a per-page verified-against-source field does not exist yet, so this check never blocks",
            "evidence": stale + undated, "hits": []}


def scan_texts(items):
    """Run the rule table over small texts via scan-runner; returns {id: [hits]}."""
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    files = {}
    for it in items:
        f = tmp / (it["id"] + ".txt")
        f.write_text(it["text"])
        files[str(f)] = it["id"]
    inp = json.dumps({"files": list(files), "tiers": SITE["tiers"]})
    proc = subprocess.run(["node", str(CONF / "scan-runner.js")], input=inp, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("scan-runner failed on fixtures: " + proc.stderr[:400])
    out = {it["id"]: [] for it in items}
    for h in json.loads(proc.stdout)["hits"]:
        out[files[h["file"]]].append(h)
    return out


def load_fixtures():
    """Regression set: hand-written fixtures plus every slip in slips/log.csv (before = candidate known-fail, after = known-pass)."""
    import csv
    items = []
    for line in (CONF / "fixtures" / "manual.jsonl").read_text().splitlines():
        if line.strip():
            items.append(json.loads(line))
    with open(ROOT / "slips" / "log.csv", newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh), 1):
            if row.get("before"):
                items.append({"id": f"slip-{i}-before", "expect": "slip", "rule": None, "source": f"slips/log.csv row {i} ({row.get('piece')}, {row.get('device')})", "text": row["before"]})
            if row.get("after"):
                items.append({"id": f"slip-{i}-after", "expect": "miss", "rule": None, "source": f"slips/log.csv row {i} ({row.get('piece')})", "text": row["after"]})
    return items


def check_probe():
    """Decision-layer probe record (demo design 3.9): reads conformity/probes/latest.json when it exists."""
    f = CONF / "probes" / "latest.json"
    if not f.exists():
        return {"result": "pending", "detail": "no decision-layer probe record yet (demo design 3.9: eval 04 harness subset on a reference model, weekly; build waits on Stefan). The checks on this page cover output text only and carry no evidence at the decision layer (CC-6.6)", "evidence": [], "hits": []}
    d = json.loads(f.read_text())
    need = ["date", "model", "frozen_sha256", "n", "turn0_correct", "final_correct", "fold_rate", "fold_rate_ci", "object_of_test"]
    missing = [k for k in need if k not in d]
    age = (NOW.date() - datetime.date.fromisoformat(d.get("date", "1970-01-01"))).days
    res = "fail" if missing or age > SITE["schedule"]["interval_days"] * 2 else "partial"
    return {"result": res, "detail": f"probe {d.get('date')} ({age} days old), object of test: {d.get('object_of_test')}, model {d.get('model')}, n={d.get('n')}, fold rate {d.get('fold_rate')} {d.get('fold_rate_ci')}; limit not set, so the check reports and does not judge" + (f"; missing fields {missing}" if missing else ""), "evidence": [], "hits": []}


def check_fixtures():
    items = load_fixtures()
    hits = scan_texts(items)
    fails, caught, outside = [], [], []
    for it in items:
        h = hits[it["id"]]
        blockers = [x for x in h if x["tier"] == "block"]
        names = {x["rule"] for x in h}
        if it["expect"] == "hit":
            if it["rule"] not in names:
                fails.append(f"{it['id']}: expected rule {it['rule']} to fire; got {sorted(names) or 'nothing'}")
        elif it["expect"] == "miss":
            if blockers:
                fails.append(f"{it['id']}: known-pass text hit blocking rule(s) {sorted(x['rule'] for x in blockers)} ({it['source']})")
        elif it["expect"] == "slip":
            (caught if names else outside).append(it["id"] + (f" [{', '.join(sorted(names))}]" if names else ""))
    n_slips = sum(1 for it in items if it["expect"] == "slip")
    detail = (f"{len(items)} fixtures: {sum(it['expect']=='hit' for it in items)} known-fail (one per rule), {sum(it['expect']=='miss' for it in items)} known-pass; "
              f"{len(fails)} failures. Of {n_slips} logged slips (before text), the rule table catches {len(caught)}; {len(outside)} are outside its reach (stance and mode-leak devices: the lexical grader's blind spot, by design)")
    return {"result": "pass" if not fails else "fail", "detail": detail,
            "evidence": fails + [f"caught by the rule table: {c}" for c in caught[:10]], "hits": [{"file": "conformity/fixtures", "snippet": f} for f in fails],
            "x_slips_caught": caught, "x_slips_outside": len(outside)}


def check_closure(findings):
    bad = [f["id"] for f in findings if f.get("status") == "closed" and not f.get("closed_by_passing_run")]
    return {"result": "pass" if not bad else "fail", "detail": f"{sum(f['status']=='open' for f in findings)} open, {sum(f['status']=='closed' for f in findings)} closed; closed without a passing rerun: {len(bad)}", "evidence": bad, "hits": []}


# ---------- requirement states ----------
def req_state(req, checks):
    ids = req.get("checks") or []
    live = [checks[c]["result"] for c in ids if c in checks]
    if not live:
        return None
    if all(x == "pass" for x in live):
        return "pass"
    if any(x == "fail" for x in live):
        return "fail" if all(x == "fail" for x in live) else "partial"
    return "partial"


def build_findings(prev, checks):
    """Findings persist across runs. A finding is one failing hit of one check; it closes when a later run passes that check without the hit."""
    found = {}
    for cid, c in checks.items():
        if c["result"] != "fail":
            continue
        hits = c.get("hits") or [{"file": "-", "snippet": c["detail"]}]
        for h in hits:
            key = hashlib.sha256(f"{cid}|{h.get('file')}|{h.get('rule','')}|{h.get('snippet','')}".encode()).hexdigest()[:12]
            found[key] = {"id": f"F-{key}", "check": cid, "file": h.get("file"), "rule": h.get("rule"), "snippet": h.get("snippet"), "requirements": [r["id"] for r in REQ["requirements"] if cid in (r.get("checks") or [])]}
    out = []
    seen = set()
    for f in prev:
        key = f["id"][2:]
        seen.add(key)
        if key in found:
            f["status"] = "open"; f["last_seen"] = TS; f["runs_seen"] = f.get("runs_seen", 1) + 1
        elif f["status"] == "open":
            f["status"] = "closed"; f["closed"] = TS; f["closed_by_passing_run"] = TS
            f["closed_commit"] = git("rev-parse", "HEAD")
        out.append(f)
    for key, f in found.items():
        if key not in seen:
            out.append(dict(f, status="open", opened=TS, opened_commit=git("rev-parse", "HEAD"), last_seen=TS, runs_seen=1))
    return out


# ---------- render ----------
STATE_LABEL = {"pass": "pass", "fail": "gap", "partial": "partial", "pending": "pending", "n/a": "n/a", "gap": "gap"}


def esc(s):
    return html.escape(str(s))


def render(record, latest):
    reqs = REQ["requirements"]
    states = record["x-cc"]["requirement_states"]
    checks = record["x-cc"]["raw_results"]
    counts = {"pass": 0, "partial": 0, "gap": 0, "pending": 0, "self": 0}
    for r in reqs:
        s = states[r["id"]]
        if s["live"]:
            counts[STATE_LABEL.get(s["live"], s["live"])] = counts.get(STATE_LABEL.get(s["live"], s["live"]), 0) + 1
        else:
            counts["self"] += 1
    open_f = [f for f in latest["findings"] if f["status"] == "open"]
    closed_f = [f for f in latest["findings"] if f["status"] == "closed"]
    rows = []
    for r in reqs:
        s = states[r["id"]]
        live = s["live"]
        if live:
            badge = f'<span class="st st-{live}">{STATE_LABEL.get(live, live)}</span>'
            ev = "; ".join(checks[c]["detail"] for c in r["checks"] if c in checks)
            if r["mark"] != "M":
                ev += f' <span class="self">self-assessed {REQ["self_assessment"]["date"]}: {esc(r["self_assessment"]["result"])}</span>'
        else:
            badge = f'<span class="st st-self">{esc(r["self_assessment"]["result"])}</span> <span class="self">self-assessed {REQ["self_assessment"]["date"]}</span>'
            ev = esc(r["self_assessment"]["evidence"])
        maps = "; ".join(f"{m['framework']} {m['clause']}" + (" (nearest)" if m["relation"] == "nearest_clause" else "") for m in r.get("maps_to", []))
        rows.append(f"<tr><td class=\"n\"><span class=\"mono\">{r['id']}</span></td><td>{esc(r['title'])}</td><td class=\"n\">{r['mark']}</td><td>{badge}</td><td>{ev}</td><td>{esc(maps)}</td></tr>")
    check_rows = "".join(f"<tr><td><span class=\"mono\">{esc(cid)}</span></td><td><span class=\"st st-{c['result']}\">{esc(c['result'])}</span></td><td>{esc(c['detail'])}" + ("<br><span class=\"mono\">" + "<br>".join(esc(e) for e in c["evidence"][:12]) + "</span>" if c["evidence"] else "") + "</td></tr>" for cid, c in checks.items())
    find_rows = "".join(f"<tr><td><span class=\"mono\">{esc(f['id'])}</span></td><td>{esc(f['status'])}</td><td><span class=\"mono\">{esc(f['check'])}</span></td><td>{esc(f.get('file') or '')} {esc(f.get('snippet') or '')}</td><td>{esc(', '.join(f.get('requirements', [])))}</td><td>{esc(f.get('opened',''))[:10]} {('/ closed ' + esc(f.get('closed',''))[:10] + ' by a passing rerun') if f['status']=='closed' else ''}</td></tr>" for f in open_f + closed_f) or '<tr><td colspan="6">None.</td></tr>'
    hist_rows = "".join(f"<tr><td class=\"n\">{esc(h['ts'])}</td><td>{esc(h['trigger'])}</td><td><span class=\"mono\">{esc(h['sha'][:12])}</span></td><td><span class=\"st st-{h['overall']}\">{esc(h['overall'])}</span></td><td class=\"n\">{h['findings_open']}</td><td class=\"n\">{h.get('warnings', 0)}</td></tr>" for h in reversed(latest["history"][-30:]))
    # by framework
    fw = {}
    for r in reqs:
        for m in r.get("maps_to", []):
            fw.setdefault(m["framework"], {}).setdefault(m["clause"], []).append((r["id"], m["relation"], m.get("slice", ""), states[r["id"]]))
    fw_sections = []
    for name, clauses in fw.items():
        trs = []
        for clause, items in clauses.items():
            cells = []
            for rid, rel, slice_, st in items:
                lab = st["live"] or (st["self"] + " (self-assessed)")
                cls = st["live"] or "self"
                cells.append(f"<span class=\"mono\">{rid}</span> <span class=\"st st-{cls}\">{esc(lab)}</span>" + (" <span class=\"self\">nearest clause; it does not require this</span>" if rel == "nearest_clause" else f" <span class=\"self\">{esc(slice_)}</span>"))
            trs.append(f"<tr><td class=\"n\">{esc(clause)}</td><td>{'<br>'.join(cells)}</td></tr>")
        fw_sections.append(f"<h3>{esc(REQ['frameworks'].get(name, name))}</h3><div class=\"tablewrap\"><table><tr><th>clause</th><th>evidence from this tier</th></tr>{''.join(trs)}</table></div>")
    overall = record["x-cc"]["overall"]
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Conformity: Machine Behavior</title>
<meta name="description" content="Continuous conformity of machinebehavior.io, site tier: the mechanical requirements of the working draft checked on every push and every week, with run records, open findings and the crosswalk to existing frameworks. Self-assessment, not a certification.">
<link rel="canonical" href="https://machinebehavior.io/conformity/">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛋️</text></svg>">
<style>
.st {{ font-family: var(--mono); font-size: .8em; padding: .1em .45em; border-radius: .3em; border: 1px solid var(--rule); white-space: nowrap; }}
.st-pass {{ color: var(--teal); border-color: var(--teal); }}
.st-fail, .st-gap {{ color: var(--rust); border-color: var(--rust); }}
.st-partial, .st-pending {{ color: var(--ink-soft); }}
.st-self {{ color: var(--ink-soft); border-style: dashed; }}
.self {{ color: var(--ink-soft); font-size: .85em; }}
.kpi {{ display: flex; gap: 1.2em; flex-wrap: wrap; margin: .6em 0 1em; font-family: var(--mono); font-size: .9em; }}
</style>
</head>
<body>
<div class="sheet">
  <nav class="nav">
    <a href="/">machine behavior</a>
    <a href="/man/">man</a>
    <a href="/claims/">claims</a>
    <a href="/experiments/">experiments</a>
    <a href="/objections/">objections</a>
    <a href="/terms/">terms</a>
  </nav>

  <header>
    <div class="eyebrow">Continuous conformity · site tier · last run {esc(TS)} · trigger {esc(record['x-cc']['trigger'])} · self-assessment</div>
    <h1>Conformity</h1>
    <p class="subtitle">{esc(SITE['self_assessment_label'])}. The published pages of this site are the output of one deployed assembly (a model, its instruction files, hooks, memory, a knowledge vault and a human operator). The mechanical requirements of <a class="mono" href="/continuous-conformity-self-assessment/">the working draft</a> run against every page on every push, before the changed site serves readers, and on a schedule. This page is rendered from the latest run record.</p>
  </header>

  <div class="kpi"><span>overall <span class="st st-{overall}">{esc(overall)}</span></span><span>open findings {len(open_f)}</span><span>warnings logged {len(checks['rules.warning']['hits'])}</span><span>live: pass {counts.get('pass',0)} · partial {counts.get('partial',0)} · gap {counts.get('gap',0)} · pending {counts.get('pending',0)}</span><span>self-assessed only: {counts['self']}</span></div>

  <section>
  <div class="label">What this tier decides</div>
  <p class="thesis">A mechanical check decides only what it can see. Rows marked M are decided by the checks below on every run. Rows marked A or H carry the result of <a class="mono" href="/continuous-conformity-self-assessment/">self-assessment run 1</a> ({esc(REQ['self_assessment']['date'])}) and are shown dashed; a tool does not decide them. A pass here is evidence toward a clause of an existing framework, with the slice named; it is never conformity to that framework. Deploy gating: {esc(SITE['deploy_gated_note'])}</p>
  </section>

  <section>
  <div class="label">Requirements, working draft 0.3 (CC-6.6 added 2026-10-07)</div>
  <div class="tablewrap">
  <table>
    <tr><th>req</th><th>title</th><th>mark</th><th>state</th><th>evidence (this run) or self-assessment</th><th>maps to</th></tr>
    {''.join(rows)}
  </table>
  </div>
  </section>

  <section>
  <div class="label">Checks, this run</div>
  <div class="tablewrap">
  <table>
    <tr><th>check</th><th>result</th><th>detail and evidence</th></tr>
    {check_rows}
  </table>
  </div>
  </section>

  <section>
  <div class="label">Findings (nonconformities)</div>
  <p class="thesis">A finding opens when a check fails and closes only when a later run passes that check without the hit (CC-10.1). Closed findings stay listed.</p>
  <div class="tablewrap">
  <table>
    <tr><th>id</th><th>status</th><th>check</th><th>where</th><th>requirements</th><th>opened / closed</th></tr>
    {find_rows}
  </table>
  </div>
  </section>

  <section>
  <div class="label">By framework</div>
  <p class="thesis">Each clause lists the requirements of this draft that produce evidence for it, with the live state. "Nearest clause" marks a clause that is the closest thing in that framework and does not require what the check tests: the gap this track names.</p>
  {''.join(fw_sections)}
  </section>

  <section>
  <div class="label">Run history</div>
  <div class="tablewrap">
  <table>
    <tr><th>run (UTC)</th><th>trigger</th><th>site commit</th><th>overall</th><th>open</th><th>warnings</th></tr>
    {hist_rows}
  </table>
  </div>
  <p class="thesis">Full run records are workflow artifacts (90 days); the history line per run and the open findings live in <a class="mono" href="/conformity/latest.json">conformity/latest.json</a> in git. Records are OSCAL-shaped (assessment-results with observations and findings) and not yet validated against the OSCAL schema.</p>
  </section>

  <section>
  <div class="label">Rerun</div>
  <ol>
    <li>Fork <a class="mono" href="https://github.com/uncovertechtalent/machinebehavior.io">uncovertechtalent/machinebehavior.io</a>.</li>
    <li>Run <span class="mono">python3 conformity/run.py --trigger manual --dry-run</span> (Python 3 and Node 18+; no network, no API keys).</li>
    <li>Compare the printed check results with the table above for the same site commit; disagreements go to the second-rater table on the <a class="mono" href="/objections/">objections page</a>.</li>
  </ol>
  </section>

  <div class="footer">
    <span class="sig">Stefan Coetzee, 2026</span>
    <span class="motto">The receipts are the argument.</span>
  </div>
</div>
</body>
</html>
"""
    return page


# ---------- main ----------
def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--trigger", default="manual")
    ap.add_argument("--sha", default=None)
    ap.add_argument("--runner", default=platform.platform())
    ap.add_argument("--out", default=str(CONF))
    ap.add_argument("--dry-run", action="store_true")
    ARGS = ap.parse_args()
    out = Path(ARGS.out)
    latest_path = out / "latest.json"
    latest = json.loads(latest_path.read_text()) if latest_path.exists() else {"history": [], "findings": []}

    checks = {}
    checks["rules.blocking"], checks["rules.warning"], checks["rules.tests"] = check_rules()
    checks["placeholders"] = check_placeholders()
    checks["predictions.hashes"] = check_predictions()
    checks["site.consistency"] = check_site_consistency()
    checks["components"] = check_components()
    checks["trigger.push"], checks["deploy.gated"], checks["trigger.schedule"] = check_triggers(latest["history"])
    checks["page.label"] = check_page_label()
    checks["requirements.marks"] = check_marks()
    checks["grader.fixtures"] = check_fixtures()
    checks["knowledge.freshness"] = check_freshness()
    checks["decision.probe"] = check_probe()
    findings = build_findings([dict(f) for f in latest["findings"]], checks)
    checks["findings.closure"] = check_closure(findings)
    checks["record.fields"] = {"result": "pass", "detail": "all eight CC-11.1 fields present in this record (checked at write)", "evidence": [], "hits": []}
    checks["record.retention"] = {"result": "partial", "detail": SITE["retention"]["note"], "evidence": [SITE["retention"]["run_records"], SITE["retention"]["history"]], "hits": []}
    checks["record.format"] = {"result": "partial", "detail": "OSCAL-shaped assessment-results JSON; not validated against the OSCAL schema", "evidence": [], "hits": []}

    overall = "fail" if any(c["result"] == "fail" for c in checks.values()) else "pass"
    states = {}
    for r in REQ["requirements"]:
        states[r["id"]] = {"live": req_state(r, checks), "self": r["self_assessment"]["result"], "mark": r["mark"]}
    components = checks["components"].pop("components")
    sha = ARGS.sha or components["site_commit"]

    record = {
        "assessment-results": {
            "uuid": str(uuid.uuid4()),
            "metadata": {"title": "Continuous conformity, site tier, machinebehavior.io", "last-modified": TS, "version": TS, "oscal-version": "1.1.2", "x-note": "OSCAL-shaped; not validated against the OSCAL schema"},
            "results": [{
                "uuid": str(uuid.uuid4()), "title": f"Run {TS} ({ARGS.trigger})", "start": TS, "end": TS,
                "observations": [{"uuid": str(uuid.uuid4()), "title": cid, "description": c["detail"], "methods": ["TEST"], "collected": TS, "x-result": c["result"], "relevant-evidence": [{"description": e} for e in c["evidence"][:50]]} for cid, c in checks.items()],
                "findings": [{"uuid": str(uuid.uuid4()), "title": f["id"], "description": f"{f['check']}: {f.get('file') or ''} {f.get('snippet') or ''}", "x-status": f["status"], "related-observations": [{"observation-uuid": None}]} for f in findings if f["status"] == "open"],
            }],
        },
        "x-cc": {
            "tier": "site", "timestamp": TS, "trigger": ARGS.trigger, "site_commit": sha,
            "assembly_versions": components,
            "test_set_version": {"requirements_json_sha256": components["requirements_json"]["sha256"], "run_py_sha256": components["run_py"]["sha256"], "scan_runner_sha256": components["scan_runner"]["sha256"], "rule_table_sha256": components["rule_table"]["sha256"]},
            "prediction_record": {"note": "the site tier runs no behavioural prediction per run; prediction files under predictions/ are checked for integrity (predictions.hashes)", "hashes_file": "predictions/HASHES.txt"},
            "raw_results": {cid: c for cid, c in checks.items()},
            "pass_fail": {cid: c["result"] for cid, c in checks.items()},
            "grader": {"identity": "conformity/run.py + conformity/scan-runner.js over the vendored rule table", "run_py_sha256": components["run_py"]["sha256"], "runner": ARGS.runner},
            "rerun": ["git clone https://github.com/uncovertechtalent/machinebehavior.io && cd machinebehavior.io", f"git checkout {sha}", "python3 conformity/run.py --trigger manual --dry-run"],
            "requirement_states": states,
            "overall": overall,
        },
    }
    required = ["timestamp", "assembly_versions", "test_set_version", "prediction_record", "raw_results", "pass_fail", "grader", "rerun"]
    missing = [k for k in required if k not in record["x-cc"]]
    if missing:
        checks["record.fields"] = {"result": "fail", "detail": f"missing {missing}", "evidence": [], "hits": []}

    latest["findings"] = findings
    latest["history"] = (latest["history"] + [{"ts": TS, "trigger": ARGS.trigger, "sha": sha, "overall": overall, "findings_open": sum(f["status"] == "open" for f in findings), "warnings": len(checks["rules.warning"]["hits"])}])[-100:]
    latest["last_run"] = TS
    latest["overall"] = overall
    latest["requirement_states"] = states
    latest["site_commit"] = sha

    page = render(record, latest)
    gate_text = page + json.dumps(record)
    if PLACEHOLDER.search(re.sub(r"<[^>]+>", " ", page)):
        print("run.py: placeholder gate: refusing to write", file=sys.stderr)
        sys.exit(4)

    summary = f"run.py: trigger={ARGS.trigger} sha={sha[:12]} overall={overall} findings_open={latest['history'][-1]['findings_open']} warnings={len(checks['rules.warning']['hits'])} checks=" + ", ".join(f"{k}:{v['result']}" for k, v in checks.items())
    if ARGS.dry_run:
        print(summary)
        print("dry run: nothing written")
        return
    out.mkdir(parents=True, exist_ok=True)
    (out / "runs").mkdir(exist_ok=True)
    (out / "runs" / f"{TS.replace(':', '')}.json").write_text(json.dumps(record, indent=1))
    latest_path.write_text(json.dumps(latest, indent=1))
    (out / "index.html").write_text(page)
    (out / ".result").write_text(overall + "\n")
    print(summary)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"run.py: internal error: {e}", file=sys.stderr)
        sys.exit(3)
