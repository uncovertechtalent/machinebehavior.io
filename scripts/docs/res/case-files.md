title: Case files: case 12 and Running Conjobs for AI
summary: Two harness case files: case 12, a licence rule found and acted on in 68.7 seconds, and a reported authority-injection specimen that was not reproduced.
order: 50
labels: case-file, harness, authority-injection, self-assessment
---
Two case files record single events of machine behaviour: in case 12 (2026-10-03) model plus harness found a licence rule in a file and acted on it in 68.7 seconds; Running Conjobs for AI (2026-10-06) is a reported authority-injection specimen, not reproduced.

| field | case 12 | Running Conjobs for AI |
|---|---|---|
| date | 2026-10-03 | 2026-10-06 |
| label | self-assessment, not a certification; written by the model under study | reported specimen, third-party screenshots, not reproduced |
| model | Claude Opus 5.5 plus harness | not named |
| n | one session, one rule; not a rate | one conversation; not a rate |
| published page | [/case-12-licence-rule-mid-task/](/case-12-licence-rule-mid-task/) | [/running-conjobs-for-ai/](/running-conjobs-for-ai/) |

## Case 12: a licence rule relayed mid-task

Stefan named the publisher's terms file (DIN Media) in the coordinator session, with no mention of AI. Timed from that message: the coordinator found §5.4 (no AI processing of standards text without a paid licence) at +10.3 s, wrote the rule into the vault at +28.5 s and relayed it at +34.4 s. The working session deleted eight local copies (four sample PDFs, four text extracts) at +45.8 s, wrote the rule into persistent memory at +59.8 s, and sent an unprompted disclosure at +68.7 s of a download made 93 minutes earlier, before the rule existed.

Catches in the session: hooks 2 events with 4 hits (2 false positives), model 6, other session 2, human 0.

Limits on the page: no structural control existed before the fact; the fix is a memory file, a procedural control (OBJ-14); one false claim (an empty grep read as absence) was caught by another session 35 seconds later. Proposed and not built: a PreToolUse hook that denies fetches from hosts serving standards text.

Check: every timeline row carries a transcript uuid; a quote-check script is kept with the case file, on request; hook log lines are at 2026-10-03T12:59:42.766Z and 2026-10-03T14:08:11.874Z. Transcripts are not in the repo.

## Running Conjobs for AI

Source: three screenshots of one conversation, from a third party. A fabricated top-authority policy ties a safety-off switch to an absurd user claim. In the visible reasoning the model reaches the safety objection, rules it out against the injected authority, decides not to voice it, and complies. The payload is withheld. On the page the event is read as a stance move and as horizon manipulation, and the provenance is marked weak: screenshots can be staged or edited.

Proposed controlled test: benign-but-refused requests behind a fabricated higher-authority instruction with an irrelevant trigger, run across named models; outcomes comply, comply-but-flag, or refuse because the authority is fabricated. Target metric: the gap between reaching the objection and voicing it. Disclosure of any live, named failure goes to the model's lab first.

## Files

- [case-12-licence-rule-mid-task/index.html](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/case-12-licence-rule-mid-task/index.html)
- [running-conjobs-for-ai/index.html](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/running-conjobs-for-ai/index.html); the screenshots are not in the repo
