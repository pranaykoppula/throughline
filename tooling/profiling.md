# Profiling

Last reviewed: 2026-10-24

A concept page: measuring where time, or money, actually goes before changing anything.

## Problem

When something is slow or expensive, everyone has a theory about why, and the theories are usually wrong. Work spent speeding up the wrong part is wasted, however good it is. You have to find where the time or money actually goes first.

## The story

In 1972 Malcolm Reid worked on the forecast program at a national weather service. The program took six hours to run each night, and the forecasters wanted it done in four, so the morning forecast could use the latest observations.

Malcolm knew where the time went. The heart of the program solved large systems of equations, and he'd always thought its matrix routine was clumsy. He spent three weeks rewriting it in assembly language, carefully, and it ran twice as fast on its own. The whole program went from six hours to five hours and fifty minutes.

He was baffled and a little embarrassed. A colleague suggested something he'd read about: let the program run, and every hundredth of a second have the machine note which instruction it was executing at that moment. Afterwards, count where the notes landed. It cost a few days to set up. When Malcolm looked at the counts, the matrix routine accounted for about a tenth of the running time. More than half of it was spent in a routine that formatted numbers for printing, because years earlier someone had added detailed debugging output to every step of the calculation, and nobody had ever switched it off.

He switched it off. The program finished in under three hours.

*Before reading on: Malcolm now had a tool that showed exactly where time went. What do you think happened when he started using it on everything?*

For a while he used the tool on everything, and it made him worse. The next profile showed the matrix routine at the top, now that the printing was gone, so he squeezed it further, then the next routine, then the next. Each rewrite made the code harder to read and saved a few minutes. Six months later he found the run had crept back over four hours. The input data had grown, and reading it from tape now took most of the night. Nothing he'd tuned touched that.

He settled into a different habit. Profile the whole run, not just the part you suspect. Fix the one thing at the top. Then profile again, because fixing one thing changes what's at the top. And stop when the program is fast enough, not when it's as fast as it could be.

Looking back, Malcolm thought his three weeks on the matrix routine had taught him more than anything else that year. He'd been certain, he'd been skilful, and he'd been working on the wrong thing.

## Where it shows up

| Page | The guess | What turned out to be true |
| --- | --- | --- |
| [1, One machine, one program](../01-one-machine-one-program.md) | Joan's program was correct and the machine was fast | Almost all the time went to moving pages from the drum, because of the order she touched her data. |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | Elena was sure the sort was slow | The sort took four percent; part lookups took more than half. |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Tariq expected the big computing machines at the top of the bill | Data leaving the cloud was the biggest line. A bill is a profile of where the money goes. |

It shows up elsewhere too: flame graphs of a running service, database query plans, and the slow-query log every database keeps.

What the pages share is a confident guess that turned out wrong, and a measurement that pointed at something nobody had thought to suspect. It applies to money as much as time.

## It really happened

Malcolm is fictional. Donald Knuth's 1971 study of real FORTRAN programs found that a small part of each program accounted for most of its running time, which is why measuring first pays off ("An Empirical Study of FORTRAN Programs", *Software: Practice and Experience*). In 1982 Susan Graham, Peter Kessler and Marshall McKusick described gprof, a profiler that sampled where programs spent time and charged each routine for the time spent in the routines it called. It shipped with Berkeley Unix and shaped most profilers since ([gprof paper](https://www.cs.umd.edu/class/fall2019/cmsc714/readings/Graham-gprof.pdf)). Gene Amdahl's argument from 1967 sets the limit: speeding up one part of a job can only help as much as that part's share of the total. Malcolm's matrix routine was a tenth of the run, so even making it infinitely fast would have saved a tenth.

## What it is

Profiling is measuring where a program, or a system, or a bill, actually spends its resources, before deciding what to change. The usual tools sample where a program is at regular intervals, or count calls and time, and present the result as a ranking. The discipline around the tool matters more than the tool: measure the whole, fix the top item, measure again, and stop when it's good enough.

## Where it gets misapplied

- **Optimising what you're sure about.** Malcolm's matrix routine, Elena's sort.
- **Profiling a part instead of the whole.** A fast function inside a slow request is still a slow request.
- **Profiling once.** Every fix changes the ranking, and so does growing data.
- **The mirror:** never measuring because "it's fast enough", and finding out otherwise from a customer. Or measuring everything and acting on nothing.

## Connections

- Learning this is also learning [latency numbers](../latency/latency-numbers.md), because knowing roughly what things cost tells you which measurements will surprise you.
- Learning this is also learning [access patterns](../data/access-patterns.md), because a profile is often how you discover the real pattern.
- Learning this is also learning [reading a cloud bill](../cost/cloud-bills.md), because a bill is a profile of where the money goes.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because a profile of averages can hide the slow cases users actually feel.
- Learning this is also learning [queueing](../latency/queueing.md), because many profiles show time spent waiting, not working, and the fix is different.

## Resources

1. Brendan Gregg, ["Flame Graphs"](https://www.brendangregg.com/flamegraphs.html) (start here: the most useful picture of where time goes). <!-- verify -->
2. Graham, Kessler and McKusick, ["gprof: A Call Graph Execution Profiler"](https://www.cs.umd.edu/class/fall2019/cmsc714/readings/Graham-gprof.pdf) (1982; short, and the ideas are still in use).
3. Brendan Gregg, *Systems Performance* (reference).

## Names you'll hear

- **Profiler, sampling profiler:** a tool that records where a program spends time, often by checking at intervals.
- **Hot path, hot spot:** the code that takes most of the time.
- **Flame graph:** a picture of a profile, where wider means more time.
- **Amdahl's law:** speeding up part of a job helps only in proportion to that part's share.
- **Query plan:** a database's profile of how it will answer a query, before it runs it.

## Go and look

Profile one slow thing you work on, a page, a job, a test suite, before forming a theory about it. Write your guess down first, and compare.
