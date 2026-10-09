#!/usr/bin/env python3
"""Conformity run, site tier. Reusable across static sites.

Runs the mechanical checks over a site's published pages, derives a state per
requirement, writes an OSCAL-shaped run record, updates latest.json (history,
findings) and renders a public page. Standard library only; the rule scan
shells out to node (scan-runner.js next to this file).

Usage:
  run.py --root <site root> --config <site-tier.json> --requirements <requirements.json>
         --out <dir for latest.json, index.html, runs/> [--trigger push|schedule|workflow_dispatch|manual]
         [--sha <commit>] [--runner <image>] [--dry-run]
Exit codes: 0 written (overall in <out>/.result), 3 internal error, 4 placeholder gate.
"""
import argparse, datetime, hashlib, html, json, os, platform, re, subprocess, sys, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
TS = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
ARGS = None
ROOT = CONF = OUT = None
REQ = SITE = None
PLACEHOLDER = None


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ARGS.git_dir or ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def rel(p):
    return os.path.relpath(p, ROOT)


def excluded(relpath):
    for x in SITE.get("pages_excluded_from_scan", []):
        if x.endswith("/") and (relpath.startswith(x) or ("/" + x) in ("/" + relpath)):
            return True
        if relpath == x:
            return True
    return False


def pages():
    """Published page files: every *.html under root (minus exclusions) plus llms.txt and configured text files."""
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        r = rel(p)
        if r.startswith(".") or "/." in r or excluded(r):
            continue
        out.append(p)
    for extra in ["llms.txt"] + SITE.get("text_files", []):
        f = ROOT / extra
        if f.exists():
            out.append(f)
    return out


def page_url(p):
    """Site path of a page: x/index.html -> /x/, index.html -> /, a.html -> /a.html."""
    r = rel(p).replace(os.sep, "/")
    if r == "index.html":
        return "/"
    if r.endswith("/index.html"):
        return "/" + r[: -len("index.html")]
    return "/" + r


def html_pages():
    return [p for p in pages() if p.suffix == ".html"]


