# Heaps and priority queues

Last reviewed: 2026-11-12

A concept page: a structure that always knows which item is most urgent, and can take it away or add a new one cheaply, without keeping everything in order. It's behind timers, schedulers, shortest-path searches and every "top ten" list worth computing.

## Problem

Many systems keep asking one question: what's next? The timer due soonest, the most urgent job, the nearest unexplored junction, the biggest spender so far. Scanning everything each time is slow when there are many items. Keeping everything sorted makes the question instant but every insertion slow. What's needed is a structure that's only as ordered as it has to be: it knows the top item for certain and is vague about the rest.

## The story

In 2013 Sigrid Nyström worked on the servers for a messaging app in Stockholm. Each phone held a connection open to the servers, and every connection needed a timer: if a phone went quiet for ninety seconds, assume it had lost signal and close the connection. Her first version kept the timers in a list and, ten times a second, went through the list to see which had run out. With a few thousand connections it was invisible. At three hundred thousand per server, checking every timer ten times a second was most of what the processor did.

She kept the timers sorted by due time instead, so the soonest was always first and checking took no time at all. But now adding a timer meant finding its place in the sorted list, and every message a phone sent pushed its connection's timer back, so the list was being reordered tens of thousands of times a second. The cost had moved from checking to inserting.

Then she found the structure designed for exactly this, a *heap*. It's a tree, stored compactly in an array, with one rule: every item is due no later than the items below it. That rule doesn't put everything in order. It only guarantees that the soonest is at the top. Adding a timer meant putting it at the bottom and letting it rise past anything due later than itself, a few steps for a heap of three hundred thousand. Taking the top meant moving the last item into its place and letting it sink. Both took about twenty steps. Processor use dropped to almost nothing.

Three weeks later a server ran out of memory. The heap held forty million timers for three hundred thousand connections. Sigrid had handled a phone's activity the easy way: add a new timer for ninety seconds later and leave the old one where it was, because finding and removing an item in the middle of a heap was awkward. When an old timer reached the top, the server noticed the connection had newer activity and ignored it. That was correct. But a busy phone sending a message every few seconds left a trail of dead timers behind it, each one waiting ninety seconds to reach the top and be thrown away.

*Before reading on: the heap answered "what's next?" perfectly, and filled up with answers nobody wanted. What would you have changed?*

Sigrid looked at which operations actually happened, and how often. Pushing a timer back happened all the time. Timers actually firing were rare, since most phones stayed active. And nobody needed a timer to fire at an exact millisecond; within a second was fine. She replaced the heap with a *timing wheel*: a ring of ninety slots, one per second, each holding the timers due in that second. Pushing a timer back meant moving it from one slot to another, which took a constant number of steps however many timers there were, and it was removed from its old slot at once, so nothing piled up. Every second, the wheel moved on one slot and closed whatever connections were left in it.

She kept the heap for the job it was best at. The server's other timers were few, varied in length from milliseconds to days, and had to fire precisely: retries, daily clean-up, certificate renewals. A heap handled those well.

Looking back, Sigrid thought each structure she'd tried had been fast at something. The list was fast to add to, the sorted list fast to read from, the heap balanced the two, and the wheel was fast at the operation her servers did most. The question had never been which structure was best. It was which operations happened, how often, and how precise they needed to be.

![A heap of timers drawn two ways: as a tree, with the soonest-due timer at the top and every timer due no later than the ones below it, and as the array it's actually stored in, with arrows showing that each item's children sit at twice its position and one more.](../images/figures/dsa-heaps.svg)

*A heap knows its top item for certain and the rest only roughly, which is exactly enough to answer "what's next?".*

## Where it shows up

| Page | What's most urgent | What the heap made cheap |
| --- | --- | --- |
| [Sorting](sorting.md) | Margit's hundred biggest customers | One pass through two million, keeping a heap of a hundred, instead of sorting them all. |
| [Queues](queues.md) | Yusuf's interactive jobs ahead of long ones | Serving by priority instead of by arrival, which a priority queue does directly. |
| [Graphs](graphs.md) | The nearest junction not yet explored | Dijkstra's algorithm takes it from a priority queue at every step. |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | The next job to give the processor | A scheduler choosing who runs, many times a second. |
| [Event loops and threads](../runtimes/event-loops-and-threads.md) | The next timer an event loop must fire | Every event loop keeps its timers in a structure like Sigrid's. |

