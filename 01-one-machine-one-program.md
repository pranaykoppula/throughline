# 1. One machine, one program

Last reviewed: 2026-10-24

## Problem

A program needs its data close to the processor to run fast, but fast memory is small and expensive. Most of the data has to live somewhere bigger, slower, and further away, and something has to decide what's close at any moment.

## The story

Joan Hale joined the university computing laboratory in 1958 to help the chemists. They grew crystals, fired X-rays through them, and needed to turn thousands of measured spots into a picture of where the atoms were. By hand, one structure took a team months. The lab's computer could, in principle, do it in days.

The machine had two kinds of memory. A small core store held a few thousand numbers and answered in microseconds. A magnetic drum held far more, but it was a spinning cylinder, and to read a number you waited for the right spot on the drum to come round under the head. That took milliseconds, a thousand times longer. The crystal data didn't fit in core. Nothing interesting did.

So Joan did what everyone did. She split her program and its data into pieces and wrote instructions to copy each piece from drum into core just before it was needed, and back out again afterwards. Getting it wrong meant the program read garbage or overwrote itself. She spent her first month mostly drawing diagrams of what would be in core at each moment.

Then an older programmer showed her a trick. If you knew how fast the drum turned, you could place each piece of data on the drum at exactly the spot that would be passing under the head when the program wanted it. No waiting for a full turn. Joan reworked her placements with a stopwatch and a pencil, and her program ran five times faster. She was proud of it for weeks.

It didn't last. A chemist asked for one extra step in the calculation, and adding it shifted everything after it. Her careful placements were now all slightly wrong, and the program was slower than it had been before the trick. She spent ten days fixing timings for a change that had taken an hour to write. Her notebooks filled with drum positions. She realised she was spending more time deciding where numbers lived than doing chemistry.

*Before reading on: Joan was doing by hand something the machine could, in principle, watch itself doing. What would you have wanted the machine to do for her?*

In 1962 the laboratory got time on the new Atlas computer at Manchester, and Joan went to a talk about it. The Atlas team had grown tired of exactly what she'd been doing. On their machine, a program saw one big memory. The machine split it into fixed-size *pages*, kept the ones in use in core, and left the rest on the drum. When a program reached for something that wasn't in core, the hardware stopped it, fetched the page from the drum, put away a page that hadn't been used lately, and let the program carry on. The program never knew. They called it a one-level store.

Joan didn't fully believe it until she tried it. She threw away a third of her program, the part that only moved data around, and it simply worked. She wrote the chemists' extra step in an afternoon. It felt like being let out of a room.

A year later she ran the biggest structure yet: a grid of numbers larger than core, which her program updated column by column. It took all night instead of an hour. The program was correct. The machine was faster than anything she'd used. She checked the arithmetic twice and found nothing wrong, and for a few days she wondered whether the one-level store had been too good to be true.

It was an engineer from the Atlas team who asked how her grid was stored. Row by row, she said, the way it was written on paper. And how did she walk through it? Column by column. He drew it for her. Each step down a column landed in a different row, and so, most of the time, on a different page. Core could hold only a few dozen pages. Her program was touching hundreds of them in turn, so almost every step meant fetching a page from the drum and throwing out one it would need again moments later. The machine was spending all night moving pages and almost no time computing.

She swapped the order of her two loops so the program walked along each row instead of down each column. Nothing else changed. The run took fifty minutes.

The one-level store hadn't failed her. It had hidden *where* her data lived, and she'd taken that to mean it no longer mattered. It still did. The machine would put things in the right place for her, but only if she touched things that were near each other at around the same time. She'd stopped deciding where her data lived. She hadn't stopped paying for where it lived.

Looking back, everything she learned in those years came down to one idea: fast memory is small and close, big memory is slow and far, and the cost of anything you do is set by where the data is when you need it. The machines got faster for the rest of her career, and that never changed. Each new layer, caches in front of core and disks behind the drum, just added another floor to the same building.

## It really happened