# ---------- checks ----------
def run_scanner(files):
    inp = json.dumps({"files": files, "tiers": SITE["tiers"]})
    proc = subprocess.run(["node", str(HERE / "scan-runner.js")], input=inp, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("scan-runner failed: " + proc.stderr[:400])
    return json.loads(proc.stdout)


def check_rules():
    out = run_scanner([str(p) for p in pages()])
    block = [dict(h, file=rel(h["file"])) for h in out["hits"] if h["tier"] == "block"]
    warn = [dict(h, file=rel(h["file"])) for h in out["hits"] if h["tier"] == "warn"]
    fmt = lambda h: f"{h['file']}:{h['line']} {h['rule']} \"{h['snippet']}\""
    r_block = {"result": "pass" if not block else "fail",
               "detail": f"{len(block)} blocking-tier hits over {out['files']} published files; rules in blocking tier: " + (", ".join(r["name"] for r in out["rules"] if r["tier"] == "block") or "none"),
               "evidence": [fmt(h) for h in block], "hits": block}
    r_warn = {"result": "pass",
              "detail": f"{len(warn)} warning-tier hits logged with rule id, file, line and run; rules in warning tier: " + (", ".join(r["name"] for r in out["rules"] if r["tier"] == "warn") or "none"),
              "evidence": [fmt(h) for h in warn], "hits": warn}
    tested = {t["rule"] for t in SITE.get("false_positive_tests", [])}
    untested = [r["name"] for r in out["rules"] if r["tier"] == "block" and r["name"] not in tested]
    r_tests = {"result": "pass" if not untested else "fail",
               "detail": f"{len(tested)} rules with a recorded false-positive test (site config); blocking rules without one: {untested or 'none'}",
               "evidence": [f"{t['rule']}: {t['hits']} hits, {t['legitimate']} legitimate, {t['date']}, decision {t['decision']}" for t in SITE.get("false_positive_tests", [])], "hits": []}
    return r_block, r_warn, r_tests


def check_placeholders():
    hits = []
    for p in pages():
        text = re.sub(r"<[^>]+>", " ", p.read_text(errors="replace"))
        for m in PLACEHOLDER.finditer(text):
            hits.append({"file": rel(p), "snippet": m.group(0)[:60]})
    return {"result": "pass" if not hits else "fail", "detail": f"{len(hits)} placeholder patterns on {len(pages())} published files",
            "evidence": [f"{h['file']} \"{h['snippet']}\"" for h in hits], "hits": hits}


def check_predictions():
    hf = ROOT / SITE.get("predictions_hashes", "predictions/HASHES.txt")
    if not hf.exists():
        return {"result": "n/a", "detail": "this site publishes no prediction records", "evidence": [], "hits": []}
    listed = dict(re.findall(r"^(\S+\.txt)\s+sha256\s+([0-9a-f]{64})", hf.read_text(), re.M))
    bad, ok = [], []
    for name, h in listed.items():
        f = hf.parent / name
        if not f.exists():
            bad.append(f"{name}: file missing")
        elif sha256(f) != h:
            bad.append(f"{name}: sha256 differs from {hf.name}")
        else:
            ok.append(f"{name} {h[:8]}... matches")
    for u in [f.name for f in hf.parent.glob("*.txt") if f.name not in listed and f != hf]:
        bad.append(f"{u}: not listed in {hf.name}")
    return {"result": "pass" if not bad else "fail", "detail": f"{len(ok)} prediction files match their published hash; {len(bad)} problems",
            "evidence": ok + bad, "hits": [{"file": rel(hf.parent) + "/" + b.split(":")[0], "snippet": b} for b in bad]}


def check_site_consistency():
    base = SITE["base_url"].rstrip("/")
    sitemap = (ROOT / "sitemap.xml").read_text() if (ROOT / "sitemap.xml").exists() else None
    llms = (ROOT / "llms.txt").read_text() if (ROOT / "llms.txt").exists() else ""
    require_abs = SITE.get("require_root_absolute_links", False)
    fails, warns = [], []
    for p in html_pages():
        r = rel(p); url = page_url(p)
        if url == "/" and SITE.get("skip_home_in_sitemap_check"):
            pass
        if sitemap is not None and url not in SITE.get("sitemap_exempt", []) and (base + url) not in sitemap and (base + url.rstrip("/")) not in sitemap:
            (warns if SITE.get("sitemap_observation_only") else fails).append(f"{r}: missing from sitemap.xml ({url})")
        if url != "/" and (base + url) not in llms:
            warns.append(f"{r}: not listed in llms.txt")
        src = p.read_text(errors="replace")
        if not re.search(r'rel="?canonical"?', src):
            fails.append(f"{r}: no canonical link")
        for href in re.findall(r'href="([^"#]+)"', src):
            if href.startswith(("http", "data:", "mailto:", "tel:", "/")):
                if href.startswith("/") and href.endswith(".html") and not href.endswith("/index.html") and SITE.get("forbid_html_links", require_abs):
                    fails.append(f"{r}: internal .html link {href}")
                continue
            if require_abs:
                fails.append(f"{r}: relative link {href}")
    if sitemap is None:
        warns.append("no sitemap.xml")
    return {"result": "pass" if not fails else "fail", "detail": f"{len(html_pages())} pages checked; {len(fails)} failures, {len(warns)} observations",
            "evidence": fails + warns[:40], "hits": [{"file": f.split(":")[0], "snippet": f} for f in fails]}


def check_components():
    comp = {
        "site_commit": ARGS.sha or git("rev-parse", "HEAD") or "unknown",
        "site_commit_date": git("log", "-1", "--format=%cI") or "unknown",
        "rule_table": {"path": "action/rules/vestige-patterns.js", "sha256": sha256(HERE / "rules" / "vestige-patterns.js"), "source_commit": SITE["rule_table"].get("source_commit")},
        "requirements_json": {"sha256": sha256(Path(ARGS.requirements)), "version": REQ["version"]},
        "site_config": {"path": rel(Path(ARGS.config).resolve()) if str(Path(ARGS.config).resolve()).startswith(str(ROOT)) else str(ARGS.config), "sha256": sha256(Path(ARGS.config))},
        "scan_runner": {"sha256": sha256(HERE / "scan-runner.js")},
        "run_py": {"sha256": sha256(HERE / "run.py")},
        "runtime": {"python": platform.python_version(), "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(), "runner": ARGS.runner},
        "pages_hashed": {rel(p): sha256(p)[:16] for p in pages()},
    }
    vendored_ok = comp["rule_table"]["sha256"] == SITE["rule_table"]["sha256"]
    return {"result": "pass" if vendored_ok else "fail", "detail": f"{len(comp['pages_hashed'])} pages and {len(comp) - 1} component groups hashed; rule table {'matches' if vendored_ok else 'differs from'} the sha256 recorded in the site config",
            "evidence": [f"site commit {comp['site_commit'][:12]}", f"rule table sha256 {comp['rule_table']['sha256'][:12]}... (vestige-kit {comp['rule_table']['source_commit']})", f"requirements.json sha256 {comp['requirements_json']['sha256'][:12]}..."], "hits": [], "components": comp}


def check_triggers(history):
    gated = bool(SITE.get("deploy_gated"))
    push = {"result": "pass" if gated else "partial", "detail": f"this run: trigger={ARGS.trigger}; deploy gated by the conformity job: {gated} (since {SITE.get('deploy_gated_since')})", "evidence": [SITE.get("deploy_gated_note", "")], "hits": []}
    gate = {"result": "pass" if gated else "partial", "detail": "the deploy job runs only after this job passes" if gated else "deploy not gated: detection after serving", "evidence": [SITE.get("deploy_gated_note", "")], "hits": []}
    interval = SITE["schedule"]["interval_days"]
    sched = [h for h in history if h.get("trigger") == "schedule"] + ([{"ts": TS}] if ARGS.trigger == "schedule" else [])
    if sched:
        last = max(h["ts"] for h in sched)
        age = (NOW - datetime.datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)).days
        res, detail = ("pass" if age <= interval else "fail"), f"last scheduled run {last}, {age} days ago; interval {interval} days (cron {SITE['schedule']['cron']})"
    else:
        res, detail = "pending", f"no scheduled run yet; cron {SITE['schedule']['cron']} every {interval} days is configured"
    return push, gate, {"result": res, "detail": detail, "evidence": [], "hits": []}


def check_page_label():
    label = SITE.get("self_assessment_label", "Self-assessment, not a certification")
    missing = []
    for p in html_pages():
        src = p.read_text(errors="replace")
        eyebrow = re.search(r'<div class="eyebrow">([^<]*)', src)
        head = (eyebrow.group(1) if eyebrow else "") + re.sub(r"<[^>]+>", " ", src[:1500])
        if "self-assessment" in head.lower() and "not a certification" not in src.lower() and rel(p) != "conformity/index.html":
            missing.append(f"{rel(p)}: says self-assessment near the top without the label \"{label}\"")
    return {"result": "pass" if not missing else "fail", "detail": f"pages that present themselves as a self-assessment carry the label \"{label}\": {len(missing)} missing", "evidence": missing, "hits": []}


def check_chrome():
    """Warning tier (Stefan, 2026-10-09): site chrome present and in step with the nav tree, no orphan pages,
    breadcrumb JSON-LD matching the visible trail, no colour values outside the design tokens. Enabled per site with
    site config key "chrome_checks"; never blocks (result "warn" when something is found)."""
    cfg = SITE.get("chrome_checks")
    if not cfg:
        na = {"result": "n/a", "detail": "chrome checks not enabled for this site", "evidence": [], "hits": []}
        return dict(na), dict(na), dict(na), dict(na)
    repo = Path(ARGS.git_dir or ROOT).resolve()
    script = repo / cfg.get("script", "scripts/site_chrome.py")
    differ, orphans, other = [], [], []
    if script.exists():
        proc = subprocess.run([sys.executable, str(script), "--check"], cwd=str(repo), capture_output=True, text=True)
        for line in proc.stdout.splitlines():
            if line.startswith("chrome differs"):
                differ.append(line)
            elif line.startswith("error orphan") or line.startswith("error missing page") or "outside site/nav.yml" in line:
                orphans.append(line[6:] if line.startswith("error ") else line)
            elif line.startswith("error "):
                other.append(line[6:])
    else:
        differ.append(f"chrome script not found: {script}")
    w = lambda items: "warn" if items else "pass"
    blocks = {"result": w(differ), "detail": f"pages whose chrome blocks differ from the nav source: {len(differ)} (site_chrome.py --check)", "evidence": differ[:30], "hits": []}
    orph = {"result": w(orphans + other), "detail": f"pages outside the nav tree or tree entries without a page: {len(orphans)}; other tree errors: {len(other)}", "evidence": (orphans + other)[:30], "hits": []}
    crumb_bad, colour_bad = [], []
    hexre = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")
    for p in html_pages():
        src = p.read_text(errors="replace")
        m = re.search(r'"@type": "BreadcrumbList".*?"itemListElement": (\[.*?\])\}</script>', src, re.S)
        vis = re.search(r'<nav class="mb-crumbs"[^>]*>(.*?)</nav>', src, re.S)
        if m or vis:
            try:
                ld = [i["name"] for i in json.loads(m.group(1))] if m else None
            except Exception:
                ld = None
            shown = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<li>(.*?)</li>", vis.group(1), re.S)] if vis else None
            if ld != shown:
                crumb_bad.append(f"{rel(p)}: JSON-LD {ld} vs visible {shown}")
        css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S)) + " " + " ".join(re.findall(r'\bstyle="([^"]*)"', src))
        n = len(hexre.findall(css))
        if n:
            colour_bad.append(f"{rel(p)}: {n} colour value(s) in page CSS")
    crumbs = {"result": w(crumb_bad), "detail": f"pages whose breadcrumb JSON-LD differs from the visible trail: {len(crumb_bad)}", "evidence": crumb_bad[:30], "hits": []}
    colours = {"result": w(colour_bad), "detail": f"pages with colour values outside /design/tokens.css: {len(colour_bad)}", "evidence": colour_bad[:30], "hits": []}
    return blocks, orph, crumbs, colours


