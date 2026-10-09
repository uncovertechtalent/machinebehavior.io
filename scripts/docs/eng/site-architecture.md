title: Site architecture
summary: Three static sites on GitHub Pages, one shared conformity action, and Substack as the fourth publication.
order: 10
labels: architecture, github-pages, static-site
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Three sites publish the work. All three are static files served by GitHub Pages and deployed by GitHub Actions. A fourth publication, the Substack newsletter, is hosted by Substack and only read by the crawler.

| Site | Built with | Repository | Role |
|---|---|---|---|
| machinebehavior.io | Hand-written HTML, one shared stylesheet, Python generators for the slips page, the map data and these docs | [uncovertechtalent/machinebehavior.io](https://github.com/uncovertechtalent/machinebehavior.io) (public) | Research programme: claims, experiments, objections, case files, Inside, map, docs |
| tychat.io | Static pages and plain-text lessons | [uncovertechtalent/tychat.io](https://github.com/uncovertechtalent/tychat.io) (public) | Lessons a chat model reads on request, indexed in `llms.txt` |
| uncovertechtalent.com | Hugo | private repository | Blog and the Uncover Tech Talent offer |
| Substack | Substack | none | Newsletter; canonical home of some pieces |

## Shared parts

- **Conformity action.** The checks live in a composite action at `.github/actions/conformity/` and run on all three sites with a per-site configuration. See [Conformity gate](doc:eng/conformity-gate).
- **Machine-readable entry points.** Each site serves `sitemap.xml` and `llms.txt`. On machinebehavior.io, `llms.txt` lists every page with a one-line summary, including the [docs](/inside/docs/).
- **Conformity record.** Each site publishes `/conformity/latest.json`; [Inside](/inside/) reads all three to show site status.

## machinebehavior.io layout

| Path | Contents |
|---|---|
| `/` and one directory per page | `index.html` per page, root-absolute links only |
| `style.css` | Shared stylesheet of the research pages |
| `conformity/` | Rendered gate page, `latest.json`, `site-tier.json` (rule tiers), `requirements.json`, probe records |
| `map/` | The map page and `graph.json` |
| `inside/` | Inside front page; `inside/docs/` holds this tree |
| `predictions/` | Hashed predictions, checked by the gate |
| `scripts/` | Generators and the crawler; `scripts/docs/` holds the docs sources |

Several Claude Code sessions push this repository, each owning one track of work. The gate is the shared control between them: a session can push, and only a passing check deploys.
