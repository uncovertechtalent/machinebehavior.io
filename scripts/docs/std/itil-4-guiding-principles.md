title: ITIL 4 Guiding Principles
summary: Seven universal recommendations that guide decisions and actions across the Service Value System.
parent: itil
order: 100
labels: itil, itil-concept
aliases: ITIL 4 Guiding Principles | ITIL Seven Principles | ITIL Guiding Principles
type: itil-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/itil/ITIL 4 Guiding Principles.md
reviewed: no
---
> Seven universal recommendations that guide decisions and actions across the Service Value System. Originally introduced in ITIL Practitioner (2016), made central to ITIL 4. Designed to be durable across changing context and reusable beyond IT service management.

## The seven principles

### 1. Focus on value

Everything the organization does should link, directly or indirectly, to value for stakeholders.

What it means in practice:

- Identify who the consumer is for any work and what they value
- Identify the experience consumers have (UX) and the experience they should have
- Articulate value in stakeholder-meaningful terms (outcomes, not outputs)
- Be willing to stop work that does not contribute to value

Common failure mode: activity equated with value. Running a meeting, producing a report, completing a ticket can feel like value-creation but may produce none.

### 2. Start where you are

Do not start from scratch when building or improving services. Assess what exists and build on it.

What it means in practice:

- Measure current state directly; do not assume
- Reuse and improve existing capability rather than replacing it
- Avoid the rebuild-everything bias that often accompanies new framework adoption
- Distinguish what is working from what is not; protect the working

Common failure mode: consultant-led transformations that discard institutional knowledge and rebuild from scratch, losing the working pieces.

### 3. Progress iteratively with feedback

Work in small steps, each producing observable results. Feed back into the next step.

What it means in practice:

- Slice work into the smallest useful units
- Make each unit produce visible output
- Build feedback loops into the work itself
- Adjust based on feedback rather than persisting with original plans against contrary evidence

Borrowed heavily from Lean and Agile. Compatible with both iterative-design methods (Agile sprints) and continuous-flow methods (Kanban, DevOps continuous delivery).

### 4. Collaborate and promote visibility

Work together across silos. Make work visible.

What it means in practice:

- Cross-functional collaboration on decisions
- Transparent decision-making, visible work-in-progress
- Avoid surprises through proactive communication
- Recognize that knowledge withholding (deliberate or accidental) is dysfunctional

The "promote visibility" part is partly a counter to ITIL's historical reputation for opaque process-heavy operations. Visibility is meant to be a default, not an exception.

### 5. Think and work holistically

No service or service component stands alone. Consider the whole system.

What it means in practice:

- Use the four dimensions to check that decisions are not single-dimension only
- Consider downstream and upstream effects of changes
- Avoid local optimization that creates global problems
- Use systems thinking explicitly

Connects directly to the four-dimensions model. A decision that improves a process but degrades culture is a local optimization with negative system effect.

### 6. Keep it simple and practical

Use the minimum number of steps. Cut anything that does not add value or contribute to outcome.

What it means in practice:

- Minimum viable process — fewest steps that work
- Eliminate ceremony, redundant documentation, unnecessary approvals
- Prefer practical over theoretical
- Resist complexity creep

The principle most at risk of being violated in ITIL implementations. Process growth is gradual; cutting accumulated complexity is difficult.

### 7. Optimize and automate

Use resources of all types as effectively as possible. Eliminate manual work where machines can do it.

What it means in practice:

- Optimize the process before automating it (automating a broken process makes the broken faster)
- Use automation to remove toil and free human capacity for judgment-requiring work
- Apply emerging technologies (AI, ML) where they add value
- Continuously look for further optimization and automation opportunities

The principle that opens the door to AI-tool adoption in service management. ITIL 4 does not prescribe specific automation; it makes automation expected.

## How the principles work together

The principles are designed to be applied jointly:

- **Focus on value** + **Start where you are** + **Progress iteratively** = direct work toward stakeholder value via small evidence-based steps from current state.
- **Collaborate and promote visibility** + **Think and work holistically** = make work visible across the system so that cross-cutting effects are seen.
- **Keep it simple and practical** + **Optimize and automate** = minimum viable process, then automate what remains.