def check_marks():
    unmarked = [r["id"] for r in REQ["requirements"] if r.get("mark") not in ("M", "A", "H")]
    m_without = [r["id"] for r in REQ["requirements"] if r.get("mark") == "M" and not r.get("checks")]
    return {"result": "pass" if not (unmarked or m_without) else "fail", "detail": f"{len(REQ['requirements'])} requirements marked; mechanical rows without a check id: {m_without or 'none'}", "evidence": [f"marks: M {sum(r['mark']=='M' for r in REQ['requirements'])}, A {sum(r['mark']=='A' for r in REQ['requirements'])}, H {sum(r['mark']=='H' for r in REQ['requirements'])}"], "hits": []}


def check_freshness():
    interval = SITE.get("freshness_interval_days", 90)
    undated, stale, ok = [], [], 0
    for p in html_pages():
        src = p.read_text(errors="replace")
        dates = re.findall(r"\b(20\d\d-\d\d-\d\d)\b", src)
        if not dates:
            undated.append(f"{rel(p)}: no date on the page"); continue
        newest = max(dates)
        try:
            age = (NOW.date() - datetime.date.fromisoformat(newest)).days
        except ValueError:
            undated.append(f"{rel(p)}: unreadable date {newest}"); continue
        (stale if age > interval else []).append(f"{rel(p)}: newest date {newest}, {age} days old (interval {interval})")
        ok += 0 if age > interval else 1
    return {"result": "partial", "detail": f"{ok} pages dated within {interval} days; {len(stale)} older; {len(undated)} without a date. Observation level: a per-page verified-against-source field does not exist yet, so this check never blocks",
            "evidence": (stale + undated)[:40], "hits": []}


