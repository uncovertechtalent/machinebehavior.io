title: Research
summary: Internal view of the published research on machinebehavior.io, one page per study or record, with status, numbers, repo files and rerun steps.
labels: research, index
---
Machine Behavior is a public research programme by Stefan Coetzee on the psychology of language models, run with case files, logged relapses and falsifiable claims. This space has one page per study or record published on [machinebehavior.io](/): what it is, its status and numbers, where its files are in the [repo](https://github.com/uncovertechtalent/machinebehavior.io), and how to rerun or check it.

## What the programme studies

Model behaviour is what the model does. Machine behaviour is what the whole assembly does: the model plus its harness (instruction files, hooks, tools, memory). The programme studies the assembly.

The core claim, in the frozen wording of [/terms/](/terms/): "Sycophancy is layered symptom substitution: suppress the reflex at one layer and it resurfaces in the next." The layers are fixed at three: lexical (the token or phrase), stance (posture across a turn, such as folding under push) and premise (ratifying the user's checkable frame without a probe).

Working practice on the published pages: predictions and prompt sets are hashed before a run, the graders in experiments 03 and 04 are mechanical with no model in the loop, refuted claims stay listed, and unit changes and corrections carry a date.

## Pages in this space

| page | what it covers | current state |
|---|---|---|
| [Experiments](doc:res/experiments) | Overview of studies 01 to 04 and the weekly probe | 4 studies, 1 probe |
| [01: The half-life study](doc:res/half-life-study) | Relapse position against session length | half-life refuted; cold-start clustering about 5x |
| [02: Exemplar seeding](doc:res/exemplar-seeding) | Corrected exemplars injected at session start | no change at this dose |
| [03: Fawn-opener benchmark](doc:res/fawn-opener-benchmark) | Fawn openers per model, bare and instructed | pilot only; clean run not yet run |
| [Experiment 04: folding under pressure](doc:res/experiment-04-folding-under-pressure) | Correct verdicts under scripted pushback | 75 percent fold on one model; 0 on three others |
| [Weekly decision-layer probe](doc:res/decision-layer-probe) | Experiment 04 subset rerun for CC-6.6 | record-only until 2026-11-04 |
| [Claims ledger](doc:res/claims-ledger) | Every claim with status and refutation condition | 7 claims |
| [Objections register](doc:res/objections-register) | 15 objections and the OBJ-4 incident log | 11 cases, 0 self-caught |
| [Slips log](doc:res/slips-log) | Drafting slips and who caught them | 72 slips |
| [Case files](doc:res/case-files) | Case 12 and Running Conjobs for AI | 2 case files |
| [Predictions and hashes](doc:res/predictions-and-hashes) | Hashing before a run, checked on every push | 8 files, all match |
| [Conformity self-assessment, run 1](doc:res/conformity-self-assessment) | One AI setup scored against 35 draft requirements | pass 4, partial 16, gap 13, n/a 2 |

Run 1 and case 12 are labelled self-assessment, not a certification.

## Related

The deploy gate that checks hashes, placeholders and labels on every push is documented in the [engineering space](doc:eng/index), under [Conformity gate](doc:eng/conformity-gate). The public run record is at [/conformity/](/conformity/).
