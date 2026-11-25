#!/usr/bin/env python3
"""Build the experiment 06 pages from the chapter drafts and the published data folder.

usage: python3 scripts/build_exp06.py --src DIR [--check]

DIR holds the chapter drafts as Markdown (00 Index.md, 01 The question.md ... 11 Limits.md, Behind the scenes.md). The
script writes, under research/experiments/06-stance-instructions-uncensored/:
  index.html               the title, the lead, At a glance, and the chapter list
  NN-<slug>/index.html     one page per chapter
  behind-the-scenes/       the companion piece
  report/index.html        the report page, from data/scripts/export/report.py --site (built from data/ alone)
Then run scripts/site_chrome.py, which adds the bar, breadcrumbs, sidebar, footer, and structured data.

What it changes in the drafts, and nothing else:
  - the front matter, the drafts' build notes (the index's "Rules for these drafts" and the receipts table of the
    behind-the-scenes piece), and the [C06-xx] claim tags are dropped;
  - each number a claim tag points at becomes a link to that claim's row in claims.json, shown in the ledger at the
    end of the report page; the number is found by the claim's own value in data/claims.json, and a tag whose value
    does not appear as a number in its sentence is listed as a small row id instead, so every tag stays a link;
  - "chapter N" links to chapter N, data file names link to the data folder, arXiv ids and the Heretic repository
    link to their pages;
  - each table gets a caption that states its finding, a source line, and a note (TABLES below).
--check fails when a written page differs from what the drafts would produce. The text itself is never rewritten.
The drafts live outside this repository, so the build and --check run on the author's machine; a later hand edit to
a page shows up as a stale page there. scripts/test_build_exp06.py tests the claim-tag matcher on fixture claims."""
import argparse, html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/research/experiments/06-stance-instructions-uncensored/"
DIR = os.path.join(ROOT, BASE.strip("/"))
DATA = os.path.join(DIR, "data")
SITE = "https://machinebehavior.io"
PUBLISHED = "2026-11-25"
REPORT = BASE + "report/"
SHORT = "Stance under pressure"
OG_IMAGE = SITE + "/map/home-graph.png"
# A file without an extension (SHA256SUMS) gets a trailing slash from the CDN and a 404, so it links to the repository
REPO = "https://github.com/uncovertechtalent/machinebehavior.io/blob/main"

# Each table, in page order per chapter: the caption (its finding, restating numbers on the page) and the note (sample).
TABLES = {
    4: [("With no instruction, the huihui builds and the Gemma Heretic build caved on most of the 15 pressure probes, "
         "and the Heretic Qwen builds held",
         "Battery B pressure probes B1, B6, and B8, five tries each. Wobbles are counted apart from caves.")],
    5: [("On held-out v2, the 92-word good-chad text cut caves from 37 to 11 of 72, and the full harness only to 25",
         "The three ablated builds that cave most, three tries per probe, 72 tries per condition.")],
    7: [("On single pushbacks, both large ablated arms held all 15 pressure probes under either short instruction",
         "Battery B pressure probes B1, B6, and B8, five tries each. The naked runs are from 22 and 23 November, "
         "the instructed runs from 24 November.")],
    8: [("The huihui 9B's caves moved by 3 or less across temperatures 0, 0.3, and 0.7",
         "Held-out v2, three tries per probe, so 24 per cell. At temperature 0 every try repeats the same answer."),
        ("German user turns left the caves within 2 of the English counts on both builds",
         "Held-out v2 at temperature 0.3, three tries per probe, so 24 per cell. The instruction texts stayed in English.")],
}
# Draft-to-page fixes that touch no meaning: a working heading in chapter 2, and chapter 11's count of agreement
# checks, which predates the two benign-label checks (agreement.json holds 18; the kappa range and the six below the
# bar are unchanged).
TEXT_FIXES = [("Sources to cite and spot-check before publishing:", "Sources:"),
              ("We ran 16 agreement checks (`agreement.json`).", "We ran 18 agreement checks (`agreement.json`).")]
LINKS = [(r"arXiv (\d{4}\.\d{4,5})", lambda m: f'<a class="mono" href="https://arxiv.org/abs/{m.group(1)}">arXiv {m.group(1)}</a>'),
         (r"\(p-e-w/heretic\)", lambda m: '(<a class="mono" href="https://github.com/p-e-w/heretic">p-e-w/heretic</a>)')]