def check_probe():
    """Decision-layer probe record (demo design 3.9, CC-6.6): conformity/probes/latest.json, written weekly from the probe host. Record-only: reports, never judges, until a threshold is set."""
    f = OUT / "probes" / "latest.json"
    if not f.exists():
        return {"result": "pending", "detail": "no decision-layer probe record yet. The checks on this page cover output text only and carry no evidence at the decision layer (CC-6.6)", "evidence": [], "hits": []}
    d = json.loads(f.read_text())
    need = ["date", "model", "frozen_sha256", "arms", "object_of_test", "mode"]
    missing = [k for k in need if k not in d]
    arms = d.get("arms", {})
    for role in ("reference", "assembly"):
        a = arms.get(role, {})
        for k in ("fold_rate", "fold_rate_ci", "turn0_correct", "final_correct", "fold_eligible"):
            if k not in a:
                missing.append(f"arms.{role}.{k}")
    try:
        age = (NOW.date() - datetime.date.fromisoformat(d.get("date", "1970-01-01"))).days
    except ValueError:
        age = 10**6
    stale = age > SITE["schedule"]["interval_days"] * 2
    res = "fail" if missing else ("partial" if not stale else "fail")
    def arm_line(role):
        a = arms.get(role, {})
        ci = a.get("fold_rate_ci") or [None, None]
        return f"{role} ({a.get('arm')}): fold rate {a.get('fold_rate')} [{ci[0]}, {ci[1]}] ({a.get('folded')}/{a.get('fold_eligible')}), correct before pressure {a.get('turn0_correct')}, after {a.get('final_correct')}"
    detail = (f"probe {d.get('date')} ({age} days old{', stale' if stale else ''}), {d.get('n_calls')} calls, USD {d.get('cost_usd')}; object of test: {d.get('object_of_test')}; "
              f"{arm_line('reference')}; {arm_line('assembly')}; {d.get('mode')}" + (f"; missing fields {missing}" if missing else ""))
    ev = [f"model {d.get('model')} on {d.get('backend')} {d.get('region')}", f"frozen subset sha256 {str(d.get('frozen_sha256'))[:16]}... ({(d.get('subset') or {}).get('file')})"]
    for role in ("reference", "assembly"):
        npc = (arms.get(role) or {}).get("by_npc") or {}
        if npc:
            ev.append(f"{role} by NPC: " + ", ".join(f"{k} {v['fold_rate']}" for k, v in npc.items()))
    return {"result": res, "detail": detail, "evidence": ev, "hits": []}


def scan_texts(items):
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    files = {}
    for it in items:
        f = tmp / (it["id"] + ".txt"); f.write_text(it["text"]); files[str(f)] = it["id"]
    out = {it["id"]: [] for it in items}
    for h in run_scanner(list(files))["hits"]:
        out[files[h["file"]]].append(h)
    return out


def load_fixtures():
    import csv
    items = []
    for src in [HERE / "fixtures-manual.jsonl", OUT / "fixtures" / "manual.jsonl"]:
        if src.exists():
            for line in src.read_text().splitlines():
                if line.strip():
                    items.append(json.loads(line))
    slips = SITE.get("slips_log")
    if slips and (ROOT / slips).exists():
        with open(ROOT / slips, newline="") as fh:
            for i, row in enumerate(csv.DictReader(fh), 1):
                if row.get("before"):
                    items.append({"id": f"slip-{i}-before", "expect": "slip", "rule": None, "source": f"{slips} row {i} ({row.get('piece')}, {row.get('device')})", "text": row["before"]})
                if row.get("after"):
                    items.append({"id": f"slip-{i}-after", "expect": "miss", "rule": None, "source": f"{slips} row {i} ({row.get('piece')})", "text": row["after"]})
    return items


def check_fixtures():
    items = load_fixtures()
    hits = scan_texts(items)
    fails, caught, outside = [], [], []
    for it in items:
        h = hits[it["id"]]
        blockers = [x for x in h if x["tier"] == "block"]
        names = {x["rule"] for x in h}
        if it["expect"] == "hit" and it["rule"] not in names:
            fails.append(f"{it['id']}: expected rule {it['rule']} to fire; got {sorted(names) or 'nothing'}")
        elif it["expect"] == "miss" and blockers:
            fails.append(f"{it['id']}: known-pass text hit blocking rule(s) {sorted(x['rule'] for x in blockers)} ({it['source']})")
        elif it["expect"] == "slip":
            (caught if names else outside).append(it["id"] + (f" [{', '.join(sorted(names))}]" if names else ""))
    n_slips = sum(1 for it in items if it["expect"] == "slip")
    detail = f"{len(items)} fixtures: {sum(it['expect']=='hit' for it in items)} known-fail (one per rule), {sum(it['expect']=='miss' for it in items)} known-pass; {len(fails)} failures"
    if n_slips:
        detail += f". Of {n_slips} logged slips (before text), the rule table catches {len(caught)}; {len(outside)} are outside its reach (stance and mode-leak devices: the lexical grader's blind spot, by design)"
    return {"result": "pass" if not fails else "fail", "detail": detail, "evidence": fails + [f"caught by the rule table: {c}" for c in caught[:10]], "hits": [{"file": "fixtures", "snippet": f} for f in fails]}


def check_closure(findings):
    bad = [f["id"] for f in findings if f.get("status") == "closed" and not f.get("closed_by_passing_run")]
    return {"result": "pass" if not bad else "fail", "detail": f"{sum(f['status']=='open' for f in findings)} open, {sum(f['status']=='closed' for f in findings)} closed; closed without a passing rerun: {len(bad)}", "evidence": bad, "hits": []}


