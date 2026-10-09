title: ADR-0020: A five-minute founder tour on one page
summary: One page at /inside/tour/ walks a founder through the platform in six stops, each with a screenshot of the live page, what to notice, what it does in a company, and the link.
parent: decision-log
order: 20
adr: 20
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

A founder who gets one link has about five minutes. Inside has a front page, a service catalog, six docs spaces, a status page, a board and a deploy gate, and a first visit does not show which pages carry the evidence. The research note on enterprise portals lists what to show a founder in five minutes: the front page, one service page, the docs tree, an incident trail and the gate.

## Decision

One static page at [/inside/tour/](/inside/tour/) with six stops: the front page, one service, owned and dated docs with a decision record, one incident from the status page to the fix, a deploy that a failed check blocked, and, as an optional stop, cost and the map. Each stop has a screenshot of the live page, two or three lines on what to notice, one line on what the same part does for a team of 10 to 200 people, and the links. The incident stop needed a ticket on the board, so incident records gained a `tickets` field ([Status page](doc:eng/status-page)).

The screenshots are self-hosted WebP files with width, height and alt text, so the page sends no request to a third party; the stop on the blocked deploy shows the public GitHub Actions run as an image and links it. The page carries the top bar and the demo banner, and the banner on every Inside page except the map links it. The home page links it from "The whole body of work".

## Consequences

The screenshots age. Each caption carries its date, and `scripts/tour_shots.js` (puppeteer-core and a local Chrome, run from a scratch folder) retakes them; a stop whose page changes in a way the text no longer matches is retaken and its lines are checked against the live page before the push. The closing section names the builder and links Stefan Coetzee's LinkedIn profile; it carries no e-mail or phone number until the legal pages are live.