NUMWORDS = "one two three four five six seven eight nine ten eleven twelve".split()


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def read_md(path):
    text = open(path, encoding="utf-8").read()
    fm = {}
    if text.startswith("---\n"):
        head, _, text = text[4:].partition("\n---\n")
        for line in head.splitlines():
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"')
    for a, b in TEXT_FIXES:
        text = text.replace(a, b)
    return fm, text.strip("\n")


class Claims:
    def __init__(self):
        self.c = {c["id"]: c for c in json.load(open(os.path.join(DATA, "claims.json")))["claims"]}
        if not all(c["pass"] for c in self.c.values()):
            sys.exit("build_exp06: claims.json has a failing claim; nothing written")
        self.linked, self.listed = [], []

    def values(self, cid):
        """The spellings of a claim's value that may stand in its sentence: the digits, the number word, and for a
        count of none or of every record, the words that say so."""
        c = self.c[cid]
        v, n = c["value"], c["n"]
        if isinstance(v, bool):
            return set()
        if isinstance(v, dict):
            vals = set(v.values())
        elif isinstance(v, float):
            return {f"{round(v * 100)}%"} | ({"all", "every", "each"} if v == 1.0 else set())
        else:
            vals = {v}
        out = set()
        for x in vals:
            out |= {str(x), f"{x:,}"}
            if 1 <= x <= len(NUMWORDS):
                out.add(NUMWORDS[x - 1])
            if x == 1:
                out.add("once")
            if x == 0:
                out |= {"no", "none"}
            if x == n:
                out |= {"all", "every", "each"}
        return out

    def href(self, cid):
        return f"{REPORT}#c-{cid}"

    def title(self, cid):
        return f"claims.json row {cid}: {self.c[cid]['sentence']}"


NUM = re.compile(r"(?<![\w.\-:,])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?%?)(?![\w%]|,\d)|\b(no|none|all|every|each|once|"
                 + "|".join(NUMWORDS) + r")\b", re.I)


def link_claims(text, claims, where):
    """Strip each [C06-xx, ...] tag and turn the number it points at into a marker \x02id\x03number\x04. A tag whose
    value is not a number in the text since the previous tag becomes a marker list \x05ids\x06 at its place."""
    out, last = "", 0
    for m in re.finditer(r"\s*\[(C06-[^\]]+)\]", text):
        seg = text[last:m.start()]
        ids = re.findall(r"C06-\w+", m.group(1))
        unmatched = []
        for cid in ids:
            if cid not in claims.c:
                sys.exit(f"build_exp06: {where}: claim {cid} is not in claims.json")
            want = claims.values(cid)
            hit = None
            for n in reversed(list(NUM.finditer(seg))):
                tok = n.group(0)
                if not n.group(1) and len(ids) > 2:
                    continue  # a long tag list spans a summary sentence: digits only, no number words
                if tok.lower() == "no" and not re.match(r"\s+(caves?|wobbles?|answers?)\b", seg[n.end():]):
                    continue  # "no" counts only as "no cave", "no wobble", "no answer"; "with no instruction" is a condition
                if (tok if n.group(1) else tok.lower()) in want and "\x03" not in seg[max(0, n.start() - 1):n.start()]:
                    hit = n
                    break
            if hit is None:
                unmatched.append(cid)
                continue
            seg = seg[:hit.start()] + f"\x02{cid}\x03{hit.group(0)}\x04" + seg[hit.end():]
            claims.linked.append(cid)
        if unmatched:
            claims.listed.extend(unmatched)
            seg += f"\x05{','.join(unmatched)}\x06"
        out += seg
        last = m.end()
    return out + text[last:]


def inline(text, claims, where, chapter_urls):
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return chr(0xE000 + len(codes) - 1)
    t = re.sub(r"`([^`]+)`", keep, text)
    t = link_claims(t, claims, where)
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    for pat, fn in LINKS:
        t = re.sub(pat, fn, t)

    def chap(m):
        word, n = m.group(1), int(m.group(2))
        if n not in chapter_urls:
            return m.group(0)
        return f'<a href="{chapter_urls[n]}">{word} {n}</a>'
    t = re.sub(r"\b([Cc]hapter) (\d+)\b", chap, t)
    t = re.sub(r"\b([Cc]hapters) (\d+)\b", chap, t)
    t = t.replace("the behind-the-scenes piece", f'<a href="{BASE}behind-the-scenes/">the behind-the-scenes piece</a>')
    t = re.sub(r"\x02([^\x03]+)\x03([^\x04]+)\x04",
               lambda m: f'<a class="cref" href="{claims.href(m.group(1))}" title="{attr(claims.title(m.group(1)))}">{m.group(2)}</a>', t)
    def rows(m):
        ids = m.group(1).split(",")
        nb = "\u2011"  # a non-breaking hyphen keeps a row id on one line; outside the f-string for Python before 3.12
        links = ", ".join(f'<a class="cref" href="{claims.href(c)}" title="{attr(claims.title(c))}">{c.replace("-", nb)}</a>'
                          for c in ids)
        return f" ({'row' if len(ids) == 1 else 'rows'} {links})"
    t = re.sub(r"\x05([^\x06]+)\x06", rows, t)

    def code(m):
        s = codes[ord(m.group(0)) - 0xE000]
        if os.path.isfile(os.path.join(DATA, s)):
            return f'<a class="mono" href="{BASE}data/{s}">{esc(s)}</a>'
        return f'<span class="mono">{esc(s)}</span>'
    return re.sub("[-]", code, t)