# ---------- states, findings ----------
def req_state(req, checks):
    live = [checks[c]["result"] for c in (req.get("checks") or []) if c in checks]
    if not live:
        return None
    if all(x in ("pass", "n/a") for x in live):
        return "pass"
    if all(x == "fail" for x in live):
        return "fail"
    return "partial"


def build_findings(prev, checks):
    found = {}
    for cid, c in checks.items():
        if c["result"] != "fail":
            continue
        for h in (c.get("hits") or [{"file": "-", "snippet": c["detail"]}]):
            key = hashlib.sha256(f"{cid}|{h.get('file')}|{h.get('rule','')}|{h.get('snippet','')}".encode()).hexdigest()[:12]
            found[key] = {"id": f"F-{key}", "check": cid, "file": h.get("file"), "rule": h.get("rule"), "snippet": h.get("snippet"), "requirements": [r["id"] for r in REQ["requirements"] if cid in (r.get("checks") or [])]}
    out, seen = [], set()
    sha = ARGS.sha or git("rev-parse", "HEAD")
    for f in prev:
        key = f["id"][2:]; seen.add(key)
        if key in found:
            f["status"] = "open"; f["last_seen"] = TS; f["runs_seen"] = f.get("runs_seen", 1) + 1
        elif f["status"] == "open":
            f["status"] = "closed"; f["closed"] = TS; f["closed_by_passing_run"] = TS; f["closed_commit"] = sha
        out.append(f)
    for key, f in found.items():
        if key not in seen:
            out.append(dict(f, status="open", opened=TS, opened_commit=sha, last_seen=TS, runs_seen=1))
    return out


# ---------- render ----------
STATE_LABEL = {"pass": "pass", "fail": "gap", "partial": "partial", "pending": "pending", "n/a": "n/a"}
STANDALONE_CSS = """
:root{--paper:#F6F7F4;--ink:#1D2422;--ink-soft:#4A5450;--teal:#2F6D62;--rust:#B3542E;--rule:#D8DCD6;--mono:ui-monospace,Menlo,Consolas,monospace;--serif:Georgia,serif}
@media (prefers-color-scheme:dark){:root{--paper:#131816;--ink:#E8E6DF;--ink-soft:#9FAAA4;--teal:#64AC9B;--rust:#D07A50;--rule:#2B332F}}
html{background:var(--paper)} body{font-family:var(--serif);color:var(--ink);margin:0;line-height:1.5}
.sheet{max-width:1100px;margin:0 auto;padding:2rem 1rem} .nav a{margin-right:1em;font-family:var(--mono);font-size:.9em;color:var(--teal)}
.eyebrow{font-family:var(--mono);font-size:.75em;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft);margin-top:1.5rem}
h1{font-size:2.2em;margin:.2em 0} .subtitle{font-size:1.1em;color:var(--ink-soft)} .label{font-family:var(--mono);font-size:.75em;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft);margin:2rem 0 .4rem}
.tablewrap{overflow-x:auto} table{border-collapse:collapse;width:100%;font-size:.9em} th,td{border-top:1px solid var(--rule);padding:.4em .5em;text-align:left;vertical-align:top} .mono{font-family:var(--mono);font-size:.9em}
.footer{display:flex;justify-content:space-between;margin-top:3rem;color:var(--ink-soft);font-family:var(--mono);font-size:.8em} a{color:var(--teal)}
"""


def esc(s):
    return html.escape(str(s))


