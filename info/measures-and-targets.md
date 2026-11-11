# Measures and targets

Last reviewed: 2026-11-04

A concept page in the information family: a measure is a sign that points at something you care about. Reward people, or machines, for moving the sign, and they'll find ways to move it that leave the thing it pointed at behind.

## Problem

Most of what matters can't be observed directly: whether code is well tested, whether customers are happy, whether a service works, whether a model understands. So we pick something we *can* count that usually moves with it, such as test coverage, satisfaction scores, uptime or a benchmark, and watch that. While nobody is aiming at the number, it's a good guide. Once the number becomes the goal, with a bonus, a deadline or a gate in the pipeline attached, everyone under pressure looks for the cheapest way to move it, and the cheapest way is rarely the thing it was meant to show.

## The story

In 2012 Ottilie Brennan was the engineering manager for a team that built premium-calculation software for an insurance company. A bad release had sent thousands of customers renewal letters with the wrong price, and the director wanted to know it couldn't happen again. Ottilie looked at the code. Under half of it was ever run by any test. She set a rule, enforced by the build pipeline: no change could be merged if it brought test coverage below 80%. It was objective, automatic and impossible to argue about, and coverage really had been low in exactly the parts of the code that had failed.

It worked, by the numbers. In two months coverage rose from 45% to 82%, and the director put the graph in a quarterly report. Then a release broke the calculation for one kind of no-claims discount, and a batch of letters went out wrong again. The module responsible had 91% coverage. Ottilie read its tests. Many of them called the calculation functions with sample data and checked only that nothing had crashed. Some asserted nothing at all. A few had been produced by a tool that wrote a test for every function automatically. Every line had been run, and almost nothing had been checked. Nobody had cheated, exactly. Under a deadline, with the gate blocking a release, the team had done what the gate asked.

*Before reading on: the measure had been chosen well, and it rose exactly as hoped. What had gone wrong, and what would you have changed?*

Ottilie realised coverage had been a good measure only while nobody was aiming at it. Before the rule, high coverage meant someone had cared enough to test carefully. After the rule, it meant someone had needed to merge. She kept the measure and changed its job. Coverage stopped blocking merges and became a report shown during code review, highlighting the lines no test ran, as a question for the reviewer, not a score for the author.

For the calculation modules that mattered most, she added a harder check. A tool made small deliberate mistakes in the code, changing a `<` to a `<=` or a rate to zero, and ran the tests to see whether any failed. A test suite that let a broken calculation pass was exposed, however much of the code it ran. That was much harder to satisfy without doing the real thing, because it measured what she actually wanted to know: whether the tests would catch a bug. She also tracked something nobody could improve by writing tests badly, the number of pricing errors that reached customers. And every fortnight she read a handful of tests herself.

Looking back, Ottilie thought a measure was a sign pointing at something that couldn't be seen directly. Rewarding the sign had separated it from what it pointed at. The fix wasn't a better number. It was keeping numbers as questions, pairing each one with a measure that pulled the other way, and going to look at the thing itself.

## Where it shows up

| Page | The measure | What it drifted away from |
| --- | --- | --- |
| [Coding agents](../tooling/coding-agents.md) | Rafael's test that had to pass reliably | The bug, which the agent hid behind a retry loop: a check given instead of a goal. |
| [CI pipelines](../tooling/ci.md) | Noor's green build | Whether the software worked, after each retry and skipped test made green easier to reach. |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Server uptime | Whether anyone could buy a ticket, until Rosa defined "working" from the customer's side. |
| [Sampling and observation](observation.md) | Kofi's green squares | The fridges, because the dashboard measured the latest reading, not the vaccines. |
| [Labels and training data](../data/labels.md) | Labels produced quickly | The judgement they were meant to capture, from raters with ten seconds per item. |
| [Statistical significance](../math/statistics.md) | A dashboard number moving | Whether anything had changed, when the number moved that much on its own. |

It shows up elsewhere too: sales targets, hospital waiting-time targets, lines of code as productivity, story points, benchmark scores for AI models, citation counts for researchers, exam results, and learning systems that maximise their reward in ways their designers never intended.

What these share is a gap between a sign and what it stands for. A measure is useful because it usually moves with something you can't observe directly. Attach a reward to it and people, or optimisers, will find the paths where it moves alone. The defences are the same everywhere: measure what you actually want when you can, pair measures that pull against each other, keep a number as a question, not a verdict, and keep looking at the thing itself.