In tension, principles can pull in different directions. Example: "Start where you are" can conflict with "Keep it simple and practical" if the current state is overly complex. The principles guide judgment; they don't replace it.

## Where the principles came from

ITIL Practitioner (2016) introduced nine guiding principles. ITIL 4 (2019) consolidated to seven by merging and removing:

- Removed: Be Transparent (subsumed into Collaborate and Promote Visibility)
- Removed: Design for Experience (subsumed into Focus on Value)
- Merged: Various principle pairs combined

The principles drew on broader management thinking: Lean (Eliminate Waste, Build Quality In), Agile (Inspect and Adapt, Working Software over Documentation), Systems Thinking (Think Holistically), DevOps (Three Ways: Flow, Feedback, Continuous Learning).

The principles' durability outside ITIL is a feature: they read as general operating-model recommendations, not IT-specific advice.

## Applying the principles to a decision

ITIL guidance recommends running decisions through the seven principles:

1. Does this **focus on value**? Whose value, by what measure?
2. Are we **starting where we are**? Do we know what currently works?
3. Can we **progress iteratively with feedback**? What is the smallest useful step?
4. Are we **collaborating and promoting visibility**? Who needs to be involved, what needs to be shared?
5. Are we **thinking and working holistically**? What are the system effects?
6. Are we **keeping it simple and practical**? Is there a leaner version?
7. Should we **optimize and automate**? What can machines do?

Decisions that fail multiple principles deserve scrutiny.

## Common implementation gaps

- **Principles as posters.** Printed on walls, ignored in practice. Common in low-maturity adoptions.
- **Cherry-picking principles.** Citing "Keep it simple" to justify cutting needed work; citing "Think holistically" to justify scope creep. The principles work as a set; cherry-picking degrades them.
- **Principle-vs-process tension.** Existing process documents conflict with the principles. ITIL guidance: principles trump process documents in case of conflict — but practitioner culture often inverts this.
- **Confusion with values.** Principles are operating recommendations, not moral values. They tell you how to work, not what to value beyond stakeholder value.

## SRE and AI-agent fit notes

### The principles map well to SRE practice

- **Focus on value** → SRE's customer-defined SLO discipline.
- **Start where you are** → SRE's measurement-first approach (you cannot improve what you do not measure).
- **Progress iteratively with feedback** → SRE's gradual rollout, canary deployments, error budget consumption monitoring.
- **Collaborate and promote visibility** → SRE's blameless postmortems, shared on-call, public dashboards.
- **Think and work holistically** → SRE's reliability-as-system-property framing.
- **Keep it simple and practical** → SRE's bias toward simplicity in architecture and process.
- **Optimize and automate** → SRE's toil-reduction discipline.

The principles serve as bridge vocabulary in cross-discipline conversations.

### The principles for AI-system operations

- **Focus on value** → AI features deliver value when they help consumers; not by existing. Hype-driven AI adoption fails this principle quickly.
- **Start where you are** → existing operational practices for monitoring, incident response, change management need adaptation, not replacement, for AI features.
- **Progress iteratively with feedback** → AI-feature rollouts should be canaried, with monitoring on agent behavior and human-feedback loops to refine.
- **Collaborate and promote visibility** → agent action logs are visibility infrastructure; ai-system reliability requires cross-team collaboration (engineering, security, compliance, support).
- **Think and work holistically** → AI feature behavior touches data, security, customer experience, financial cost (token spend), reliability, brand. All dimensions need consideration.
- **Keep it simple and practical** → resist over-engineering AI agents; the simplest agent that solves the problem is usually right.
- **Optimize and automate** → AI tools enable new automation; opportunities expand, but the principle still requires that automation produce value.

## Stefan-context implementation sketch

- The seven principles serve as a personal decision-checking heuristic. Useful for self-applied work scope decisions and for client engagement scoping.
- "Focus on value" + "Keep it simple and practical" are the load-bearing two for solo / small-team operations — they cut overhead before it accumulates.
- "Start where you are" is the relevant principle when surveying existing vault state, existing skill set, existing client baseline before proposing changes.

## See also

- [[ITIL Cluster|cluster MOC]] · [[ITIL 4 Service Value System]] · [[ITIL 4 Four Dimensions]] · [[ITIL 4 Practices]]
