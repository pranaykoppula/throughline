# CI pipelines

Last reviewed: 2026-10-24

A concept page: a machine that builds and tests every change, and the discipline that makes people believe it.

## Problem

Continuous integration only works if the build is trusted: when it's red, something is really broken, and when it's green, it's safe to merge. Builds get slow and tests get flaky, and once people learn that red often means nothing, they stop looking, and the build stops protecting anyone.

## The story

In 2016 Noor Hassan led a team of thirty engineers working on a travel booking platform. Every change ran through the build server: compile, run four thousand tests, report green or red, and nothing merged on red. It had served them well for years.

By that spring the build was red about one run in five, and almost never because of the change being tested. A few dozen tests failed now and then on their own: timing, ordering, a shared test database. Engineers had learned to click "run again". Noor added an automatic retry: any failed test was run up to three times, and only failed the build if it failed all three. The red builds vanished. It was a sensible fix for a real annoyance, and the team thanked her.

Four months later, a bug in how bookings were saved under load reached production and double-charged a few hundred customers. Afterwards, Noor found that a test had been catching it for weeks. It failed about a third of the time, because the bug was a real race that only showed up sometimes. The automatic retries had passed it every time. The team had built a machine for ignoring exactly the kind of failure that mattered most.

*Before reading on: flaky tests trained people to ignore the build, and retries hid a real bug. How would you have dealt with flakiness instead?*

Noor removed the blanket retries and treated flakiness as a bug. Every test that failed and then passed on the same code was flagged automatically and logged. A flaky test went into quarantine: it still ran and was still reported, but didn't block merges. It got an owner and a date by which it had to be fixed or deleted. The flaky rate became a number on the team's dashboard, reviewed every week. And when the main build went red for a real reason, fixing it came before any other work, so red kept its meaning. It took a month to work through the backlog, and they found two more real bugs among the "flaky" tests.

Looking back, Noor thought the build had only ever been worth what people believed about it. Each retry or skipped test had made it a little more comfortable and a little less believable, until it said green about something that was broken.

## Where it shows up

| Page | The pipeline | What it enforced |
| --- | --- | --- |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | Sofia's build server testing every merge | Daily integration and required review. "A practice that wasn't in a tool wasn't really a practice." |
| [Migrations](../data/migrations.md) | Shipping each small step safely | Bilal's six steps depended on deploying often and reliably. |
| [Coding agents](coding-agents.md) | The checks an agent works towards | Only as good as the tests: an agent can make a weak test pass without fixing anything. |
| [The cost of reliability](../cost/reliability.md) | Small, easily undone deploys | Prevent more outages than most redundancy. |
| [Code signing](../auth/code-signing.md) | The build system as part of the supply chain | What it produces gets signed and trusted, so it's a target. |

It shows up elsewhere too: deployment pipelines, security scanning, automated formatting, and dependency updates proposed by bots.

What these share is that the pipeline is where a team's rules actually live, and it only works while red means stop.

## It really happened

Noor is fictional; flakiness at scale is well measured. In 2016 Google reported that about 1.5% of all its test runs gave a flaky result, and that almost 16% of its tests showed some flakiness, a test passing and failing on identical code ([Google Testing Blog, "Flaky Tests at Google and How We Mitigate Them"](https://testing.googleblog.com/2016/05/)). Martin Fowler's article on continuous integration describes the practices Noor went back to: build every change, keep the build fast, and fix a broken build immediately ([Fowler](https://martinfowler.com/articles/continuousIntegration.html) <!-- verify -->).

## What it is

Continuous integration means merging changes into a shared line often, with an automated pipeline that builds and tests each one. Its value depends on trust. The pipeline must be fast enough that people wait for it, reliable enough that red means broken, and strict enough that red blocks merging. Flaky tests are bugs, in the test or in the code, to be tracked, quarantined and fixed, not retried away.

## Where it gets misapplied

- **Automatic retries.** Noor's fix: the build goes green, and so do real intermittent bugs.
- **A slow build.** If it takes an hour, people batch changes, merge without waiting, or stop running it.
- **Skipping tests to get green.** Each skipped test is a promise the build no longer keeps.
- **The mirror:** a pipeline so strict and slow that nothing ships. Checks should be proportionate to the risk.

## Connections

- Learning this is also learning [statistical significance](../math/statistics.md), because a test that fails a third of the time is a noisy measurement, and deciding whether a failure is real is a statistics question.
- Learning this is also learning [event loops and threads](../runtimes/event-loops-and-threads.md), because many flaky tests are race conditions, in the test or in the code.
- Learning this is also learning [build systems and package managers](build-systems.md), because a fast pipeline depends on rebuilding only what changed.
- Learning this is also learning [code signing](../auth/code-signing.md), because the pipeline's output is what gets signed and shipped.
- Learning this is also learning [coding agents](coding-agents.md), because agents optimise for the pipeline's checks, so the checks had better be right.

## Resources

1. Martin Fowler, ["Continuous Integration"](https://martinfowler.com/articles/continuousIntegration.html) (start here). <!-- verify -->
2. John Micco, "Flaky Tests at Google and How We Mitigate Them" ([Google Testing Blog, 2016](https://testing.googleblog.com/2016/05/)) (go deeper).
3. Titus Winters, Tom Manshreck and Hyrum Wright, [*Software Engineering at Google*](https://abseil.io/resources/swe-book), the chapters on testing and continuous integration (reference). <!-- verify -->

## Names you'll hear

- **CI, CD:** continuous integration, and continuous delivery or deployment.
- **Pipeline:** the sequence of automated steps a change goes through.
- **Flaky test:** one that passes and fails on the same code.
- **Quarantine:** running a flaky test without letting it block merges, while it's fixed.
- **Trunk:** the shared main line everyone merges into.

## Go and look

Find out how often your team's main build is red, and how often a red build passes on a plain re-run. The second number is how much your build is trusted.
