# Statistical significance

Last reviewed: 2026-10-24

A concept page: telling a real difference from noise, before you act on it.

## Problem

Numbers wobble. Two identical versions of a page will show different results on different days purely by chance. When you change something and a number moves, you have to decide whether the change caused it or the wobble did, and people are very good at seeing patterns that aren't there.

## The story

In 2014 Lucas Ferreira ran experiments at an online shoe retailer. The team wanted more people to finish checkout, and a designer suggested a bigger, green "Buy now" button instead of the small grey one. Lucas set up a test: half of visitors saw the old button, half the new.

He checked the results that afternoon. Green was ahead by 9%. He checked again the next morning: still ahead, by 7%. The product manager saw the dashboard, declared victory and asked for the green button to go to everyone. Lucas felt uneasy, and couldn't quite say why, so he shipped it.

Two months later, checkout completion was exactly where it had been before. The finance team asked where the promised 7% had gone.

Lucas went back to the test. It had run for under two days, with a few hundred checkouts on each side. He ran the same test again, but this time with two identical grey buttons, and watched the dashboard for a week. On different days, one grey button "beat" the other by 6%, then 4%, then lost by 5%. The noise was as big as the effect he'd celebrated. And by checking every few hours and stopping as soon as the result looked good, he'd almost guaranteed he would find a winner, whether there was one or not.

*Before reading on: the test had shown a clear winner, and the winner made no difference. What would you have done differently?*

Lucas changed how the team ran tests. Before starting, they decided how big a change was worth detecting and worked out how many visitors that needed. Usually that meant thousands of checkouts and a couple of weeks, covering every day of the week. Nobody stopped a test early because it looked good. They chose one main measure in advance instead of searching twenty for one that moved. And every new kind of test began with an A/A test, two identical versions, to see how big the noise was. Fewer tests "won". The ones that did, stayed won.

Looking back, Lucas thought the dashboard had been honest, and he had read it like a scoreboard. A number moving isn't news until you know how much it moves on its own.

## Where it shows up

| Page | The question | Why it mattered |
| --- | --- | --- |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Is this pattern in the data real? | A model learns whatever patterns are in its data, real or accidental. |
| [Distributions and percentiles](percentiles.md) | What does the spread look like? | You can't judge a difference without knowing the normal variation. |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Is this group's failure rate really different? | Rosa's Brazilian customers were a real signal in a small group; the opposite mistake is chasing noise in a small group. |
| [Profiling](../tooling/profiling.md) | Did this change actually make it faster? | One run proves little; timings wobble too. |

It shows up elsewhere too: performance benchmarks, alert thresholds, fraud detection, and every "this metric went up after we shipped" conversation.

What these share is one discipline: decide in advance what you're measuring and how much data you need, know the size of the noise, and be suspicious of results you were hoping for.

## It really happened

Lucas is fictional; his mistakes are the standard ones. Ronny Kohavi, who ran large experimentation programmes at Microsoft, Amazon and Airbnb, has written that most ideas tested don't improve the metrics they aim at, and that surprising results usually turn out to be errors. That's why his teams treat results that look too good with extra suspicion. They are sometimes real. At Bing, a small change to how ad headlines were displayed set off an alarm because revenue was suspiciously high, and repeated testing showed it really did lift revenue by about 12% ([Kohavi and Thomke, "The Surprising Power of Online Experiments", *HBR*, 2017](https://web-docs.stern.nyu.edu/executive/The%20Surprising%20Power%20of%20Online%20Experiments.pdf)). The difference between Lucas's button and Bing's headline was replication.

## What it is

Statistical significance is a way of asking how likely a difference this large would be if there were no real effect at all. A significant result is unlikely to be pure chance. It isn't proof, and it says nothing about whether the effect is large enough to matter. Valid tests fix their sample size and measures in advance, don't stop early when results look good, account for testing many things at once, and are repeated when the stakes are high.

## Where it gets misapplied

- **Peeking and stopping early.** Lucas's two days: checking repeatedly and stopping at a good moment manufactures winners.
- **Testing many metrics and reporting the one that moved.** With enough measures, something always moves by chance.
- **Significant but trivial.** With huge samples, tiny effects become "significant" and still don't matter.
- **The mirror:** refusing to act on anything without a perfect experiment. Some decisions are cheap to reverse and fine to make on judgement.

## Connections

- Learning this is also learning [distributions and percentiles](percentiles.md), because significance is about whether two distributions really differ.
- Learning this is also learning [labels and training data](../data/labels.md), because a model trained on noise learns noise.
- Learning this is also learning [profiling](../tooling/profiling.md), because a benchmark run once is an anecdote.
- Learning this is also learning [access patterns](../data/access-patterns.md), because deciding what's typical usage is a statistics question.
- Learning this is also learning [the cost of reliability](../cost/reliability.md), because judging whether a change made things more reliable needs enough incidents to compare.

## Resources

1. Ron Kohavi, Diane Tang and Ya Xu, *Trustworthy Online Controlled Experiments* (2020) (start here).
2. Evan Miller, "How Not To Run an A/B Test" (go deeper: short, on the peeking problem).
3. Any introductory statistics text, for hypothesis testing and confidence intervals (reference).

## Names you'll hear

- **A/B test, A/A test:** comparing two versions, and comparing two identical versions to measure noise.
- **p-value:** how likely a result this extreme would be if nothing were really different.
- **Statistical power, sample size:** how likely a test is to detect a real effect, and how much data that takes.
- **Multiple comparisons:** testing many things and finding something by chance.
- **Twyman's law:** any figure that looks interesting or different is usually wrong.

## Go and look

Find a number on a dashboard you watch and look at how much it varies week to week when nothing has changed. That's the size of the noise any claimed improvement has to beat.
