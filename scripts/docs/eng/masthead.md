title: Masthead page
summary: How /inside/masthead/ is built from inside/masthead/seats.json, what the file holds, what the contract check refuses, and where the check runs.
order: 67
labels: inside, masthead, seats, generated-pages, how-to
owner: Stefan Coetzee
reviewed: 2026-10-16
review_by: 2027-01-14
type: how-to
---
The [masthead](/inside/masthead/) shows the seats of the house, the holder of each, the machinery that runs the seat's staff work, and the gates that apply with where each one runs, plus the editorial standards. The seats come from one data file, `inside/masthead/seats.json`; `scripts/build_masthead.py` writes the page's blocks from it ([ADR-0032](doc:eng/adr-0032-masthead-from-a-seats-file)).

## The file

| Key | Form | Meaning |
|---|---|---|
| `schema` | the integer 1 | The contract version |
| `updated` | `YYYY-MM-DD` | The date of the last edit; the sitemap date of the page must match it |
| `house` | up to 60 characters: letters, digits, spaces, `.` and `-` | The house name, in one place |
| `source` | up to 400 characters | One paragraph on where the file comes from |
| `where` | an object of 1 to 8 entries, each a short key and one line | The places a gate can run; every gate's `where` is one of these keys |
| `seats` | a list, one entry per seat, in masthead order | `ceo`, `cto`, `cfo`, `chro`, `publisher`, `cko`; each at most once |

Per seat:

| Key | Form | Meaning |
|---|---|---|
| `seat` | one of the six keys | The seat |
| `title` | up to 80 characters | The title shown on the page |
| `holder` | up to 80 characters | The person who holds the seat |
| `areas` | a non-empty list of distinct keys from the cockpit's eight | The areas the seat reads; each links to the cockpit |
| `bundle` | `null` or a slug | The bundle of the seat in the CTO powersuit, once one exists |
| `machinery` | 1 to 20 rows of `name` and `what` | The modules and skills that do the seat's staff work |
| `gates` | 1 to 20 rows of `check`, `where`, and `what` | The checks a change in the seat's scope passes, each with where it runs |

Free text (`what`, `source`, the values of `where`) is at most 400 characters with no angle bracket, no control or format character (bidi overrides and zero-width characters included), and no URL. Names, titles, holders, and `where` keys allow letters, digits, spaces, and `. , & / : ( ) -`.

## Build and check

```bash
python3 scripts/build_masthead.py            # check the file, write the blocks, apply the chrome
python3 scripts/build_masthead.py --check    # write nothing; exit 1 on a contract error, a stale block, or a stale sitemap date
python3 scripts/test_build_masthead.py       # the tests: contract variants, blocks, --check on an edited copy
```

The build writes four blocks between `<!-- static:masthead-… -->` markers in `inside/masthead/index.html`: the eyebrow, the lede, the `where` map, and the seats. Everything outside the markers is hand-written page content. The build also sets the page's `lastmod` in `sitemap.xml` to the file's `updated` date, which the chrome uses for the page's Updated line and `dateModified`.

`--check` runs in the Conformity checks job before the gate, so a file that breaks the contract, or a page whose blocks were edited by hand, can neither merge nor deploy. The tests run in the Script tests job. The area titles are read through `scripts/build_cockpit.py` from `site/powersuit.yml` and `cto-powersuit/modules.json`, so the masthead and the cockpit cannot drift apart on them.

## Editing

1. Edit `inside/masthead/seats.json`. A seat that moves to another person is one changed `holder`. A new gate needs a `where` from the map; a gate this site does not run cannot carry `site gate`.
2. Set `updated` to today.
3. Run the build, then `python3 scripts/site_chrome.py --check` and the gate dry run from `CLAUDE.md`.
4. Open the pull request with the issue in its title.

The file is hand-edited for now. The seats file of the local cockpit, and a command that writes this public copy from it, are planned outside this repository.
