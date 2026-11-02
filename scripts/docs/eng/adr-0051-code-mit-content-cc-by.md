---
title: ADR-0051: The repository's code is under MIT and the site's own text is under CC BY 4.0
summary: The repository had no licence file, which leaves every right reserved by default and made the public claim that the house's work is open source false for this repository. The code is now under the MIT licence in LICENSE; the site's own text, images, and data files are under CC BY 4.0 in LICENSE-CONTENT, with the attribution form named; quotations from other works keep their own rights.
parent: decision-log
order: 51
adr: 51
status: accepted
created: 2026-11-02
labels: adr, decision, licence, repository
owner: Stefan Coetzee
reviewed: 2026-11-02
review_by: 2027-01-31
type: explanation
---
## Context

The repository has been public since 2026-08-07 without a licence file. A public repository with no licence grants no right to copy, change, or redistribute; a reader may look and nothing more. Five of the house's eight public repositories carry the MIT licence (the CTO powersuit, agent-observability, vestige-kit, vault-kit, chain-traveler); this one, tychat.io, and site-infra carried none. A draft post on 2026-11-02 said all of the work is free and open source, and a check of the eight repositories showed that for three of them it was not.

The repository holds two kinds of work. Code: the build scripts, the gate, the crawler, the dashboards' builders, the tests. Content: the research pages, the case files, the articles, the topic pages, the docs, the model-facing text in `llms.txt`, the images, and the data files the pages are built from. The site also carries material that is not the owner's: quotations from papers and articles, cited where they appear, and pages imported from the knowledge vault ([ADR-0009](doc:eng/adr-0009-vault-notes-with-review-label)) that paraphrase standards without reproducing their text ([the standard page](/conformity/standard/) names the rule).

## Decision

**Code under MIT.** The file `LICENSE` at the root holds the MIT licence text with the owner as the copyright holder, the same text and holder as the five sibling repositories. GitHub reads this file and shows the licence on the repository page.

**The site's own content under CC BY 4.0.** The file `LICENSE-CONTENT` holds the Creative Commons Attribution 4.0 International legal code, with a header that names what it covers (the text, images, and data files of the site), the attribution form ("Stefan Coetzee, machinebehavior.io", with a link to the page used), and what it leaves out. A reader may copy, quote at length, translate, or build on a page, for any purpose, with that attribution. A model may read the pages on the same terms; the model-facing text was written to be read that way ([TYChat](https://tychat.io/)).

**What is not relicensed.** Quotations from other works stay under the rights of their authors; the licence covers the owner's words around them. The imported vault pages carry the licence as the owner's paraphrase; the standards they describe are not reproduced on the site and are not licensed by it.

**Where it is stated.** The two files, and a licence section in `README.md`. The page footer is unchanged for now; a footer line is a change to the site chrome on every page and gets its own decision if wanted.

**Siblings.** tychat.io gets the same two files with its own attribution form; site-infra, which holds only code, gets `LICENSE` alone.

## Consequences

The public claim holds: every repository of the house is under a licence that allows reuse. A reader who copies a page knows the terms and the attribution line. GitHub shows two licences on the repository page, MIT and CC BY 4.0, which is the accurate picture. What this does not do: grant rights over third-party quotations, add a visible licence line to every page, or change the terms of the copies of pieces published on other platforms.
