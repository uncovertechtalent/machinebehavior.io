title: ADR-0040: Report pages carry the furniture of a consulting report
summary: The research section's report pages take over the evidence motifs of consulting articles: exhibits numbered in the HTML with a finding as the title, a Note line beside the Source line, references to exhibits in the text, At a glance at the top, sidebar boxes, a page-type pill, the reading time and a print stylesheet. Engagement furniture (share rails, stock hero art, AI summary buttons, ratings) stays out.
parent: decision-log
order: 40
adr: 40
status: accepted
created: 2026-10-26
labels: adr, decision, design-system, research, site-chrome, accessibility, print
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

[ADR-0039](doc:eng/adr-0039-research-report-theme) gave the research section the look of a consulting report: type, colour, the title band and numbered tables. On 2026-10-26 the article pages of mckinsey.com (the AI operating system article), bcg.com (the AI value gap article) and hbr.org were read for their layout motifs, beyond type and colour. They share one article system. A summary comes first ("At a glance" at McKinsey). Every exhibit is labelled "Exhibit N", states its finding as its title ("An AI operating system drives value creation from strategy to execution", McKinsey; BCG's exhibit on AI spending and reinvested gains), and carries a source line and a note line under it (BCG: "Source: … Note: …"). The text refers to exhibits by number. Boxed sidebars hold definitions and cases. A meta line gives the type, date and reading time ("Article · September 30, 2025 · 3 min read", BCG), an outlined pill names the topic, and the article can be downloaded (a 12-page PDF at McKinsey).

Around that system the sites add engagement furniture: sticky share, save and subscribe rails, star ratings, "most popular" lists, full-bleed AI hero art, an AI "Summarize" button and a chatbot. Stefan Coetzee chose the evidence motifs on 2026-10-26.

## Decision

**Exhibits are numbered in the HTML.** On every report page `scripts/site_chrome.py` (`number_exhibits`) writes "Exhibit N" into a span at the start of each table caption, in page order, and writes the same number into every `<a class="exhibit-ref" href="#id">` that points at a captioned table's id. A reference to any other id stops the chrome pass. This replaces ADR-0039's CSS counter: a number in the HTML reaches screen readers, search, copied text and print, and a reference in the text always matches its exhibit. `site_chrome.py --check` holds the numbers in the required job.

**An exhibit's caption states its finding.** "The ablated model keeps its facts and folds on every order the stock model refuses", where the caption used to name the table. Method tables state what they show ("The arms differ only in what they add to the shared task prompt"). Captions carry no counted nouns ("the pressure characters", not "the six pressure characters"); measurements stay ("42 of 56 runs").

**A Note line beside the Source line.** A `<p class="exhibit-note">` under an exhibit gives the sample, the settings and the caveats a reader needs to read it: the arm, the interval, a superseded unit, a pilot label. The Source line still appears only where the data is published (ADR-0039).

**At a glance opens every report page.** A `<section class="glance">` after the title band holds one bullet per finding: an italic sentence that states it, then the number and the exhibit behind it. It is the governing thought of the page, and on the experiments page one bullet per experiment. Every sentence restates a number or a statement already on the page; At a glance adds no claim.

**Sidebars.** Notes that a reader can skip and come back to (a unit note, a disclosure, a conflict of interest, a same-day update) go in an `<aside class="sidebar">`, a grey box in the text flow.

**The page type is a pill before the eyebrow.** A `<span class="kind">Experiment</span>` stands just before the eyebrow in the title band, outlined. Pages whose eyebrow began with their type ("Article ·", "Case file ·", "Method ·") moved that word into the pill. The eyebrow itself stays plain text: the gate's self-assessment check and the map crawler's date reader both read the eyebrow only up to its first tag. The section index, written by `build_hubs.py`, has no pill yet.

**Reading time and print.** The breadcrumb line of every hand-written research page, ledgers and indexes included so that they print too, gives the reading time, the page's own text at 230 words a minute rounded up (`read_minutes`), and a "Print or save as PDF" button. A print stylesheet drops the site chrome and the band's fill, prints the title in ink, keeps exhibits, sidebars and At a glance whole on a page, and prints the address of each outside link. Saving the print as PDF replaces a separate PDF download, so there is no second copy of a page to keep in step. The button uses an inline click handler, as the top bar uses an inline script; a Content-Security-Policy without `'unsafe-inline'` would need both moved into a same-origin file.

**Left out.** Share and save rails, subscribe boxes, ratings and popularity lists need tracking or a third party ([ADR-0010](doc:eng/adr-0010-no-third-party-requests)). Stock hero art adds images that carry no evidence; the band does the same job. An AI summary button repeats At a glance, and llms.txt already serves machine readers. Audio versions and footnote pop-overs are not needed for the current pages.

## Consequences

The report pages read as reports: a reader gets the findings in At a glance, each exhibit's claim in its title, and the conditions in its note, before the method. Seven pages gained At a glance and finding titles, sixteen exhibits gained numbers in the HTML, and every research page except the section index gained a pill. A new report page needs At a glance and finding captions written by its author; the chrome numbers the exhibits and computes the reading time. A finding title is a claim and is checked against the table like any other sentence. The reading time changes when the text changes, so a text edit can change a page's chrome line.
