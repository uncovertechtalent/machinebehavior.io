title: Add a page to machinebehavior.io
summary: The five things a new page needs to pass the gate, and the commands to check them before pushing.
order: 40
labels: how-to, pages, gate
---
A new page passes the gate when it has a directory URL, a self canonical, a sitemap entry, an `llms.txt` line and root-absolute links. Docs pages get all five from the generator; see [Docs tree](doc:eng/docs-tree).

## Steps

1. Create `<name>/index.html`. The URL is `/<name>/`.
2. In `<head>`, add `<link rel="canonical" href="https://machinebehavior.io/<name>/">` and a meta description.
3. Link only with root-absolute paths: `/man/`, `/style.css`. Relative paths and links ending in `.html` fail the gate.
4. Add `<url><loc>https://machinebehavior.io/<name>/</loc><lastmod>YYYY-MM-DD</lastmod></url>` to `sitemap.xml`.
5. Add a line with the title, URL and a one-line summary to `llms.txt`.
6. Put at least one ISO date on the page; the freshness check reads the newest one.
7. Run the dry run (see [Deploy pipeline](doc:eng/deploy-pipeline)), then pull, commit and push.

## Links built in script

If a page builds links in JavaScript, set `a.href` in code. The gate reads `href="..."` in the page source, and a template string such as an interpolated `href` is read as a relative link. See [Link check flags a template string](doc:eng/runbook-template-href).

## Inside pages

A page under `/inside/` carries the Inside top bar instead of the site menu. Put the marked block `<!-- inside-bar:begin here=<section> --><!-- inside-bar:end -->` right after `<body>`, link `/inside/bar.css` and `/inside/bar.js`, add the page to `SYNCED` in `scripts/inside_chrome.py` and run it. See [Top bar and search](doc:eng/top-bar-and-search).

## Menu

Every page carries the same menu: machine behavior, man, claims, experiments, objections, terms, inside, infrastructure. Copy it from an existing page. The conformity page builds its menu from the `nav` list in `conformity/site-tier.json`.