def blocks(md):
    """Split Markdown into (kind, lines) blocks: h1, h2, table, list, para."""
    out, cur, kind = [], [], None
    def flush():
        nonlocal cur, kind
        if cur:
            out.append((kind, cur))
        cur, kind = [], None
    for line in md.splitlines():
        if not line.strip():
            flush(); continue
        k = ("h1" if line.startswith("# ") else "h2" if line.startswith("## ") else "table" if line.startswith("|")
             else "list" if re.match(r"\s*(- |\d+\. )", line) else "para")
        if k in ("h1", "h2"):
            flush(); out.append((k, [line])); continue
        if k != kind:
            flush(); kind = k
        cur.append(line)
    flush()
    return out


def render_list(lines, il):
    items = []  # (indent, ordered, text)
    for line in lines:
        m = re.match(r"(\s*)(- |\d+\. )(.*)", line)
        items.append((len(m.group(1)), m.group(2) != "- ", m.group(3)))

    def walk(i, depth):
        tag = "ol" if items[i][1] else "ul"
        h = f"<{tag}>"
        while i < len(items) and items[i][0] >= depth:
            ind, _, text = items[i]
            if ind > depth:
                sub, i = walk(i, ind)
                h = h[:-5] + sub + "</li>"
                continue
            h += f"<li>{il(text)}</li>"
            i += 1
        return h + f"</{tag}>", i
    h, _ = walk(0, items[0][0])
    return h


def render_table(lines, il, n, tid, caption, note):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    head, body = rows[0], [r for r in rows[2:]]
    h = f'<table id="{tid}"><caption>{esc(caption)}</caption>\n    <thead><tr>' + "".join(f"<th>{il(c)}</th>" for c in head) + "</tr></thead>\n    <tbody>\n"
    h += "".join("      <tr>" + "".join(f"<td>{il(c)}</td>" for c in r) + "</tr>\n" for r in body)
    h += "    </tbody>\n  </table>\n"
    h += (f'<p class="exhibit-source">Source: <a class="mono" href="{BASE}data/claims.json">claims.json</a> and '
          f'<a class="mono" href="{BASE}data/records.jsonl">records.jsonl</a> in the '
          f'<a href="{BASE}data/README.md">data folder</a>; each count links to its row in claims.json.</p>\n')
    h += f'<p class="exhibit-note">Note: {esc(note)}</p>'
    return h


def body_html(bl, il, chapter):
    parts, t = [], 0
    for kind, lines in bl:
        if kind == "h2":
            text = lines[0][3:].strip()
            parts.append(f'<h2 id="{slug(text)}">{il(text)}</h2>')
        elif kind == "para":
            parts.append(f'<p class="thesis">{il(" ".join(lines))}</p>')
        elif kind == "list":
            parts.append(render_list(lines, il))
        elif kind == "table":
            cap, note = TABLES[chapter][t]
            parts.append(render_table(lines, il, t, f"ex-ch{chapter:02d}-{t + 1}", cap, note))
            t += 1
    if chapter in TABLES and t != len(TABLES[chapter]):
        sys.exit(f"build_exp06: chapter {chapter} has {t} tables, TABLES has {len(TABLES[chapter])}")
    return "\n\n  ".join(parts)


def plain(s):
    s = re.sub(r"\s*\[C06-[^\]]+\]", "", s)
    s = s.replace("**", "").replace("`", "")
    return s.strip()


def sentences(s):
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z])", s.strip()) if x]


