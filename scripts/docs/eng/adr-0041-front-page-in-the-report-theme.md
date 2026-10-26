title: ADR-0041: The front page uses the report theme, with one message and one lead finding
summary: The front page takes the report theme of ADR-0039 and the layout of a consulting home page: a title band with the second-brain graph, the programme's finding, a lead finding with its number chosen by hand, research rows and doors written by build_fallbacks.py from site/nav.yml and the research pages, two Use it cards, and where it aims. The long explanatory paragraph moves to the research index.
parent: decision-log
order: 41
adr: 41
status: accepted
supersedes: adr-0028-home-page-portal-front
created: 2026-10-26
labels: adr, decision, design-system, front-page, site-chrome, research
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

On 2026-10-26 the front page held 883 words and 38 links in seven sections: a hero with a long explanatory paragraph, the one-line finding and three buttons beside the second-brain graph; eight section cards; four research cards with descriptions of up to 220 characters; topic chips; a "Use it" block with a paragraph and four cards; five "Elsewhere" cards; and a closing statement. Read the same day, mckinsey.com's home page held about 307 words and 28 links and bcg.com's about 692 words: one message, one lead story, a few ways in. That was the portal front page of [ADR-0028](doc:eng/adr-0028-home-page-portal-front), which this record replaces. Stefan Coetzee called the front page cluttered, a mockup in the report theme was rendered beside the live page, and he chose it.

## Decision

**The front page carries the report theme.** `THEMED_PAGES` in `scripts/site_chrome.py` gives the exact URL `/` the report theme of [ADR-0039](doc:eng/adr-0039-research-report-theme); a prefix entry cannot, because every URL starts with `/`. The title band, the type and the colours are the research section's.

**One message, then one lead.** The title band holds the page-type pill, the eyebrow, the name, the "Fix your models" line and two buttons, with the second-brain graph as its art (it links to the map). Under it the programme's finding stands alone: "Sycophancy is layered symptom substitution". Then the lead finding: one research page, chosen by hand in `index.html`, with its headline number set large in the way consulting exhibits call out a figure ("54 of 54").

**Generated lists stay generated.** `home()` in `scripts/build_fallbacks.py` writes two blocks. The research rows are the newest published research pages whose kind pill is a finding (Experiment, Case file, Article, Method), leaving out the lead; each row shows its pill, title and date. The doors are six sections (Research, Red team, Inside, Docs, Topics, CTO), each with its one-line `door:` text from `site/nav.yml`. Mission Control is reached through Inside, and the second brain through the graph in the band.

**What left the front page.** The explanatory paragraph moves to the top of the research index (`RESEARCH_INTRO` in `scripts/build_hubs.py`), where a reader who chose the research reads it; the research index also gets its kind pill. The topic chips go: Topics is a door and is in the navigation. The "Use it" paragraph and the two lesson cards become two cards, TYChat and the CTO powersuit. The five "Elsewhere" cards become one line of links under "Where it aims". The tour button goes; the tour is reached from Inside.

## Consequences

The front page drops to about 290 words and 21 links in one column of decisions: what this is, what it found, the latest finding, where to go next. The lead finding needs a person to change it when a newer result should lead; the rows under it update on every build. A section that should become a door needs a `door:` line in `site/nav.yml` and an entry in `HOME_DOORS`. The front page is light for every visitor, as every page is after [ADR-0042](doc:eng/adr-0042-one-light-scheme).
