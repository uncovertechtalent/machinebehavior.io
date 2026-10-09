title: Map crawler
summary: scripts/crawl_map.py crawls the three sites and Substack into map/graph.json, splitting body links from navigation and keeping a node per page, post, repo, thread and tag.
order: 50
labels: map, crawler, graph
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
`scripts/crawl_map.py` builds `map/graph.json`, the data behind the [map of the work](/map/) and the front page of [Inside](/inside/). It runs in the deploy job on every push and on the Monday schedule, and by hand.

```bash
python3 scripts/crawl_map.py map/graph.json
```

## What it crawls

1. Every URL in the `sitemap.xml` of machinebehavior.io, tychat.io and uncovertechtalent.com.
2. Substack posts from the archive API; the RSS feed if the API fails; the posts in the previous snapshot if both fail.
3. Each page once. Links to GitHub repositories and Reddit threads become nodes without being fetched.

## What it records per node

| Field | Source, in order of preference |
|---|---|
| `title` | `og:title`, else `<title>`, with the site name stripped |
| `kind` | `page`, `doc` (pages under `/inside/docs/`), `service` (pages under `/inside/services/<id>/`), `tag`, `substack`, `github`, `reddit`, `dashboard` (public Grafana dashboards linked from a crawled page) |
| `desc` | `og:description` or meta description; "Originally published at" boilerplate stripped; 300 characters at most; a description shared by three or more nodes counts as a site default and is dropped |
| `date` | `article:published_time`, a `<time datetime>`, the date in a machinebehavior.io header, the sitemap `lastmod`, the Substack post date, the previous snapshot |
| `space`, `tags` | Docs pages only: the `docs-space` meta and the `article:tag` metas written from front matter |

## Links

- **body**: links inside the page content.
- **nav**: links inside `<nav>`, `<footer>` and site headers. A tag index link and a tag page's "all posts" link count as navigation.
- **tree**: a docs or service page's `<link rel="up">` to its parent page, so the documentation tree and the catalog appear in the graph.

A dashboard node is not fetched: a Grafana page needs JavaScript to show its title. Its title is the link text used most often on the crawled pages, with generic texts such as "open" skipped.

## Guards

- Pages that answer with something other than HTML are dropped (Hugo tag pages without a template served RSS).
- A page that fails to load keeps its outgoing links from the previous snapshot.
- Tag pages with no content links are dropped.
- The deploy job keeps the committed snapshot when a crawl returns fewer nodes or links. See [Deploy pipeline](doc:eng/deploy-pipeline).
