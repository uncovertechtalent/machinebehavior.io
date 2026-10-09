title: Add a page to machinebehavior.io
summary: The five things a new page needs to pass the gate, and the commands to check them before pushing.
order: 40
labels: how-to, pages, gate
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: how-to
---
A new page passes the gate when it has a directory URL, a self canonical, a sitemap entry, an `llms.txt` line and root-absolute links. It joins the navigation with one entry in `site/nav.yml`. Docs pages get all of this from the generator; see [Docs tree](doc:eng/docs-tree).

## Steps

1. Create `<name>/index.html`. The URL is `/<name>/`.
2. In `<head>`, add `<link rel="canonical" href="https://machinebehavior.io/<name>/">` and a meta description.
3. Link only with root-absolute paths: `/man/`, `/style.css`. Relative paths and links ending in `.html` fail the gate.
4. Add `<url><loc>https://machinebehavior.io/<name>/</loc><lastmod>YYYY-MM-DD</lastmod></url>` to `sitemap.xml`.
5. Add a line with the title, URL and a one-line summary to `llms.txt`.
6. Put at least one ISO date on the page; the freshness check reads the newest one.
7. Add the page to its section in `site/nav.yml` and run `python3 scripts/site_chrome.py`. It writes the top bar, the breadcrumbs, the sidebar and the footer, and reports the page as an orphan if the entry is missing.
8. Run the dry run (see [Deploy pipeline](doc:eng/deploy-pipeline)), then pull, commit and push.

## Links built in script

If a page builds links in JavaScript, set `a.href` in code. The gate reads `href="..."` in the page source, and a template string such as an interpolated `href` is read as a relative link. See [Link check flags a template string](doc:eng/runbook-template-href).

## Chrome and layout

Do not write a menu, breadcrumbs or a footer into the page; `scripts/site_chrome.py` writes them between `<!-- mb:NAME -->` markers. A research page links `/style.css` and puts its content in `<div class="sheet">` (reading layout). An Inside page puts its content in `<main>` and keeps its own styles (app layout). A page that needs its breadcrumbs or footer somewhere else holds the empty markers there, for example `<!-- mb:crumbs --><!-- /mb:crumbs -->`. See [Site navigation and chrome](doc:eng/site-navigation).