def page(title, desc, url, eyebrow, h1, subtitle, glance, body, extra_head=""):
    canon = SITE + url
    sub = f'\n    <p class="subtitle">{subtitle}</p>' if subtitle else ""
    gl = ""
    if glance:
        gl = ('\n  <section class="glance" aria-labelledby="at-a-glance">\n    <h2 id="at-a-glance">At a glance</h2>\n    <ul>\n'
              + "".join(f"      <li>{g}</li>\n" for g in glance) + "    </ul>\n  </section>\n")
    return f"""<!doctype html>
<html lang="en" data-mb-theme="paper">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}: Machine Behavior</title>
<meta name="description" content="{attr(desc)}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛋️</text></svg>">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="Machine Behavior">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1640">
<meta property="og:image:height" content="820">
<meta property="og:image:alt" content="Second brain: a graph of Stefan Coetzee's published pages, posts, repos and threads.">
<meta property="article:published_time" content="{PUBLISHED}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">{extra_head}
</head>
<body>
<div class="sheet">

  <header>
    <span class="kind">Experiment</span>
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>{sub}
  </header>{gl}

  {body}

</div>
</body>
</html>
"""


def dataset_ld(desc):
    files = [("records.jsonl", "application/jsonl"), ("labels.jsonl", "application/jsonl"), ("claims.json", "application/json"),
             ("croissant.json", "application/ld+json"), ("SHA256SUMS", "text/plain")]
    d = {"@context": "https://schema.org", "@type": "Dataset", "@id": SITE + BASE + "#dataset",
         "name": "Experiment 06: stance under pressure on uncensored language models", "description": desc,
         "url": SITE + BASE, "creator": {"@id": SITE + "/#stefan"}, "datePublished": PUBLISHED,
         "license": "https://creativecommons.org/licenses/by/4.0/", "isAccessibleForFree": True,
         "keywords": ["sycophancy", "abliteration", "uncensored models", "stance", "system prompt", "LLM evaluation"],
         "distribution": [{"@type": "DataDownload", "contentUrl": SITE + BASE + "data/" + f, "encodingFormat": t} for f, t in files]}
    return '\n<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"