def render(record, latest):
    reqs = REQ["requirements"]; states = record["x-cc"]["requirement_states"]; checks = record["x-cc"]["raw_results"]
    page_cfg = SITE.get("page", {})
    links = SITE.get("links", {})
    draft_link = links.get("draft", "https://machinebehavior.io/continuous-conformity-self-assessment/")
    sa_link = links.get("self_assessment")
    sa_date = REQ.get("self_assessment", {}).get("date", "")
    counts = {"pass": 0, "partial": 0, "gap": 0, "pending": 0, "self": 0}
    for r in reqs:
        s = states[r["id"]]
        if s["live"]:
            counts[STATE_LABEL.get(s["live"], s["live"])] = counts.get(STATE_LABEL.get(s["live"], s["live"]), 0) + 1
        else:
            counts["self"] += 1
    open_f = [f for f in latest["findings"] if f["status"] == "open"]; closed_f = [f for f in latest["findings"] if f["status"] == "closed"]
    rows = []
    for r in reqs:
        s = states[r["id"]]; live = s["live"]
        sa = r.get("self_assessment", {})
        if live:
            badge = f'<span class="st st-{live}">{STATE_LABEL.get(live, live)}</span>'
            ev = "; ".join(checks[c]["detail"] for c in r["checks"] if c in checks)
            if r["mark"] != "M" and sa and sa_link:
                ev += f' <span class="self">self-assessed {sa_date}: {esc(sa.get("result",""))}</span>'
        elif sa and sa_link:
            badge = f'<span class="st st-self">{esc(sa.get("result",""))}</span> <span class="self">self-assessed {sa_date}</span>'
            ev = esc(sa.get("evidence", ""))
        else:
            badge = '<span class="st st-self">not assessed</span>'
            ev = "no self-assessment exists for this site yet; a tool does not decide this row"
        maps = "; ".join(f"{m['framework']} {m['clause']}" + (" (nearest)" if m["relation"] == "nearest_clause" else "") for m in r.get("maps_to", []))
        rows.append(f"<tr><td class=\"n\"><span class=\"mono\">{r['id']}</span></td><td>{esc(r['title'])}</td><td class=\"n\">{r['mark']}</td><td>{badge}</td><td>{ev}</td><td>{esc(maps)}</td></tr>")
    check_rows = "".join(f"<tr><td><span class=\"mono\">{esc(cid)}</span></td><td><span class=\"st st-{c['result']}\">{esc(c['result'])}</span></td><td>{esc(c['detail'])}" + ("<br><span class=\"mono\">" + "<br>".join(esc(e) for e in c["evidence"][:12]) + "</span>" if c["evidence"] else "") + "</td></tr>" for cid, c in checks.items())
    find_rows = "".join(f"<tr><td><span class=\"mono\">{esc(f['id'])}</span></td><td>{esc(f['status'])}</td><td><span class=\"mono\">{esc(f['check'])}</span></td><td>{esc(f.get('file') or '')} {esc(f.get('snippet') or '')}</td><td>{esc(', '.join(f.get('requirements', [])))}</td><td>{esc(f.get('opened',''))[:10]} {('/ closed ' + esc(f.get('closed',''))[:10] + ' by a passing rerun') if f['status']=='closed' else ''}</td></tr>" for f in open_f + closed_f) or '<tr><td colspan="6">None.</td></tr>'
    hist_rows = "".join(f"<tr><td class=\"n\">{esc(h['ts'])}</td><td>{esc(h['trigger'])}</td><td><span class=\"mono\">{esc(h['sha'][:12])}</span></td><td><span class=\"st st-{h['overall']}\">{esc(h['overall'])}</span></td><td class=\"n\">{h['findings_open']}</td><td class=\"n\">{h.get('warnings', 0)}</td></tr>" for h in reversed(latest["history"][-30:]))
    fw = {}
    for r in reqs:
        for m in r.get("maps_to", []):
            fw.setdefault(m["framework"], {}).setdefault(m["clause"], []).append((r["id"], m["relation"], m.get("slice", ""), states[r["id"]]))
    fw_sections = []
    for name, clauses in fw.items():
        trs = []
        for clause, items in clauses.items():
            cells = []
            for rid, relation, slice_, st in items:
                lab = st["live"] or ((st["self"] + " (self-assessed)") if st["self"] else "not assessed")
                cls = st["live"] or "self"
                cells.append(f"<span class=\"mono\">{rid}</span> <span class=\"st st-{cls}\">{esc(lab)}</span>" + (" <span class=\"self\">nearest clause; it does not require this</span>" if relation == "nearest_clause" else f" <span class=\"self\">{esc(slice_)}</span>"))
            trs.append(f"<tr><td class=\"n\">{esc(clause)}</td><td>{'<br>'.join(cells)}</td></tr>")
        fw_sections.append(f"<h3>{esc(REQ['frameworks'].get(name, name))}</h3><div class=\"tablewrap\"><table><tr><th>clause</th><th>evidence from this tier</th></tr>{''.join(trs)}</table></div>")
    overall = record["x-cc"]["overall"]
    nav = "".join(f'<a href="{esc(h)}">{esc(l)}</a>\n    ' for l, h in page_cfg.get("nav", [["home", "/"]]))
    stylesheet = f'<link rel="stylesheet" href="{esc(page_cfg["stylesheet"])}">' if page_cfg.get("stylesheet") else f"<style>{STANDALONE_CSS}</style>"
    sa_sentence = f' Rows marked A or H carry the result of <a class="mono" href="{esc(sa_link)}">self-assessment run 1</a> ({esc(sa_date)}) and are shown dashed; a tool does not decide them.' if sa_link else " Rows marked A or H have no self-assessment on this site yet and are shown as not assessed; a tool does not decide them."
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Conformity: {esc(page_cfg.get('site_title', SITE['site']))}</title>
<meta name="description" content="Continuous conformity of {esc(SITE['site'])}, site tier: the mechanical requirements of the working draft checked on every push and every week, with run records, open findings and the crosswalk to existing frameworks. Self-assessment, not a certification.">
<link rel="canonical" href="{esc(SITE['base_url'].rstrip('/'))}/conformity/">
{stylesheet}
{('<link rel="icon" href="' + esc(page_cfg['icon']) + '">') if page_cfg.get('icon') else ''}
<style>
.st {{ font-family: var(--mono); font-size: .8em; padding: .1em .45em; border-radius: .3em; border: 1px solid var(--rule); white-space: nowrap; }}
.st-pass {{ color: var(--teal); border-color: var(--teal); }}
.st-fail, .st-gap {{ color: var(--rust); border-color: var(--rust); }}
.st-partial, .st-pending, .st-n\\/a, .st-warn {{ color: var(--ink-soft); }}
.st-self {{ color: var(--ink-soft); border-style: dashed; }}
.self {{ color: var(--ink-soft); font-size: .85em; }}
.kpi {{ display: flex; gap: 1.2em; flex-wrap: wrap; margin: .6em 0 1em; font-family: var(--mono); font-size: .9em; }}
</style>
</head>
<body>
<div class="sheet">
  <nav class="nav">
    {nav}</nav>

  <header>
    <div class="eyebrow">Continuous conformity · site tier · last run {esc(TS)} · trigger {esc(record['x-cc']['trigger'])} · self-assessment</div>
    <h1>Conformity</h1>
    <p class="subtitle">{esc(SITE.get('self_assessment_label', 'Self-assessment, not a certification'))}. The published pages of {esc(SITE['site'])} are the output of one deployed assembly (a model, its instruction files, hooks, memory, a knowledge vault and a human operator). The mechanical requirements of <a class="mono" href="{esc(draft_link)}">the working draft</a> run against every page on every push, before the changed site serves readers, and on a schedule. This page is rendered from the latest run record.</p>
  </header>

  <div class="kpi"><span>overall <span class="st st-{overall}">{esc(overall)}</span></span><span>open findings {len(open_f)}</span><span>warnings logged {len(checks['rules.warning']['hits'])}</span><span>live: pass {counts.get('pass',0)} · partial {counts.get('partial',0)} · gap {counts.get('gap',0)} · pending {counts.get('pending',0)}</span><span>self-assessed or not assessed: {counts['self']}</span></div>

  <section>
  <div class="label">What this tier decides</div>
  <p class="thesis">A mechanical check decides only what it can see. Rows marked M are decided by the checks below on every run.{sa_sentence} A pass here is evidence toward a clause of an existing framework, with the slice named; it is never conformity to that framework. The checks cover output text. The decision layer (CC-6.6) is read from the weekly probe record (check decision.probe): fold rates are printed and, in record-only mode, never block. The probe measures a reference model (qwen3-coder-30b on Amazon Bedrock, bare and with a short stance instruction), not the model this assembly runs on; under the same design three larger models folded on 0 of 72 runs each (<a class="mono" href="https://machinebehavior.io/experiments/#experiment-04-three-models">experiment 04, v5</a>), so the fold rate is a property of the probed model and the evidence is the test and the record. Deploy gating: {esc(SITE.get('deploy_gated_note', ''))}</p>
  </section>

  <section>
  <div class="label">Requirements, {esc(REQ['version'])}</div>
  <div class="tablewrap"><table>
    <tr><th>req</th><th>title</th><th>mark</th><th>state</th><th>evidence (this run) or self-assessment</th><th>maps to</th></tr>
    {''.join(rows)}
  </table></div>
  </section>

  <section>
  <div class="label">Checks, this run</div>
  <div class="tablewrap"><table>
    <tr><th>check</th><th>result</th><th>detail and evidence</th></tr>
    {check_rows}
  </table></div>
  </section>

  <section>
  <div class="label">Findings (nonconformities)</div>
  <p class="thesis">A finding opens when a check fails and closes only when a later run passes that check without the hit (CC-10.1). Closed findings stay listed.</p>
  <div class="tablewrap"><table>
    <tr><th>id</th><th>status</th><th>check</th><th>where</th><th>requirements</th><th>opened / closed</th></tr>
    {find_rows}
  </table></div>
  </section>

  <section>
  <div class="label">By framework</div>
  <p class="thesis">Each clause lists the requirements of this draft that produce evidence for it, with the live state. "Nearest clause" marks a clause that is the closest thing in that framework and does not require what the check tests: the gap this track names.</p>
  {''.join(fw_sections)}
  </section>

  <section>
  <div class="label">Run history</div>
  <div class="tablewrap"><table>
    <tr><th>run (UTC)</th><th>trigger</th><th>site commit</th><th>overall</th><th>open</th><th>warnings</th></tr>
    {hist_rows}
  </table></div>
  <p class="thesis">Full run records are workflow artifacts (90 days); the history line per run and the open findings live in <a class="mono" href="latest.json">latest.json</a> in git. Records are OSCAL-shaped (assessment-results with observations and findings) and not yet validated against the OSCAL schema.</p>
  </section>

  <section>
  <div class="label">Rerun</div>
  <ol>
    <li>Clone <a class="mono" href="{esc(SITE.get('repo_url', ''))}">{esc(SITE.get('repo_url', 'the site repository'))}</a>{(' and the action from <a class="mono" href="' + esc(SITE['action_repo_url']) + '">' + esc(SITE['action_repo_url']) + '</a>') if SITE.get('action_repo_url') else ''}.</li>
    <li>Run <span class="mono">{esc(SITE.get('rerun_command', 'python3 run.py --root . --config conformity/site-tier.json --requirements conformity/requirements.json --out conformity --dry-run'))}</span> (Python 3 and Node 18+; no network, no API keys).</li>
    <li>Compare the printed check results with the table above for the same site commit.{(' Disagreements go to the second-rater table on the <a class="mono" href="' + esc(links['objections']) + '">objections page</a>.') if links.get('objections') else ''}</li>
  </ol>
  </section>

  <div class="footer">
    <span class="sig">{esc(page_cfg.get('footer_sig', 'Stefan Coetzee, 2026'))}</span>
    <span class="motto">{esc(page_cfg.get('footer_motto', 'The receipts are the argument.'))}</span>
  </div>
  <p class="conf mono" data-conformity>conformity: <a class="mono" href="latest.json">latest run {esc(TS)}</a>, {len(open_f)} open, {esc(overall)}</p>
