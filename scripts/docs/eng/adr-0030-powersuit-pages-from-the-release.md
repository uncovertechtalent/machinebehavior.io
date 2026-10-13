title: ADR-0030: The CTO powersuit pages are built from the pinned release
summary: /cto-powersuit/ and one page per plugin are built by scripts/build_powersuit.py from the powersuit repository at a release tag and commit pinned in site/powersuit.yml; the pages carry a sidebar of the plugins by area in place of the section sidebar, and CSS scoped to them.
parent: decision-log
order: 30
adr: 30
status: accepted
created: 2026-10-13
labels: adr, decision, powersuit, navigation, generated-pages
owner: Stefan Coetzee
reviewed: 2026-10-13
review_by: 2027-01-11
type: explanation
---
## Context

/cto-powersuit/ listed the 18 plugins of the CTO powersuit in two hand-written tables, one line each ([#85](https://github.com/uncovertechtalent/machinebehavior.io/issues/85)). The facts a reader needs per plugin (version, skills, gate checks) live in the powersuit repository and change with each release, so a hand-written copy goes stale with the next tag. On 2026-10-13 Stefan Coetzee approved a design for these pages: the plugins as tiles grouped by the area of the CTO job, a sidebar with the page sections and the plugins by area, and one page per plugin ([#90](https://github.com/uncovertechtalent/machinebehavior.io/issues/90)).

## Decision

- `scripts/build_powersuit.py` builds the plugin pages from the powersuit repository at the release pinned in `site/powersuit.yml`: a tag and the commit it points to. It reads every file from that commit with `git show`, and it stops when the tag resolves to another commit or the manifest's plugins differ from the areas in `site/powersuit.yml`. The install commands on every page pin the same tag, so the pages and the install agree.
- `site/powersuit.yml` holds what the repository does not: the areas of the CTO job, one line per plugin (true for the pinned release), and where each module runs on this site. A new release means a new tag and commit there, a check of the lines, and a rebuild.
- The overview stays a hand-written page. The generator fills its static blocks (eyebrow, install commands for both installers, latest release, licence, area tiles, knowledge tiles, release line), writes the overview's line in llms.txt, and writes `cto-powersuit/modules.json`. Every release name on the overview sits in those blocks: the build stops when the hand-written text (body or meta) names a release, or states a licence or a plugin or module count that differs from the release.
- `scripts/site_chrome.py` stays the one writer of the navigation ([ADR-0021](doc:eng/adr-0021-one-navigation-source)): `auto: powersuit` in `site/nav.yml` adds the plugin pages from `modules.json`, and on /cto-powersuit/ and its plugin pages the sidebar lists the overview's sections and the plugins by area in place of the CTO section sidebar ([ADR-0022](doc:eng/adr-0022-section-sidebars)). Each plugin page gets a `SoftwareSourceCode` node that is part of the overview's node ([ADR-0027](doc:eng/adr-0027-structured-data)).
- The top bar, the footer and the reading layout stay as on every page ([ADR-0025](doc:eng/adr-0025-one-design-system)). The sidebar and tile styles are in `/cto-powersuit/powersuit.css`, linked from these pages only, with values from the design tokens.

## Consequences

- A release of the powersuit reaches the site only through a pull request that moves the pin and rebuilds; nothing fetches the repository at deploy time. `python3 scripts/build_powersuit.py --check` reports pages that differ from the pinned release; the job `Script tests` runs it, with the generator's tests, on every pull request. It writes nothing.
- The pages say what the pinned release contains. Work on the powersuit's main branch after the tag shows only in the release line on the overview, until the next tag.
- A rebuild of an unchanged release changes no file. A plugin page's sitemap date moves only when its content changes, and the IndexNow job submits only the plugin pages a rebuild changed.
- The generator writes the pages on a maintainer's machine with git and network access to GitHub, never in CI or the deploy job; CI runs only its `--check`.