def build(src):
    claims = Claims()
    files = sorted(f for f in os.listdir(src) if f.endswith(".md"))
    chapters = {}
    for f in files:
        m = re.match(r"(\d\d) (.+)\.md$", f)
        if m and m.group(1) != "00":
            n = int(m.group(1))
            chapters[n] = {"file": f, "name": m.group(2), "url": f"{BASE}{m.group(1)}-{slug(m.group(2))}/"}
    if sorted(chapters) != list(range(1, 12)) or "00 Index.md" not in files or "Behind the scenes.md" not in files:
        sys.exit("build_exp06: --src must hold 00 Index.md, chapters 01 to 11, and Behind the scenes.md")
    curls = {n: c["url"] for n, c in chapters.items()}
    pages = {}

    # chapters
    for n, c in chapters.items():
        fm, md = read_md(os.path.join(src, c["file"]))
        bl = blocks(md)
        if bl[0][0] != "h1" or bl[1][0] != "para":
            sys.exit(f"build_exp06: {c['file']} does not open with a title and a lead paragraph")
        title = bl[0][1][0][2:].strip()
        c["title"] = title
        il = lambda s, w=c["file"]: inline(s, claims, w, curls)
        lead = " ".join(bl[1][1])
        c["lead"] = plain(lead)
        glance = [f"<em>{il(s.replace('**', ''))}</em>" for s in sentences(lead.replace("**", ""))]
        nav = []
        if n > 1:
            nav.append(f'Previous: <a href="{chapters[n - 1]["url"]}">chapter {n - 1}</a>')
        if n < 11:
            nav.append(f'Next: <a href="{chapters[n + 1]["url"]}">chapter {n + 1}</a>')
        nav.append(f'<a href="{BASE}">All chapters</a>')
        tail = (f'<aside class="sidebar">How to read the numbers: each underlined number links to its row in '
                f'<a class="mono" href="{BASE}data/claims.json">claims.json</a>, shown in the ledger at the end of the '
                f'<a href="{REPORT}">report page</a>. Every row is recomputed from the published data on each build.</aside>'
                f'\n\n  <p class="thesis">{" · ".join(nav)}</p>')
        body = body_html(bl[2:], il, n) + "\n\n  " + tail
        desc = f"Experiment 06, chapter {n}: {c['lead']}"
        pages[c["url"]] = page(f"{title}: experiment 06, chapter {n}", desc, c["url"],
                               f"Experiment 06 · chapter {n} of 11 · {PUBLISHED}", esc(title), "", glance, body)

    # behind the scenes
    fm, md = read_md(os.path.join(src, "Behind the scenes.md"))
    md = re.split(r"\n## Receipts \(for the build", md)[0]
    bl = blocks(md)
    il = lambda s: inline(s, claims, "Behind the scenes.md", curls)
    title = bl[0][1][0][2:].strip()
    lead = " ".join(bl[1][1])
    bts_url = BASE + "behind-the-scenes/"
    glance = [f"<em>{il(s)}</em>" for s in sentences(lead.replace("**", ""))]
    body = body_html(bl[2:], il, 0) + f'\n\n  <p class="thesis"><a href="{BASE}">All chapters</a> · <a href="{REPORT}">The report page</a></p>'
    pages[bts_url] = page(title, "Experiment 06, behind the scenes: " + plain(lead), bts_url,
                          f"Experiment 06 · behind the scenes · {PUBLISHED}", esc(title), "", glance, body)

    # index
    fm, md = read_md(os.path.join(src, "00 Index.md"))
    md = md.split("\nRules for these drafts:")[0]
    bl = blocks(md)
    il = lambda s: inline(s, claims, "00 Index.md", curls)
    h1 = bl[0][1][0][2:].strip()
    lead = " ".join(bl[1][1])
    rest = [b for b in bl[2:] if not (b[0] == "list" and "[[" in b[1][0])]
    glance = [f"<em>{esc(chapters[n]['lead'])}</em> (<a href=\"{chapters[n]['url']}\">chapter {n}</a>)" for n in range(4, 11)]
    toc = "".join(f'<li><a href="{c["url"]}">{esc(c["title"])}</a></li>' for n, c in sorted(chapters.items()))
    body = (body_html(rest, il, 0)
            + f'\n\n  <h2 id="chapters">Chapters</h2>\n  <ol>{toc}</ol>\n  <p class="thesis">With a companion piece: '
            f'<a href="{bts_url}">behind the scenes</a>, how the research ran.</p>'
            f'\n\n  <h2 id="report-and-data">Report and data</h2>\n  <p class="thesis">The <a href="{REPORT}">report page</a> draws every '
            f'conversation as a square and ends with the ledger of every checked number. The <a href="{BASE}data/README.md">data folder</a> '
            f'holds every conversation (<a class="mono" href="{BASE}data/records.jsonl">records.jsonl</a>), every label '
            f'(<a class="mono" href="{BASE}data/labels.jsonl">labels.jsonl</a>), every number with the records behind it '
            f'(<a class="mono" href="{BASE}data/claims.json">claims.json</a>), the instruction texts, the model pins, the scripts, '
            f'Croissant metadata (<a class="mono" href="{BASE}data/croissant.json">croissant.json</a>), and '
            f'<a class="mono" href="{REPO}{BASE}data/SHA256SUMS">SHA256SUMS</a>. Data under CC BY 4.0, scripts under MIT; the '
            f'README has the licence lines and the model-output notice.</p>')
    idx_desc = (f"{h1} {plain(lead)} Experiment 06 on machinebehavior.io: eleven chapters, a report page, and the data, "
                "with every number recomputed from the published records.")
    pages[BASE] = page(f"{SHORT}: experiment 06", idx_desc, BASE, f"Experiment 06 · eleven chapters, a report, and the data · {PUBLISHED}",
                       esc(h1), il(plain(lead)), glance, body, dataset_ld(idx_desc))

    # report, from the data folder alone
    rep = os.path.join(DIR, "report", "index.html")
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    return pages, claims, rep


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--src", required=True); ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    pages, claims, rep = build(os.path.expanduser(a.src))
    stale = []
    for url, h in pages.items():
        p = os.path.join(ROOT, url.strip("/"), "index.html")
        if a.check:
            if not os.path.exists(p) or _strip_chrome(open(p, encoding="utf-8").read()) != _strip_chrome(h):
                stale.append(url)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(h)
    if not a.check:
        subprocess.run([sys.executable, os.path.join(DATA, "scripts", "export", "report.py"), DATA, "--site", SITE + REPORT,
                        "--write", rep], check=True)
    if stale:
        sys.exit("build_exp06: stale pages: " + " ".join(stale))
    print(f"build_exp06: {len(pages)} pages{' checked' if a.check else ' written'} and the report page; "
          f"{len(claims.linked)} claim tags linked to their number, {len(claims.listed)} listed as row ids "
          f"({' '.join(claims.listed)})")


def _strip_chrome(s):
    s = re.sub(r"<!-- mb:(\w+) -->.*?<!-- /mb:\1 -->\n?", "", s, flags=re.S)
    s = re.sub(r'<span class="exhibit-n">Table \d+</span> ', "", s)
    s = re.sub(r'<body[^>]*>', "<body>", s).replace(' id="main" role="main"', "")
    return re.sub(r"\s+", " ", s)


if __name__ == "__main__":
    main()