Joan is fictional. Her problem wasn't. IBM 650 programmers in the 1950s placed instructions on a spinning drum by hand so each would arrive under the head just in time, and assemblers such as SOAP were written to do the placing for them; a young Donald Knuth wrote one of its versions ([SOAP](https://en.wikipedia.org/wiki/Symbolic_Optimal_Assembly_Program)). The Atlas team at Manchester built the one-level store, the first virtual memory, because hand-programmed transfers between core and drum had become impractical (Kilburn, Edwards, Lanigan and Sumner, "One-Level Storage System", *IRE Transactions on Electronic Computers*, 1962; [IEEE milestone](https://ethw.org/Milestones:Atlas_Computer_and_the_Invention_of_Virtual_Memory,_1957-1962)).

The collapse Joan saw got a name later in the 1960s, once machines ran many programs at once and all of them fought for the same pages: *thrashing*. Peter Denning showed in 1968 that it came from the huge gap between core and drum, and that the fix was to keep each program's *working set*, the pages it was actually using, in fast memory ([Denning, 1968](https://cs.uwaterloo.ca/~brecht/courses/epfl/Possible-Readings/vm-and-gc/thrashing-denning-afips-1968.pdf)). Ladder: virtual memory moved up, trading control for ease; Joan's loop swap was a small step back down, knowing the layer underneath well enough to work with it. Both were right.

Her loop-order bug still happens today, one floor up. Walk a large grid in the wrong order and the processor's caches miss the same way core missed.

## What survived

Memory is a hierarchy: a little fast storage near the processor, and ever larger, slower, cheaper storage further away. Abstractions like virtual memory and caches move data between the layers for you, but they don't hide the cost. They reward *locality*: touching data that's near data you just touched. The cost of an operation is set by where the data is.

## Where it gets misapplied

- **Optimizing the computation while the data is far away.** Shaving processor cycles off a loop that waits on a disk or a network saves nothing you'll notice. Find out where the time goes first.
- **Buying a bigger machine before measuring.** More memory fixes a working set that doesn't fit. It does nothing for a program that touches data in the wrong order.
- **The mirror:** treating memory as free and flat because the abstraction says so. It's flat to the program. It isn't flat to the clock.

## Connections

- Learning this is also learning [latency numbers](latency/latency-numbers.md), because a memory read, a disk read and a network round trip differ by factors of a thousand, and those ratios explain why some things are fast.
- Learning this is also learning [arrays and linked lists](dsa/arrays-and-linked-lists.md), because an array that keeps its data together often beats a linked list that's better on paper, for exactly Joan's reason.
- Learning this is also learning [cloud](09-buying-computers-is-too-slow.md), because a rented machine is still a machine with the same hierarchy, now with a network at the bottom.
- Learning this is also learning [storage tiers](cost/storage-tiers.md), because fast storage is expensive storage at every level, and cloud pricing is the memory hierarchy with a price list.

## Resources

1. ["Latency numbers every programmer should know"](https://gist.github.com/jboner/2841832), after Jeff Dean (start here: one screen, and it reframes everything). <!-- verify -->
2. Randal Bryant and David O'Hallaron, *Computer Systems: A Programmer's Perspective*, chapter 6, the memory hierarchy (go deeper).
3. Ulrich Drepper, ["What Every Programmer Should Know About Memory"](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) (2007; reference, and long). <!-- verify -->
4. Peter Denning, ["Thrashing: Its Causes and Prevention"](https://cs.uwaterloo.ca/~brecht/courses/epfl/Possible-Readings/vm-and-gc/thrashing-denning-afips-1968.pdf) (1968): the original diagnosis.

## Names you'll hear

- **Virtual memory, pages:** the Atlas idea, now in every operating system.
- **Thrashing, working set:** Denning's names for the collapse and its cure.
- **Moore's law** (Gordon Moore): transistor counts doubling roughly every two years. Processors sped up much faster than memory did, so the gap between the floors kept widening.
- **Amdahl's law** (Gene Amdahl): speeding up one part of a job only helps as much as that part's share of the total time.

## Go and look

Find a lookup by key and a full scan in something you've built, and time both. Then look at which one your busiest screen actually does.

## The model so far

New on this page: sentence 1, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. **A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.**
