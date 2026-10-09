title: Service catalog
summary: The catalog at /inside/services/ is built from one YAML file per service in services/, validated at build; each service is a page and a node in the map.
order: 66
labels: inside, services, catalog, ownership
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The [service catalog](/inside/services/) lists every service that runs the platform, with the owner, tier, lifecycle, SLOs, dashboard, runbooks, docs, repository and dependencies. Each service has its own page, and each page is a node in the [map](/map/) linked to its docs and dashboards.

## Source

One file per service in [services/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/services). `scripts/build_inside.py` reads them with a strict YAML reader (`scripts/mini_yaml.py`, standard library only) and writes:

- `/inside/services/` and `/inside/services/<id>/`;
- `inside/services/services.json`, the machine-readable catalog, also read by the search index;
- a managed block in `sitemap.xml` and a section "Inside services" in `llms.txt`.

```bash
python3 scripts/build_docs.py     # first: the catalog checks its docs links against the docs build
python3 scripts/build_inside.py
```

## Fields

| Field | Required | Values |
|---|---|---|
| `id` | yes | Same as the file name |
| `name`, `description` | yes | Plain text; the description is the meta description and the search snippet |
| `owner` | yes | The person who answers for the service |
| `operator` | no | Who runs it day to day, when that is not the owner (for example an agent session) |
| `tier` | yes | 1, 2 or 3, see below |
| `lifecycle` | yes | `experimental`, `production`, `deprecated` |
| `system` | yes | `Publishing`, `Observability`, `Research tooling`, `Agents` |
| `url`, `repository` | no | https URLs; `repository: private` for a private repository |
| `dashboard` | no | `name` and `url`; the URL must be a public Grafana dashboard |
| `slo` | no | A list of `name`, `target`, `good` |
| `docs`, `runbooks` | yes | Lists of `doc:space/slug`; may be empty |
| `depends_on` | yes | Service ids; may be empty |
| `external` | no | Dependencies outside the catalog, as plain names |
| `status` | no | Where the [status page](/inside/status/) reads the current state: `gate` (a `conformity/latest.json` URL) and `deploys` (a repository in the deploy feed) |
| `principles` | no | The SRE principles the service applies, as `doc:sre/principle-<name>`; each must be a page under [Principles in practice](doc:sre/principles-in-practice). Shown under "SRE principles applied"; the principle page lists the service back |

The build stops on an unknown field, a missing required field, a value outside the allowed set, an id that differs from the file name, a docs link to a page that does not exist, or a dependency on an unknown service.

## Tiers

| Tier | Meaning |
|---|---|
| 1 | Readers meet it directly, or it decides whether a deploy goes out. First in line when something breaks |
| 2 | Keeps the platform observable and the research running. Fixed the same day |
| 3 | Tooling a reader does not meet directly. Waits for the next working session |

## In the map

A service page links its principle pages in the body, and each principle page links back to the services that name it, so the map holds those links in both directions. The crawler gives `/inside/services/<id>/` pages the kind `service` and adds the public Grafana dashboards they link as `dashboard` nodes, titled by the link text used most often. A service page's `<link rel="up">` to the catalog is a `tree` link. See [Map crawler](doc:eng/map-crawler).

## Add or change a service

1. Copy a file in `services/` that is close to the new service and edit it.
2. Run both builds; fix what the build reports.
3. Run the gate dry run, then pull, commit and push. See [Deploy pipeline](doc:eng/deploy-pipeline).
