#!/usr/bin/env python3
"""Tests for the "The law asks, we do" table on /conformity/ (#142), rendered by .github/actions/conformity/run.py.

The gate engine is shared: tychat.io and uncovertechtalent.com run it through a pinned commit, and their requirements
files have no law_asks key. So the cases check the data of this site, and that the key only adds the table and its CSS:
the key adds only the table and its CSS, so a requirements file without it leaves the rest of the page unchanged. Each render
is a real run of run.py into a temporary folder
(Python 3 and Node, no network); nothing in the checkout is written. Stdlib only.

    python3 scripts/test_conformity_law.py

Exits 1 when a case fails.
"""
import importlib.util, json, re, subprocess, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
REPO = Path(__file__).resolve().parent.parent
RUN = REPO / ".github" / "actions" / "conformity" / "run.py"
REQ = json.loads((REPO / "conformity" / "requirements.json").read_text())
FAILS = []


def check(name, cond, detail=""):
    if not cond:
        FAILS.append(f"{name}: {detail}")


def render(requirements, tmp, name):
    """One run of run.py against this checkout, written to tmp/name; returns the page."""
    req, out = Path(tmp) / f"{name}.json", Path(tmp) / name
    req.write_text(json.dumps(requirements, indent=1) + "\n")
    out.mkdir()
    (out / "latest.json").write_text((REPO / "conformity" / "latest.json").read_text())
    r = subprocess.run([sys.executable, str(RUN), "--root", ".", "--config", "conformity/site-tier.json", "--requirements", str(req),
                        "--out", str(out), "--trigger", "manual"], cwd=REPO, capture_output=True, text=True)
    check(f"{name}: run.py exits 0", r.returncode == 0, (r.stderr or r.stdout)[-500:])
    page = out / "index.html"
    return page.read_text() if page.exists() else ""


def masked(page):
    """Run timestamps and the requirements file's own sha256 (components evidence) differ between the two runs by design."""
    page = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", "<ts>", page)
    return re.sub(r"requirements\.json sha256 [0-9a-f]+", "requirements.json sha256 <sha>", page)


# ---- the data: every paraphrase has a crosswalk row, a source, and a read date
law = REQ["law_asks"]
evidence = {(m["framework"], m["clause"]) for r in REQ["requirements"] for m in r.get("maps_to", []) if m["relation"] == "evidence_for"}
keys = [(c["framework"], c["clause"]) for c in law["clauses"]]
check("law_asks: no clause twice", len(keys) == len(set(keys)), str(keys))
for c in law["clauses"]:
    name = f"law_asks {c['framework']} {c['clause']}"
    check(f"{name}: has a crosswalk row with the relation evidence_for", (c["framework"], c["clause"]) in evidence)
    check(f"{name}: names the framework in frameworks", c["framework"] in REQ["frameworks"])
    check(f"{name}: has a source with the article anchor", "{art}" in law["sources"].get(c["framework"], ""))
    check(f"{name}: asks and applies_to are filled", bool(c.get("asks")) and bool(c.get("applies_to")))
    check(f"{name}: read is a date", bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", c.get("read", ""))), c.get("read"))
for fw in ("GDPR Art 32(1)(d)", "NIS2 Art 21(2)(f)", "AIA Art 17(1)(d)"):
    check(f"the testing clause {fw} leads the table", tuple(fw.split(" ", 1)) in keys[:3], str(keys[:3]))

spec = importlib.util.spec_from_file_location("conformity_run", RUN)
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

with tempfile.TemporaryDirectory() as tmp:
    with_law = render(REQ, tmp, "with")
    without = render({k: v for k, v in REQ.items() if k != "law_asks"}, tmp, "without")

    # ---- with the key: one row per clause, the link to the article, the label
    rows = with_law.count('<td data-col="The law asks">')
    check("with law_asks: one row per clause", rows == len(keys), f"{rows} rows, {len(keys)} clauses")
    links = re.findall(r'href="https://eur-lex\.europa\.eu/[^"]*#art_\d+"', with_law)
    check("with law_asks: each row links its article on EUR-Lex", len(links) == len(keys), f"{len(links)} links")
    check("with law_asks: the table carries the label", "Self-assessment, not a certification." in with_law and "a later amendment is not reflected. Rebuilt on every run" in with_law)
    check("with law_asks: the testing clause GDPR Art 32(1)(d) comes first",
          with_law.find("GDPR Art 32(1)(d)</a>") < with_law.find("NIS2 Art 21(2)(f)</a>") < with_law.find("AIA Art 17(1)(d)</a>"))
    check("with law_asks: no nearest_clause row in the table", "nearest clause" not in with_law[with_law.find('<table class="law">'):with_law.find("</table>", with_law.find('<table class="law">'))])

    # ---- without the key (the consumers): no table, no CSS, and the rest of the page unchanged
    check("without law_asks: no table", '<table class="law">' not in without and "The law asks, we do" not in without)
    check("without law_asks: no table CSS", "table.law" not in without)
    start = with_law.find('\n  <section>\n  <div class="label">The law asks, we do')
    end = with_law.find("</section>\n", start) + len("</section>\n")
    stripped = with_law[:start] + with_law[end:] if start >= 0 else with_law
    stripped = stripped.replace(run.LAW_CSS.lstrip(), "", 1)
    check("without law_asks: the page equals the page with the key minus the table and its CSS",
          masked(stripped) == masked(without), "the key changed more of the page than the table and its CSS")

if FAILS:
    print(f"{len(FAILS)} failed:")
    for f in FAILS:
        print("  " + f)
    sys.exit(1)
print(f"ok: {len(keys)} clauses, the table renders with law_asks, and the key adds only the table and its CSS")
