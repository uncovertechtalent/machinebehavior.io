#!/usr/bin/env python3
"""Build the experiment 06 link preview (og:image): research/experiments/06-stance-instructions-uncensored/report/preview.png.

usage: python3 scripts/build_exp06_preview.py [--chrome PATH]

The image is a crop of the generated report, nothing drawn by hand: data/scripts/export/report.py builds the
standalone page from the data folder with the site's EB Garamond embedded, a script keeps two parts of it (the title
block and the first four rows of the figure "How often the three builds caved": no instruction, good-chad, slim,
and the full harness), and headless Chrome takes a 1200 x 627 screenshot, the
size LinkedIn and other link previews show. scripts/build_exp06.py points og:image at the file. Needs a local Chrome."""
import argparse, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "research", "experiments", "06-stance-instructions-uncensored")
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "report", "preview.png")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FIGURE = "How often the three builds caved"
W, H = 1200, 627

KEEP = f"""
<style>
.sheet{{max-width:{W}px;padding:30px 64px 0}}
.top{{margin:0 0 22px}}
h1{{font-size:42px;margin-bottom:12px}}
.subtitle{{font-size:22px}}
.ex{{margin:0}}
.src,.note,#tip{{display:none}}
</style>
<script>
(() => {{
  const sheet = document.querySelector('main.sheet');
  const top = document.querySelector('header.top');
  const fig = [...document.querySelectorAll('figure')].find(f => f.textContent.includes({FIGURE!r}));
  if (!sheet || !top || !fig) {{ document.title = 'PREVIEW-MISSING'; return; }}
  fig.querySelectorAll('.hl').forEach((row, i) => {{ if (i > 3) row.remove(); }});  // naked, good-chad, slim, full harness
  fig.querySelectorAll('.key, .lgd').forEach(e => e.remove());
  sheet.replaceChildren(top, fig);
}})();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--chrome", default=os.environ.get("CHROME", CHROME))
    a = ap.parse_args()
    if not shutil.which(a.chrome) and not os.path.exists(a.chrome):
        sys.exit(f"build_exp06_preview: no Chrome at {a.chrome}; pass --chrome")
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "report.html")
        subprocess.run([sys.executable, os.path.join(DATA, "scripts", "export", "report.py"), DATA,
                        "--fonts", os.path.join(ROOT, "fonts"), "--write", page], check=True, stdout=subprocess.DEVNULL)
        html = open(page, encoding="utf-8").read()
        if FIGURE not in html:
            sys.exit(f"build_exp06_preview: the report has no figure {FIGURE!r}; nothing written")
        open(page, "w", encoding="utf-8").write(html.replace("</body>", KEEP + "</body>", 1))
        shot = os.path.join(tmp, "preview.png")
        subprocess.run([a.chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={W},{H}", "--virtual-time-budget=3000", f"--screenshot={shot}", "file://" + page],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        shutil.copyfile(shot, OUT)
    print(f"build_exp06_preview: {os.path.relpath(OUT, ROOT)} ({os.path.getsize(OUT):,} bytes, {W} x {H})")


if __name__ == "__main__":
    main()
