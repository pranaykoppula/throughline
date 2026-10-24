# Latency numbers

Last reviewed: 2026-10-24

A concept page: the rough cost of everything, and why the ratios matter more than the numbers.

## Problem

Engineers make dozens of decisions a day that depend on how long things take: read from memory or disk, call another service or compute locally, cache here or there. Without a rough sense of the costs, those decisions are guesses, and the costs differ by factors of a thousand or a million, so bad guesses are very bad.

## The story

In 2015 Daniel Weiss ran the backend for a travel booking app with users in North America and Europe. Prices for hotels came from slow partner systems, so he added a cache. To keep it simple, with one copy and no question of copies disagreeing, he ran it in a single data centre in Virginia, next to the main database. Every server, in both regions, checked that cache first.

American users got noticeably faster. European users complained that search had got *slower*. Daniel didn't believe it until he measured. Before the cache, the European servers had read prices from a local database copy in Ireland: about a millisecond away. Now each lookup crossed the Atlantic to Virginia and back, about eighty milliseconds, and a search page did a dozen lookups one after another. He had added a fast cache and made European searches nearly a second slower.

He sat with a colleague's printed table of rough timings that had been pinned to the wall for years and that he'd never really read. Reading from memory: a tenth of a microsecond. Reading from a fast disk: around a hundred microseconds. A round trip inside one data centre: half a millisecond. A round trip across the Atlantic: eighty milliseconds, set mostly by the speed of light in glass fibre. No amount of engineering would make that last number smaller.

*Before reading on: the cache was fast, and the ocean between it and half the users was not. What would you have done?*

He put a copy of the cache in each region and accepted that the two copies could disagree for a few seconds about a hotel price, which the booking step checked anyway. He also changed the search page to ask for all twelve prices at once instead of one after another, so even a slow lookup cost one round trip, not twelve. European searches dropped below their old times. He kept the table on his own wall after that.

Looking back, Daniel thought the table had taught him to ask one question before any design: where is the data, and how far is that from where it's needed? The exact numbers changed every few years. The ratios between them, a thousand times here, a million there, barely did.

## Where it shows up

| Page | The gap | What it decided |
| --- | --- | --- |
| [1, One machine, one program](../01-one-machine-one-program.md) | Core memory against the drum: about a thousand times | Joan's program spent all night fetching pages because of the order she touched her data. |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | The processor against tape drives and printers | Ruth's machine was idle four-fifths of the time, waiting. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | A round trip across a continent | Lin's transfer cost was set by the number of round trips, not the size of the data. |
| [Profiling](../tooling/profiling.md) | Any of them | Knowing the rough costs tells you which measurements will surprise you. |

It shows up elsewhere too: in every choice between calling a service and computing locally, in database query plans, and in the gap between a phone on wifi and the same phone on a weak mobile signal.

What the pages share is one picture repeated at every scale: a little fast storage close by, a lot of slow storage far away, and the cost of anything set by which one you have to reach.

## It really happened

Daniel is fictional; his table is real and widely copied. Peter Norvig published a version in his essay "Teach Yourself Programming in Ten Years", and Jeff Dean of Google popularised another in talks around 2009; it circulates as "Latency numbers every programmer should know" ([one copy](https://gist.github.com/jboner/2841832) <!-- verify -->). The numbers have changed with hardware, as disks became solid-state and networks got faster, but light in fibre still covers only about two hundred kilometres per millisecond. Grace Hopper used to hand audiences pieces of wire about thirty centimetres long, the distance light travels in a nanosecond, to show why distance limits computers.

## What it is

Latency numbers are rough, order-of-magnitude costs for common operations: reading from a processor cache, from memory, from disk, and making network round trips at different distances. Their value is in the ratios. Memory is about a thousand times faster than a fast disk, which is hundreds of times faster than a cross-continent round trip. Use them to estimate before building, and to recognise when a measurement doesn't make sense.

## Where it gets misapplied

- **Treating the numbers as exact.** They're rough and they date. Use them for orders of magnitude, then measure.
- **Optimising the cheap part.** Saving microseconds of computation inside a request that makes a dozen sequential network calls.
- **Forgetting the speed of light.** One copy of anything, used from everywhere, is slow for whoever is far from it.
- **The mirror:** spreading copies everywhere to save milliseconds nobody notices. Each copy is a [consistency](../data/consistency.md) problem.

## Connections

- Learning this is also learning [round trips](round-trips.md), because the network rows of the table are where most real latency comes from.
- Learning this is also learning [caching](caching.md), because a cache only helps if it's nearer, in this table's terms, than the original.
- Learning this is also learning [storage tiers](../cost/storage-tiers.md), because the fast rows of the table are also the expensive ones.
- Learning this is also learning [arrays and linked lists](../dsa/arrays-and-linked-lists.md), because the gap between cache and memory is why data kept together is fast.
- Learning this is also learning [profiling](../tooling/profiling.md), because rough numbers tell you what to expect, and measurement tells you what's true.

## Resources

1. ["Latency numbers every programmer should know"](https://gist.github.com/jboner/2841832) (start here: one screen). <!-- verify -->
2. Ilya Grigorik, [*High Performance Browser Networking*](https://hpbn.co/), the chapters on latency (go deeper). <!-- verify -->
3. Peter Norvig, ["Teach Yourself Programming in Ten Years"](https://norvig.com/21-days.html), for his version of the table and the advice around it. <!-- verify -->

## Names you'll hear

- **Latency, bandwidth:** how long one thing takes, and how much can move per second. They're different, and confusing them is common.
- **Round-trip time (RTT):** the time for a message to go and its reply to come back.
- **Order of magnitude:** a factor of ten. Most of these comparisons are several orders.
- **Nanosecond, microsecond, millisecond:** a billionth, a millionth and a thousandth of a second.

## Go and look

Pick one request in something you've built and estimate, from the table, how long it should take. Then measure it. If the two disagree by more than ten times, find out why.
