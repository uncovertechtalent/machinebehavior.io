title: ADR-0052: Requests to the house come in through one issue form per seat
summary: Inside shows the house's work and takes nothing in. Each of the six seats now has one GitHub issue form that carries the shape of the first fixed-shape request (what, why, blocked on, done when) and sets the seat's area label, and each seat tab on the Inside landing page links to its form. Intake is public by construction, the cockpit's trust rule is unchanged, and a login, a form on the site itself, and stages as labels are later decisions.
parent: decision-log
order: 52
adr: 52
status: accepted
created: 2026-11-03
labels: adr, decision, inside, issues, requests
owner: Stefan Coetzee
reviewed: 2026-11-03
review_by: 2027-02-01
type: explanation
---
## Context

Inside projects the house's work outward. The board and the cockpit read the issues of the public repositories ([ADR-0011](doc:eng/adr-0011-ticket-board-from-github-issues), [ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues)), the seat tabs of the landing page count and list them ([ADR-0034](doc:eng/adr-0034-inside-intranet-theme-and-seat-tabs), [ADR-0049](doc:eng/adr-0049-seat-pane-grammar)), and the page takes nothing in. A visitor, or an officer of the house, who wants something from a seat has no shaped way to ask. The two issue templates in the repository, a bug and a change request, cover a defect in the site and a change to it. Neither asks a seat for anything.

Issue 230 on the repository is the first request with a fixed shape: what is asked for, why, what it is blocked on, and what done looks like. Those sections hold what a seat needs to decide, and the issue carries the labels the cockpit needs to place it. It was written by hand, and nothing in the repository gives the next author that shape.

The [access model](doc:eng/access-model) already names the production end state: Inside behind an identity-aware proxy, with public, internal, and restricted spaces, and access granted per person and device. This site is the public demo of that. No login exists on it, and none is added before the end state is built, so any intake today is open to anyone with a GitHub account and is public text.

## Decision

**One issue form per seat.** Six GitHub issue forms in `.github/ISSUE_TEMPLATE/`, in masthead order: `request-ceo.yml`, `request-cto.yml`, `request-cfo.yml`, `request-chro.yml`, `request-publisher.yml`, and `request-cko.yml`. Each is named "Request: <seat title>", and its description says in one sentence what the seat decides or does, taken from the seat's lens questions in the seats file ([ADR-0032](doc:eng/adr-0032-masthead-from-a-seats-file)).

**The shape.** Every form has the same fields in the same order: What, Why, Blocked on, Done when (all required), Constraints (optional), Kind (a dropdown of decision, action, or finding), and a required checkbox that the text holds nothing private. The text above the fields repeats the rule of the two older templates: issue text is public, so private addresses, host names, personal details, and financial details stay out, while list prices, specs, and measured results are fine.

**The area label.** Each form sets the seat's first area label at creation: `area:direction` for the chief executive, `area:delivery` for the chief AI and technology officer, `area:money` for the chief financial officer, `area:people` for the chief human resources officer, `area:ai` for the publisher, and `area:knowledge` for the chief knowledge officer. It sets no other label. The kind, the status, and the priority are set by a maintainer at triage, and the Kind dropdown tells the maintainer which kind label was asked for. The forms set no title prefix.

**A Request link on each seat tab.** The tools band of every seat dashboard on the Inside landing page gains one card, last in the band: the heading "Request", the line "Ask this seat for a decision or an action. The text is public.", and a link, "Open a request", to the seat's form on GitHub. The card is the same on every seat; only the seat in the address changes. It sits in the hand-written slot of each seat, so the generator carries it over unchanged.

**Intake is public by construction.** The forms are on a public repository and the issues they create are public. The form says so above the first field and in a required checkbox. A request that needs a private detail to be understood does not belong in this path.

**The trust rule does not change.** The cockpit shows an item's title only when the item has an area label and its author is the owner, a member, or a collaborator ([cockpit page](doc:eng/cockpit)). A request from anyone else carries the area label the form set and is still counted as untriaged, without its text, for as long as its author stands outside those three relations. The maintainers read it in the issue list on GitHub. The board is unchanged: it shows an issue only when it has a `type:` label, which a maintainer sets.

**What comes later, one decision each.** Stages as labels, so a request can show where it stands. A form on the site itself for people without a GitHub account. A login, which waits for the access model's end state. Each is its own record.

## Consequences

A request to a seat has one shape and one place to go. The seat gets the four things it needs to decide, the cockpit places the item in the seat's area from the first minute, and the seat tab links to the form, so the page that shows the work is also the way to ask for it. The change is small and reversible: six form files, six cards, a test, and one sentence or paragraph in each of three docs pages, with no change to a generator and no new data on the site.

What this does not do. It adds no login, so a request has the identity of its GitHub account and nothing else. It adds no form on the site: asking needs a GitHub account, which leaves out readers who have none, and that gap is the reason for the later form. It does not change the board's columns or the cockpit's contract. It does not stop a stranger from filing a request: the trust rule keeps the stranger's text off the pages, and the maintainers read the rest in the issue list. And it does not make a request a commitment; a seat decides, and says so in the issue.

Checks: `scripts/test_issue_forms.py` reads the six forms and the seats file and fails when a seat has no form, a form has another shape, a label is not one of the cockpit's areas, or a seat tab has no link to its form. It runs by hand for now. A step for it in the script tests job is a change to a workflow file and gets its own pull request.
