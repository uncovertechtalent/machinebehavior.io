title: ADR-0053: A chief marketing officer seat owns reach, and public relations is one press page
summary: The house gets a seventh seat, the chief marketing officer, that owns reach: which audience a page reaches, through which surface, how that is measured, and whether search and AI answers return it. The publisher keeps editorial truth and the site gate. The seat reads the existing AI area, so the cockpit keeps its eight areas. Public relations is one page, /press/, under the seat, and the seat has its own request form.
parent: decision-log
order: 53
adr: 53
status: accepted
created: 2026-11-03
labels: adr, decision, inside, masthead, seats, press, aieo
owner: Stefan Coetzee
reviewed: 2026-11-03
review_by: 2027-02-01
type: explanation
---
## Context

The house has one holder and six seats ([ADR-0032](doc:eng/adr-0032-masthead-from-a-seats-file)). The publisher seat carried two jobs under one lens. Its first question was "Does it reach the audience, and through which surface?" and its other two were "Does it pass the editorial standards and the site gate?" and "Which claim on it is unverified, and is that labelled?" The first is a question about reach, the other two are questions about truth. A change that raises reach can lower truth, and a seat whose lens holds both questions has no place where the two can disagree.

The machinery split the same way. The publisher held `aieo`, the module that makes a page findable by search and by AI answers, next to the site gate, the change review, and the editorial standards. It also held the `predictions.hashes` gate, which keeps a prediction file matching its recorded hash. Both belong to a page's standing with an audience as much as to its correctness.

On 2026-11-03 Stefan Coetzee decided to split the seat: a seventh seat, chief marketing officer, owns reach, and the publisher keeps truth.

## Decision

**The seat.** `inside/masthead/seats.json` gains the seat `cmo`, title "Chief marketing officer", held by Stefan Coetzee, between the publisher and the chief knowledge officer in masthead order, with no bundle yet. Its lens has three questions: which audience a page reaches, through which surface, and how that is measured; which offer it feeds and what the reader's next step is; and whether the page carries the one-liner, the entity, and the link, so that search and AI answers return it.

**The areas.** The seat reads one area, `ai`, whose definition on the CTO powersuit pages is "Running AI in the company, and being found by AI", and whose `aieo` module is the house's findability work. The chief AI and technology officer reads `ai` too; two seats may read one area, as the publisher and the chief knowledge officer both read `knowledge` before this record.

**What moves, and what stays.** The `aieo` machinery entry and the `predictions.hashes` gate move from the publisher to the new seat, with their text unchanged. The publisher's areas become `delivery` and `knowledge`: its gates are the site gate, which is a deploy gate and so Delivery in the powersuit, and its editorial work is Knowledge. Its lens drops the reach question and gains "Does it say what its source says, with the source linked?" Its machinery keeps the site gate, the change review, and the editorial standards. The editorial standards stay on the masthead page.

**What the seat adds.** Two machinery entries and one gate. `press` is the press page. `reach signals` is the seat's measurement, described by the rule below. The gate `press.cite-verbatim` has the `where` value `policy`: every line the press page offers for quotation appears word for word on the page it links. The holder checks it by hand when the page changes; no code checks it yet.

**Public relations is one page.** [The press page](/press/) carries the house in one sentence and one paragraph, who holds the seats, a table of the main works with each canonical URL and one line that appears word for word on that page, the fact that the site has no logo file, the contact lines exactly as the Impressum gives them, how corrections are made with a link to the editorial standards, and a link to the seat's request form. It is the one page a journalist, a podcast host, a programme committee, or a standards body needs. It is hand-written, sits in the home section of `site/nav.yml` after the privacy notice, and adds nothing by hand to its structured data: the publisher of the site stays the Person node that `scripts/site_chrome.py` writes from `site/nav.yml`, and no Organization node exists.

**The measurement rule.** The seat measures reach with three sources and no other. Counts of what reaches the site come from the server's access log, which holds no IP address, as the [privacy notice](/privacy/) describes. The index submissions go out after every deploy from main ([deploy pipeline](doc:eng/deploy-pipeline), job 4). A fixed query set probed against AI search engines is the third; the [AIEO measurement](/aieo/measurement/) page lists that probe as not built, and no figure from it exists. [ADR-0010](doc:eng/adr-0010-no-third-party-requests) keeps every page free of requests to a third party, so no analytics script, tracking pixel, or embed reaches a page, and the seat's numbers come only from these sources. The panel that shows them does not exist yet. Until it does, the seat's dashboard on [Inside](/inside/) carries a labelled placeholder, "Reach signals", with no number, and the AIEO measurement page states what is and is not measured.

**The request form.** `.github/ISSUE_TEMPLATE/request-cmo.yml` has the body of the other six, the name "Request: Chief marketing officer", and the label `area:ai`. By the rule of [ADR-0052](doc:eng/adr-0052-requests-through-one-issue-form-per-seat), a form sets the seat's first area label, so the publisher's form changes from `area:ai` to `area:delivery`, and its description follows its new lens. The seat's tools slot on the Inside landing page holds a Press card and the Request card, with the Request card last.

**No ninth area.** The cockpit's eight areas are the eight areas of the CTO job, taken from `site/powersuit.yml` at the pinned powersuit release ([ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues)). A ninth area would be a change to the CTO powersuit, which this site does not own. The seat therefore reads an area that exists, and no area key is added to the cockpit, the seats contract, or any form.

## Consequences

The publisher and the new seat can now disagree on a page in the open: the publisher asks whether the page passes the standards and the gate, and the new seat asks whether it reaches the people it is for.

The publisher's request form carries another label. A request filed through it now lands in Delivery in the cockpit, where it landed in AI before; a request filed through the new form lands in AI. The cockpit shows seven forms, seven seat tabs, and seven tiles in the chief executive's roll-up; the tab row keeps one row at every width.

The seat starts with a placeholder where its signal should be. The panel for reach signals is the first follow-up, and it needs a data source that does not exist yet. Whether `press.cite-verbatim` gets a code check is the second: a script could compare each quoted line with its page, and until one does, the gate is a rule the holder follows by hand, and the masthead says so.

What this does not do. It adds no seat to any company's powersuit, no area to the cockpit, no analytics, and no request to a third party. It does not start the answer probe. It does not change the editorial standards, the site gate, or the private-terms check.

Checks: `scripts/test_build_masthead.py` holds the seven seats, the moves, and the contract; `scripts/test_build_inside_seats.py` holds the placeholder and the committed page's slot for the new seat; `scripts/test_issue_forms.py` holds the seven forms and their links. Steps and the contract: [Masthead page](doc:eng/masthead).
