title: Top bar and search
summary: One top bar on every page from one navigation source, and one search index over the docs, the services and the map, with a results page on Enter.
order: 65
labels: inside, search, navigation, frontend
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
Every page of the site carries the same top bar: the couch mark and "Machine Behavior" (the home page), the sections Research, Inside, Docs and Map, and the search box. The current section is marked. The bar comes from one source, so a page cannot show a different menu.

## One source for the bar

The sections come from `site/nav.yml`; the HTML is the function `bar()` in `scripts/site_chrome.py`, which writes it between `<!-- mb:bar -->` markers on every page, together with the breadcrumbs and the footer. See [Site navigation and chrome](doc:eng/site-navigation).

```bash
python3 scripts/site_chrome.py           # write the chrome on every page
python3 scripts/site_chrome.py --check   # exit 1 if a page differs from the source
```

The styles are in `/design/chrome.css` and the search script in `/inside/bar.js`. The bar is dark in both colour schemes. Below 820 px the brand and the search box share the first row and the sections move to a second row; the page itself does not scroll sideways.

## Public-demo banner

`banner()` in the same module writes the strip under the bar that says Inside is a public demo and that in production it sits behind single sign-on, with a link to the [Access model](doc:eng/access-model). It is on the app pages of the Inside and Docs sections (`banner: true` in `site/nav.yml`), not on the map.

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

A skip link is the first element of every page. Links, the search box and the suggestions show a visible focus ring.
