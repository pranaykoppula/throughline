# Arrays and linked lists

Last reviewed: 2026-10-24

A concept page: the two simplest ways to keep a sequence, and why the one that's worse on paper is often faster in practice.

## Problem

A list of things can be kept side by side in memory, in an array, or scattered, with each item pointing to the next, in a linked list. Textbooks show that linked lists make inserting and removing in the middle cheap, and arrays make it expensive. On real hardware the cost that usually dominates is something the textbook comparison leaves out: where the data sits in memory.

## The story

In 2009 Marta Silva programmed the particle effects for a video game: sparks, smoke and rain, thousands of tiny objects created and destroyed every frame. Each frame, every particle had to be moved, faded and drawn, and dead ones removed. Removing items from the middle of a list was the main operation, so Marta used a linked list. Each particle pointed to the next; removing one meant changing a single pointer, without shifting anything. Her algorithms course had been clear that this was the right structure for frequent removal.

The game ran fine with a few hundred particles. In the big battle scenes, with thirty thousand, the particle update alone took more time than the whole frame was allowed, and the game stuttered. Marta measured, expecting the removals to be the problem. They weren't. Most of the time went on simply walking the list. Each particle had been allocated separately, wherever memory was free, so each step to the next particle was a jump to a different part of memory, and almost every jump missed the processor's cache. The processor spent most of its time waiting for memory, a few dozen bytes at a time.

*Before reading on: the linked list made removal cheap and made every step through the list a trip to slow memory. What would you have used instead?*

She rewrote it as a plain array of particles, stored side by side. To remove a dead particle, she copied the last particle into its place and shrank the count by one. That was cheap, at the price of not keeping the particles in order, which didn't matter for sparks. Walking the array now read memory in a straight line, and the processor fetched the next particles before they were needed. The update ran about eight times faster. Then she went further and split the particles' fields into separate arrays, all positions together and all colours together, because the movement step only touched positions. Another doubling.

Looking back, Marta thought the textbook had been right about what it measured: the number of steps. On her machine, what a step cost depended entirely on where the data was. An array's data was together. A linked list's data was wherever it happened to land.

## Where it shows up

| Page | The layout | What it decided |
| --- | --- | --- |
| [1, One machine, one program](../01-one-machine-one-program.md) | Joan's grid, walked against its layout | The same lesson with pages and a drum: touching data in the order it's stored is fast; jumping around is slow. |
| [Latency numbers](../latency/latency-numbers.md) | Cache against main memory | About a hundred times apart, which is why data kept together wins. |
| [Access patterns](../data/access-patterns.md) | Storing fields together, as in column stores | Marta's split arrays are a column store in miniature. |
| [Hash tables](hash-tables.md) | Open addressing keeps entries in one array | Often faster than chaining, which scatters entries in linked lists. |

It shows up elsewhere too: in standard library advice to prefer dynamic arrays by default, in database pages, and in game engines organised around arrays of components.

What these share is page 1's lesson at the smallest scale: the cost of an operation is set by where the data is, and data kept together is cheap to walk.

## It really happened

Marta is fictional; her rewrite is standard practice in game programming, where it's called data-oriented design. Mike Acton's 2014 CppCon talk, "Data-Oriented Design and C++", argued that the layout of data in memory, not the elegance of the code, decides performance on modern hardware, and became widely cited. Standard libraries in most languages default to dynamic arrays for sequences for the same reason, and linked lists are kept for the cases they truly suit.

## What it is

An array stores elements contiguously, so any element can be reached by position in one step, and walking it reads memory in order, which processor caches handle very well. Inserting or removing in the middle means shifting elements. A linked list stores elements separately, each pointing to the next. Inserting and removing anywhere is cheap once you're there, but reaching an element means walking from the start, and each step may be a cache miss. On modern hardware, arrays are usually faster unless the list is huge and changes constantly in the middle.

## Where it gets misapplied

- **Choosing by big-O alone.** Marta's linked list: fewer steps on paper, far slower in practice.
- **Linked lists by default.** In most code, a dynamic array is the better starting point.
- **Arrays where order must be kept and the middle changes constantly.** Shifting large arrays repeatedly is genuinely slow; other structures exist for this.
- **The mirror:** contorting every data structure for cache layout in code where performance doesn't matter. Measure first ([profiling](../tooling/profiling.md)).

## Connections

- Learning this is also learning [latency numbers](../latency/latency-numbers.md), because the gap between cache and memory decides which structure wins.
- Learning this is also learning [access patterns](../data/access-patterns.md), because walking data in order is the pattern caches reward.
- Learning this is also learning [hash tables](hash-tables.md), because how a hash table stores collisions is a choice between these two.
- Learning this is also learning [profiling](../tooling/profiling.md), because Marta found the real cost by measuring, not by reasoning from the textbook.
- Learning this is also learning [B-trees](b-trees.md), because packing many keys into one node is the same idea for disks.

## Resources

1. Randal Bryant and David O'Hallaron, *Computer Systems: A Programmer's Perspective*, chapter 6, on locality (start here).
2. Mike Acton, "Data-Oriented Design and C++" (CppCon 2014, talk) (go deeper).
3. Ulrich Drepper, ["What Every Programmer Should Know About Memory"](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) (2007) (reference). <!-- verify -->

## Names you'll hear

- **Contiguous:** stored side by side.
- **Cache line:** the chunk of memory the processor fetches at once, typically 64 bytes.
- **Cache miss:** needing data that isn't in the cache, and waiting for memory.
- **Dynamic array, vector:** an array that grows by reallocating.
- **Structure of arrays, array of structures:** keeping each field in its own array, or each item's fields together.
- **Data-oriented design:** organising code around how data is laid out and accessed.

## Go and look

Find a list in code you've written that's walked often, and check how it's stored. If it's a linked structure, try the same loop over an array and time both.
