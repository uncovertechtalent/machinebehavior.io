title: Transcriber Incident Register
summary: Every failure of the video transcriber pipeline since February 2026, as typed atoms.
parent: incidents
order: 100
labels: moc, transcriber-incidents
type: moc
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Transcriber Incident Register.md
reviewed: no
---
> Every failure of the video transcriber pipeline since February 2026, as typed atoms. An incident links to its root cause, to what was done about it, and to the test that found the cause. A fix that replaced a wrong fix links to it as superseded. The trap file in the skill folder stays the working copy the agent reads; this register is the same record in a form the graph can walk.

Two terms, fixed: **imported consequences** are the record of what a failure cost, which is what these atoms hold. **Imported experience** is what an agent has once it reads them.

## Incidents

- [[Incident 2026-02-27 Dead Collection Short Links]]
- [[Incident 2026-07 Summaries Inverted Irony]]
- [[Incident 2026-07-14 Backup Missed WAL Writes]]
- [[Incident 2026-07-14 Short Scrape Looked Like a Quiet Feed]]
- [[Incident 2026-07-19 Pending Status on Finished Videos]]
- [[Incident 2026-07-21 Ad Filter Removed Artist Videos]]
- [[Incident 2026-08-08 Empty-Transcript Videos Invisible to Review]]
- [[Incident 2026-08-08 False Enumeration Bug Finding]]
- [[Incident 2026-09-11 Three-Morning Cron Crash]]
- [[Incident 2026-09-13 Ghost Still-Running Job]]
- [[Incident 2026-09-16 Server Cannot List the Collection]]

## Root causes

- [[Expired Bot-Manager Cookie Returns Empty Body]]
- [[File Copy of a WAL-Mode Database Misses Recent Writes]]
- [[Handle-Based Ad Filter Matches Artist Accounts]]
- [[Process Check Matches Its Own Shell]]
- [[Publish Date Treated As Time In Collection]]
- [[Re-Scrape Relinks Processed Rows As Pending]]
- [[Review Tool Lists Only Rows With a Transcript]]
- [[Sensitivity-Gated Posts Vanish From Unauthenticated Listing]]
- [[Short Link Redirects to the Homepage]]
- [[Small Local Model Misreads Ironic Register]]
- [[Swallowed Stderr Hides the Cause]]

## Mitigations

- [[Authenticated Cookie Jar for Gated Posts]]
- [[Back Up SQLite With the Backup Command]]
- [[Bracket Pattern Process Check]]
- [[Compare Videos Found Against the In-App Count]]
- [[Compare Videos Found Run to Run]]
- [[Eliminate Concurrent Saves Before Blaming the Scraper]]
- [[Enumeration Retry With Unauthenticated Fallback]]
- [[Filter Expired Cookies Before Each Run]]
- [[No-Transcript Bucket in the Review Tool]]
- [[Probe Pending Rows Before Calling Them Backlog]]
- [[Pull the Full Row List After Any Scrape]]
- [[Single Video URL As the Collection Argument]]
- [[Summaries Are a Triage Index]]
- [[Verify Transcript Length Never Status]]

## Detection methods

- [[Differential Test in the Same Minutes]]
- [[Hand-Check Output Against the Primary Source]]
- [[Probe the Artifact Before Reasoning From Counts]]

## Related

- [[Blameless Postmortem Discipline]]
- [[the-trap-file/draft|The Trap File Is Longer Than the Instruction File]]
- [[_series-running-the-golem]]

## How to add one

One file per incident, `type: incident`, with `found`, `incident_state` and `cost` in the frontmatter. Link the cause under a heading `Caused by`, the fix under `Mitigated by`, the test under `Detected by`. A replaced fix links to its replacement under `Superseded by`. An incident with no known cause gets no cause link and says so in its text.