It shows up elsewhere too: hospital triage, operating-system schedulers, network routers prioritising traffic, simulations processing the next event in time order, merging many sorted files at once, and leaderboards showing the top ten of millions.

What these share is a question asked over and over: what's most urgent now? A heap answers it without ordering everything, and the right choice between a heap, a wheel or a sorted list depends on which operations happen most and how precise they need to be.

## It really happened

Sigrid is fictional. J. W. J. Williams introduced the binary heap in 1964, in the same short paper as heapsort, and it has been the standard priority queue ever since. In 1987 George Varghese and Tony Lauck described *timing wheels* for operating systems with very many timers, showing how to start and stop each one in constant time when timers don't need exact precision.

Apache Kafka, the widely used messaging system, met Sigrid's problem at much larger scale. It kept requests that were waiting for something to happen, with a timeout, in a "purgatory" that used Java's priority-queue-based delay queue. Completed requests weren't removed from the timer queue straight away, only when they reached the front, so the queue could fill with requests that were already finished. The redesign moved to hierarchical timing wheels, which insert and remove in constant time, and removed completed requests immediately ([Confluent, "Apache Kafka, Purgatory, and Hierarchical Timing Wheels"](https://www.confluent.io/blog/apache-kafka-purgatory-hierarchical-timing-wheels/)).

## What it is

A binary heap is a complete binary tree stored in an array, where every parent is ordered before its children (the smallest at the top for a min-heap). Finding the top item takes one step; inserting an item or removing the top takes a number of steps that grows with the logarithm of the size, by letting an item rise or sink until the rule holds again. It's the usual implementation of a priority queue. Removing or changing an item in the middle needs extra bookkeeping. Alternatives suit other patterns: sorted structures when the whole order is needed, timing wheels when there are many timers that change often and need only coarse precision.

## Where it gets misapplied

- **Leaving cancelled items in the heap.** Sigrid's forty million dead timers, and Kafka's purgatory.
- **Sorting everything to find the top few.** A heap of the size you need does it in one pass.
- **Using a heap where coarse buckets would do.** If "within a second" is good enough, a timing wheel is simpler and faster.
- **The mirror:** a heap for a handful of items. With ten timers, scanning a list is faster and easier to read.

## Connections

- Learning this is also learning [queues](queues.md), because a priority queue is a queue that serves by importance instead of by arrival, and a heap is how it's usually built.
- Learning this is also learning [sorting](sorting.md), because heapsort is a heap emptied in order, and the top-hundred list is a heap that never grows.
- Learning this is also learning [graphs](graphs.md), because Dijkstra's algorithm is a heap of junctions ordered by distance.
- Learning this is also learning [event loops and threads](../runtimes/event-loops-and-threads.md), because every event loop has to know which timer fires next.
- Learning this is also learning [growth](growth.md), because the heap's logarithmic steps are what make three hundred thousand timers cost about twenty steps each.

## Resources

1. [VisuAlgo, binary heap](https://visualgo.net/en/heap) (start here: insert and remove, and watch items rise and sink). <!-- verify -->
2. Confluent, ["Apache Kafka, Purgatory, and Hierarchical Timing Wheels"](https://www.confluent.io/blog/apache-kafka-purgatory-hierarchical-timing-wheels/) (go deeper: Sigrid's problem in a real system).
3. George Varghese and Tony Lauck, "Hashed and Hierarchical Timing Wheels" (1987) (reference).

## Names you'll hear

- **Binary heap, min-heap, max-heap:** the standard heap, with the smallest or largest at the top.
- **Priority queue:** a queue that always gives you the most important item next.
- **Sift up, sift down:** letting an item rise or sink until the heap rule holds.
- **Timing wheel:** a ring of time slots for many coarse timers.
- **Top-k:** finding the k largest items, usually with a heap of size k.

## Go and look

Find out how the language or framework you use stores its timers, or what structure your scheduler uses for delayed jobs. Then check what happens to a timer that's cancelled: is it removed, or left to expire?
