title: ADR-0047: The research section and the front page use a paper theme
summary: The report theme of ADR-0039 becomes a paper theme, data-mb-theme="paper", on every page under /research/ and on the front page. EB Garamond throughout on cream paper, a centred title with no band, numbered sections, tables with three rules and "Table N." above the caption, italic source and note lines, At a glance as an abstract between rules. The chrome, the numbering and the furniture of ADR-0040 and ADR-0041 stay; the type, the colours, the band and the exhibit label are replaced.
parent: decision-log
order: 47
adr: 47
status: accepted
created: 2026-10-27
labels: adr, decision, design-system, research, front-page, site-chrome, typography, accessibility, print
owner: Stefan Coetzee
reviewed: 2026-10-27
review_by: 2027-01-25
type: explanation
---
## Context

[ADR-0039](doc:eng/adr-0039-research-report-theme) chose the register of a consulting report for the research section on 2026-10-26, from three mockups built on the abliteration experiment page: a report, a paper (LaTeX and Tufte: EB Garamond, numbered sections, three-rule tables) and a lab. [ADR-0040](doc:eng/adr-0040-report-furniture-on-research-pages) added the furniture of a report (numbered exhibits with a finding as the title, source and note lines, At a glance, sidebars, the page-type pill, the reading time and print) and [ADR-0041](doc:eng/adr-0041-front-page-in-the-report-theme) put the front page in the same theme. On 2026-10-27 Stefan Coetzee chose the paper instead ("I chose A, but I want B instead"), after a mockup of the paper on three pages as they stand after ADR-0046: a case file, the abliteration probe and the front page.

The paper register, as the mockup set it: one serif face throughout, cream paper, a centred title over an italic lede, sections numbered in the margin of the heading, a table captioned above as "Table 1." with a heavy rule above and below and a hairline under the header row, the source and the note in italic beneath, and an abstract between two rules before the first section.

## Decision

**The theme is `paper`.** `THEMED` in `scripts/site_chrome.py` gives `/research/` the value `paper` and `THEMED_PAGES` gives `/` the same, in place of `report`; the tokens block, the stylesheet rules and `scripts/test_site_chrome_theme.py` follow the name. Nothing else about the chrome changes: the theme is still set by URL, still fixed, still light.

**Type.** EB Garamond (Georg Duffner, Octavio Pardo) at 400, 400 italic, 500, 500 italic and 600, from @fontsource 5.3.0, latin subset, under the SIL Open Font License 1.1, self-hosted in `/fonts/` with its licence file ([ADR-0010](doc:eng/adr-0010-no-third-party-requests)). The five files weigh about 127 KB together, and a browser fetches them only on a page that uses them. Newsreader and Inter leave `/fonts/` with their licence files; no page outside the theme used them. The body is set at 20 px (18 px on narrow screens), justified with hyphenation, in a column of 680 px; the chrome (bar, sidebar, footer) keeps its own fonts.

**Paper.** The surfaces are cream (#FFFFF8, the sunken surface #F5F4E9), the ink near black (#141414, #2A2A2A, #5A5A55), the hairline #CFCFC4, and the site's teal darkened to #1F5F55 as the one accent. The band tokens go. On the paper the text tokens reach 18.3:1, 14.3:1 and 6.9:1 and the teal 7.4:1; on the sunken surface 16.7:1, 13.0:1 and 6.3:1 and the teal 6.7:1. Every pair meets WCAG 2.2 AA; the hairline carries no text.

**Title.** Centred, with no band: the page-type pill and the eyebrow in small caps (the pill in a hairline box), the title at weight 400, the lede in italic, a hairline under the header, which gives way when At a glance follows. The `header:has(> h1)` selector of ADR-0039 stays; a browser without `:has()` shows the title left-aligned in the same colours, which loses the centring and nothing else.

**Sections.** The `h2` headings of a reading page are numbered by a CSS counter ("1 Setup", "2 Result"); small-caps labels (`h2.label`), At a glance and the front page are not. The number lives in the CSS and not in the HTML where nothing refers to a section by number; table numbers stay in the HTML (ADR-0040), because the text refers to them. A page whose headings carry their own numbers sets `data-own-numbering` on its `.sheet` and the counter stays off: the red-team method, whose contents list and text refer to its sections by number, the evidence page, and the experiments index, whose headings carry experiment ids. The run-in small-caps lead-ins in the text stay as written.

**Tables.** A captioned table is "Table N.", in small caps at the start of its caption, which sits above the table; the chrome writes the number as ADR-0040 set out, with the word changed. `number_exhibits` and the class names `exhibit-n`, `exhibit-ref`, `exhibit-source` and `exhibit-note` keep their names, so no page changes its markup. Three rules: a heavy rule above and below the table, a hairline under the italic header row, no vertical rules and none between rows. The source and note lines are italic beneath the table. A reference in the text reads "Table 2", in small caps.

**At a glance, sidebars, the print button.** At a glance is an abstract: a rule above, a hairline below, no box, its heading in small caps. A sidebar is an indented block with a hairline on its left. The print button is text in the teal inside a hairline box.

**The front page.** The lead is centred: the pill, the eyebrow, the name, the "Fix your models" line and two buttons, with the second-brain graph beneath them as Figure 1. The graph is a `<figure>` in `index.html` and its caption a `<figcaption>`, so it reaches screen readers, search and copied text; it is still drawn on its dark canvas ([ADR-0043](doc:eng/adr-0043-map-draws-on-a-dark-canvas)) and still opens the map. The section labels stay small caps and are not numbered, the lead finding's number is set in Garamond, and the lead finding, the rows, the doors and Where it aims sit between rules on the paper instead of in grey boxes.

**Print.** The print stylesheet keeps what ADR-0040 set (the chrome drops out, tables, sidebars and At a glance stay whole on a page, outside links print their address), prints on white rather than cream, and loses the band rules.

**What this replaces.** In ADR-0039 the type, the colours, the band, the layout and the exhibit label; in ADR-0040 the label "Exhibit N", the glance box, the grey sidebar, the pill on the band and the print rules for the band; in ADR-0041 the title band; in [ADR-0042](doc:eng/adr-0042-one-light-scheme) and [ADR-0043](doc:eng/adr-0043-map-draws-on-a-dark-canvas) the sentences that keep the band dark as chrome. Each record carries a sentence where it is replaced and stays accepted for the rest: the chrome setting the theme by URL, light in every setting, numbers in the HTML, finding captions, the Note line, At a glance, the reading time, the generated rows and doors.

## Consequences

Every research page and the front page change by one attribute on `<html>`, and every numbered table on the five pages that have them changes its label. The research section and the front page read as a set of papers; Inside keeps its intranet theme and the rest of the public site its own look. A new research page needs nothing of its own: the chrome sets the theme, numbers the tables and computes the reading time. The search index and llms-full.txt carry the new labels from their next build. The social preview images of the research pages and the front page show the report look until they are taken again.