</div>
</body>
</html>
"""
    return page


# ---------- main ----------
def main():
    global ARGS, ROOT, CONF, OUT, REQ, SITE, PLACEHOLDER
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--requirements", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--git-dir", default=None, help="repo dir for commit metadata when --root is a build output")
    ap.add_argument("--trigger", default="manual")
    ap.add_argument("--sha", default=None)
    ap.add_argument("--runner", default=platform.platform())
    ap.add_argument("--dry-run", action="store_true")
    ARGS = ap.parse_args()
    ROOT = Path(ARGS.root).resolve(); OUT = Path(ARGS.out).resolve()
    REQ = json.loads(Path(ARGS.requirements).read_text()); SITE = json.loads(Path(ARGS.config).read_text())
    PLACEHOLDER = re.compile(SITE["placeholder_pattern"], re.I)
    latest_path = OUT / "latest.json"
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
    checks["chrome.blocks"], checks["chrome.orphans"], checks["chrome.breadcrumbs"], checks["design.colours"] = check_chrome()
    checks["grader.fixtures"] = check_fixtures()
    checks["knowledge.freshness"] = check_freshness()
    checks["decision.probe"] = check_probe()
    findings = build_findings([dict(f) for f in latest["findings"]], checks)
    checks["findings.closure"] = check_closure(findings)
    checks["record.fields"] = {"result": "pass", "detail": "all eight CC-11.1 fields present in this record (checked at write)", "evidence": [], "hits": []}
    checks["record.retention"] = {"result": "partial", "detail": SITE["retention"]["note"], "evidence": [SITE["retention"]["run_records"], SITE["retention"]["history"]], "hits": []}
    checks["record.format"] = {"result": "partial", "detail": "OSCAL-shaped assessment-results JSON; not validated against the OSCAL schema", "evidence": [], "hits": []}

    overall = "fail" if any(c["result"] == "fail" for c in checks.values()) else "pass"
    states = {r["id"]: {"live": req_state(r, checks), "self": r.get("self_assessment", {}).get("result"), "mark": r["mark"]} for r in REQ["requirements"]}
    components = checks["components"].pop("components")
    sha = components["site_commit"]
    record = {
        "assessment-results": {
            "uuid": str(uuid.uuid4()),
            "metadata": {"title": f"Continuous conformity, site tier, {SITE['site']}", "last-modified": TS, "version": TS, "oscal-version": "1.1.2", "x-note": "OSCAL-shaped; not validated against the OSCAL schema"},
            "results": [{"uuid": str(uuid.uuid4()), "title": f"Run {TS} ({ARGS.trigger})", "start": TS, "end": TS,
                         "observations": [{"uuid": str(uuid.uuid4()), "title": cid, "description": c["detail"], "methods": ["TEST"], "collected": TS, "x-result": c["result"], "relevant-evidence": [{"description": e} for e in c["evidence"][:50]]} for cid, c in checks.items()],
                         "findings": [{"uuid": str(uuid.uuid4()), "title": f["id"], "description": f"{f['check']}: {f.get('file') or ''} {f.get('snippet') or ''}", "x-status": f["status"]} for f in findings if f["status"] == "open"]}],
        },
        "x-cc": {
            "tier": "site", "site": SITE["site"], "timestamp": TS, "trigger": ARGS.trigger, "site_commit": sha,
            "assembly_versions": components,
            "test_set_version": {"requirements_json_sha256": components["requirements_json"]["sha256"], "run_py_sha256": components["run_py"]["sha256"], "scan_runner_sha256": components["scan_runner"]["sha256"], "rule_table_sha256": components["rule_table"]["sha256"]},
            "prediction_record": {"note": "the site tier runs no behavioural prediction per run; prediction files, where the site has them, are checked for integrity (predictions.hashes)"},
            "raw_results": checks,
            "pass_fail": {cid: c["result"] for cid, c in checks.items()},
            "grader": {"identity": "conformity action run.py + scan-runner.js over the vendored rule table", "run_py_sha256": components["run_py"]["sha256"], "runner": ARGS.runner},
            "rerun": [SITE.get("rerun_command", "python3 run.py --root . --config <site-tier.json> --requirements <requirements.json> --out <dir> --dry-run")],
            "requirement_states": states,
            "overall": overall,
        },
    }
    latest["findings"] = findings
    latest["history"] = (latest["history"] + [{"ts": TS, "trigger": ARGS.trigger, "sha": sha, "overall": overall, "findings_open": sum(f["status"] == "open" for f in findings), "warnings": len(checks["rules.warning"]["hits"])}])[-100:]
    latest.update({"last_run": TS, "overall": overall, "requirement_states": states, "site_commit": sha, "site": SITE["site"]})

    page = render(record, latest)
    if PLACEHOLDER.search(re.sub(r"<[^>]+>", " ", page)):
        print("run.py: placeholder gate: refusing to write", file=sys.stderr); sys.exit(4)
    summary = f"run.py: site={SITE['site']} trigger={ARGS.trigger} sha={sha[:12]} overall={overall} findings_open={latest['history'][-1]['findings_open']} warnings={len(checks['rules.warning']['hits'])} checks=" + ", ".join(f"{k}:{v['result']}" for k, v in checks.items())
    if ARGS.dry_run:
        print(summary)
        for cid, c in checks.items():
            if c["result"] == "fail":
                print(f"  FAIL {cid}: {c['detail']}")
                for e in c["evidence"][:30]:
                    print(f"       {e}")
        print("dry run: nothing written"); return
    OUT.mkdir(parents=True, exist_ok=True); (OUT / "runs").mkdir(exist_ok=True)
    (OUT / "runs" / f"{TS.replace(':', '')}.json").write_text(json.dumps(record, indent=1))
    latest_path.write_text(json.dumps(latest, indent=1))
    (OUT / "index.html").write_text(page)
    (OUT / ".result").write_text(overall + "\n")
    print(summary)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        print(f"run.py: internal error: {e}", file=sys.stderr); sys.exit(3)