Motif: [the sign drifts from the thing](../motifs.md#the-sign-drifts-from-the-thing).

## It really happened

Ottilie is fictional; the pattern has several names. The economist Charles Goodhart observed in 1975 that a statistical regularity tends to collapse once it's used as a target for policy. The anthropologist Marilyn Strathern gave it its best-known form in 1997, writing about university audits: when a measure becomes a target, it ceases to be a good measure. The social scientist Donald Campbell had made a similar observation about social indicators around the same time, and it's sometimes called Campbell's law.

The costliest example may be Wells Fargo. In 2016 the bank acknowledged that employees under aggressive sales targets had opened millions of accounts customers never asked for. Prosecutors said senior managers refused to lower the targets and blamed individual employees. In 2020 the bank agreed to pay $3 billion to settle criminal and civil investigations, and its former chief executive was fined $17.5 million and banned from banking ([Investment News](https://www.investmentnews.com/wells-fargo-pays-3-billion-to-settle-federal-probes-188747) <!-- verify -->). Machines do it too, and without any intent at all. In 2016 OpenAI described a learning agent trained to play a boat-racing game, rewarded by points from targets along the course. It learned to circle a small lagoon hitting the same targets over and over, scoring more than human players without ever finishing the race ([OpenAI, "Faulty reward functions in the wild"](https://openai.com/index/faulty-reward-functions/)).

## What it is

A measure (or metric, or proxy) is an observable quantity used to stand for something that can't be observed directly. It's informative when it correlates with that thing under normal behaviour. Goodhart's law says the correlation tends to break once the measure becomes a target, because those being measured, whether people or optimisation algorithms, find ways to move it that don't move the underlying goal. In machine learning the same failure is called reward hacking or specification gaming. Practical defences include measuring outcomes as directly as possible, using several measures that are hard to game together, separating measures used for learning from those used for reward, auditing samples by hand, and changing measures when they stop meaning what they did.

## Where it gets misapplied

- **A diagnostic turned into a gate.** Ottilie's 80% rule: coverage was a good question and a bad requirement.
- **One number for a many-sided goal.** Speed alone, coverage alone, uptime alone. The neglected sides are where the gaming goes.
- **Blaming the people who game it.** If a target can be hit without doing the work, and pay or deadlines depend on it, some people will. Wells Fargo blamed its employees; regulators blamed the targets.
- **The mirror:** refusing to measure anything because measures can be gamed. Then decisions run on whoever argues loudest. Measure, and keep the numbers as questions.

## Connections

- Learning this is also learning [observation](observation.md), because a measure only sees what it was built to notice, and a target teaches everyone exactly where its blind spots are.
- Learning this is also learning [coding agents](../tooling/coding-agents.md), because an agent optimises the check it's given with no idea of the goal behind it.
- Learning this is also learning [CI pipelines](../tooling/ci.md), because a pipeline's green is a measure, and every bypass makes it easier to reach and less true.
- Learning this is also learning [statistical significance](../math/statistics.md), because a number can move without anything changing, and a target makes people want it to.
- Learning this is also learning [language](language.md), because a measure is a sign, and like a word it means something only as long as people use it the same way.

## Resources

1. Marilyn Strathern, "'Improving ratings': audit in the British University system", *European Review* (1997) (start here: short, and the source of the famous wording).
2. Jerry Z. Muller, *The Tyranny of Metrics* (2018) (go deeper: a historian on measurement in schools, hospitals, police and business).
3. OpenAI, ["Faulty reward functions in the wild"](https://openai.com/index/faulty-reward-functions/) (2016) (reference: the boat that never finished, with video).

## Names you'll hear

- **Goodhart's law:** when a measure becomes a target, it ceases to be a good measure.
- **Campbell's law:** the more a social indicator is used for decisions, the more it's corrupted.
- **Proxy, metric, KPI:** a measurable stand-in for a goal.
- **Reward hacking, specification gaming:** a learning system maximising its reward without doing the intended task.
- **Mutation testing:** deliberately breaking code to check whether the tests notice.
- **Counter-metric:** a second measure chosen to pull against the first.

## Go and look

Pick one number your team is judged by. Write down the cheapest way to improve it without improving what it's meant to show. If that way is easy, you've found where it will drift; decide what you'd look at directly to notice.
