title: Top bar and search
summary: One top bar on every Inside page from one Python source, and one search index over the docs, the services and the map, with a results page on Enter.
order: 65
labels: inside, search, navigation, frontend
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
Every Inside page carries the same top bar: Inside, Docs, Services, Status, Board, Map, Infrastructure, Gate and a link to the site. The bar and its search box come from one source, so a page cannot show a different menu.

## One source for the bar

The HTML of the bar is the function `bar()` in `scripts/inside_chrome.py`. Nothing else writes it.

| Page | How it gets the bar |
|---|---|
| Docs pages | `scripts/build_docs.py` calls `bar('docs')` for every page it writes |
| Pages built from YAML (services, status) | `scripts/build_inside.py` calls `bar()` |
| Hand-written pages: Inside, the board, the search page, the map | A marked block, `<!-- inside-bar:begin here=board --><!-- inside-bar:end -->`, that `scripts/inside_chrome.py` rewrites |

`here` names the section shown as current. A section whose page does not exist yet stays out of the bar until the page ships.

```bash
python3 scripts/inside_chrome.py           # rewrite the marked blocks
python3 scripts/inside_chrome.py --check   # exit 1 if a page differs from the source, or lacks the block or assets
```

The styles are in `/inside/bar.css` and the search script in `/inside/bar.js`. Class names start with `ib-`, so the bar does not collide with page styles. Below 820 px the sections move to a second row that scrolls sideways inside the bar; the page itself does not scroll sideways.

## One search index

`scripts/build_search.py` writes `/inside/search.json` from three sources:

- the docs pages, from `inside/docs/search.json`;
- the services, from `inside/services/services.json`;
- every other node of the [map](/map/): pages on the three sites, Substack posts, repositories and threads.

The deploy job runs the script again after it refreshes the map, so the deployed index matches the deployed graph. The rebuilt file is never committed. See [Deploy pipeline](doc:eng/deploy-pipeline).

## Search behaviour

- The search box is a form that submits to [/inside/search/](/inside/search/). Enter always opens the results page; it never opens the first hit. Without JavaScript the form still submits.
- While typing, up to eight suggestions appear under the box. Arrow down moves focus into them, Enter follows the focused link, Escape returns to the box.
- `/` focuses the box from anywhere on the page.
- Ranking: a title that starts with the term, then a whole word in the title, then a part of a word in the title, then labels, the summary and the page text. Every term must match. Services and pages on this site get a small boost.
- The results page filters by kind: docs, services, machinebehavior.io, the other two sites, Substack, GitHub and Reddit.
- Docs labels link to the results page for that label.

## Keyboard and focus

A skip link is the first element of the bar. Links, the search box and the suggestions show a visible focus ring.
