title: ADR-0039: The research section uses a report theme, set by the site chrome
summary: Every page under /research/ gets data-mb-theme="report": a fixed light theme in the register of a consulting report, with Newsreader 300 headlines over an Inter body, the title on a dark teal band, hairline tables, and captioned tables numbered as exhibits with a source line where the data is published. The chrome sets it by URL, as ADR-0035 does for Inside.
parent: decision-log
order: 39
adr: 39
status: accepted
created: 2026-10-26
updated: 2026-10-26
labels: adr, decision, design-system, research, site-chrome, typography, accessibility
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

The research section (/research/: the claims ledger, experiments, objections, evidence, slips, case files, articles, terms and the red team) read like every other reading page: a serif body on the reading surface, mono tables, and dark in a dark system setting. Its readers are CTOs and CEOs, who read consulting reports every week. Since 2026-10-24 the CTO powersuit page positions the work as a complement to McKinsey's AI operating system article, so a finding on this site sits next to that article in the reader's week.

On 2026-10-26 a script in the browser read the computed styles of four consulting publishers and four research publishers:

| Site | Headlines | Body | Colour |
|---|---|---|---|
| mckinsey.com | Bower, weight 300 | McKinsey Sans 300, 20/32 px | deep navy, electric blue, light grey page |
| bcg.com | Henderson BCG Serif 300 | Henderson Sans | dark green, beige page, neon green accent |
| hbr.org | Tiempos Headline | Tiempos Text, GT America | red |
| deloitte.com (Insights) | Adelle Sans Condensed 900 | Adelle Sans Condensed | black, green |
| anthropic.com | anthropicSans | anthropicSans; anthropicSerif loaded | ivory page, near-black text |
| ourworldindata.org | Playfair Display | Lato | navy text, cream page |
| epoch.ai | Messina Sans | Messina Sans | dark teal, mint |
| metr.org | Instrument Sans | Instrument Sans | teal green |

bain.com answered with a bot check and was not read. The consulting register is a light-weight serif for headlines, a body of 18 to 20 px, a light page, one deep colour and one accent, and numbered exhibits with a title above and a source line below. Bower is McKinsey's own typeface (Radim Peško with Wolff Olins); McKinsey's own slides fall back to Georgia and Arial.

Three registers were built on the abliteration experiment page and compared on screenshots: a report (the consulting register), a paper (LaTeX and Tufte: EB Garamond, numbered sections, three-rule tables) and a lab (the research labs: Inter Tight on ivory, mono tables). The paper is closest to the current serif pages and so changes least; the lab reads as an AI lab, not an adviser. Stefan Coetzee chose the report on 2026-10-26.

## Decision

**The chrome sets the theme by URL.** `THEMED` in `scripts/site_chrome.py` becomes a list of URL prefixes and themes: `/inside/` gets `intranet` ([ADR-0035](doc:eng/adr-0035-intranet-theme-on-every-inside-page)), `/research/` gets `report`, every other page gets no attribute. `python3 scripts/site_chrome.py --check` holds it in the required job, and a new research page gets the theme from the chrome with no step of its own. The theme is fixed: there is no switch for the reader.

**Light in both system settings.** The dark values in `design/tokens.css` skip the report theme, as they skip the intranet theme. Every consulting and research publisher read above serves a light page. The rest of the public site keeps light and dark from the visitor's setting, and the top bar stays dark. Replaced by [ADR-0042](doc:eng/adr-0042-one-light-scheme): every page is light.

**Our colours, their register.** The tokens keep the site's teal as the one accent (#1F6B5E on white) and use a deep teal ink (#0F1E22) and a dark teal title band (#0E2A2B). No other publisher's colour or typeface is used, and nothing on the pages claims an affiliation.

**Type.** Headlines are Newsreader at weight 300 (Production Type), the body and tables Inter (Rasmus Andersson) at 400, 400 italic and 600, both from @fontsource 5.3.0, latin subset, under the SIL Open Font License 1.1, self-hosted in `/fonts/` with their licence files ([ADR-0010](doc:eng/adr-0010-no-third-party-requests)). The five files weigh about 119 KB together; a browser fetches them only on a page that uses them, so pages outside the theme load nothing new. The chrome (bar, sidebar, footer) keeps its own fonts.

**Layout.** The eyebrow, title and subtitle sit on the dark band. The band and its light text share one selector, `header:has(> h1)`, so a browser without `:has()` (Firefox before 121, Safari before 15.4) shows the title in the page colours with no band, never light text on white; `h2` headings are Newsreader 300 with a short teal rule above; tables lose their vertical rules and get a dark top rule, uppercase column heads and hairlines between rows.

**Exhibits.** A table with a `<caption>` is an exhibit: the theme numbers it ("Exhibit 1", "Exhibit 2" in page order) above its caption. Replaced by [ADR-0040](doc:eng/adr-0040-report-furniture-on-research-pages) for the numbering: the site chrome now writes the number into the HTML. Report pages caption their tables: the experiments, the experiment pages, the red-team method, the case files and the articles. Ledgers and indexes (the claims ledger, objections, evidence, slips, the red-team catalogue) keep plain tables. A `<p class="exhibit-source">` under an exhibit names the published data behind it and links the file; an exhibit whose data is not published has no source line rather than an unchecked one. In this change the abliteration page has source lines; the other exhibits get them when their run records are published.

**Contrast.** On white the text tokens reach 17.1:1, 10.0:1 and 6.9:1 and the teal 6.3:1; on the sunken surface the lowest pair is the teal at 5.7:1. On the band the title reaches 15.2:1, the subtitle 11.6:1 and the eyebrow 8.6:1. The focus ring of a link on the band takes the eyebrow colour (8.6:1), because the teal ring of the rest of the page would reach only 2.4:1 there. Every pair meets WCAG 2.2 AA, the ring the 3:1 of SC 1.4.11.

## Consequences

The research section reads as a set of reports, distinct from the rest of the public site and from Inside, in both system settings. Fifteen pages change by one attribute on `<html>`; five pages gain table captions, and the abliteration page gains two source lines. A new table on a report page needs a caption to become an exhibit. Readers who set a dark system theme see the research pages light. The social preview images of the research pages still show the old look until they are taken again.
