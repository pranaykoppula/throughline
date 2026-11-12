# Motifs

Last reviewed: 2026-11-11

The same few shapes keep turning up in stories that look nothing alike: a hotel price in two regions, a library catalogue in nine branches and a design shared between browsers are all *copies that disagree*. Recognising a shape you've met before is much of what experience feels like, and it's what makes a new problem less strange. This page names the shapes that recur most often in this wiki, and lists where each one appears.

The names are used the same way everywhere. A page that shows a motif clearly says so in one line, "Motif:", at the end of its Where it shows up section, or of What survived on a spine page. Not every appearance is labelled: only where the shape is the point.

These are patterns across this wiki's stories, which are mostly fiction. They're a way of seeing, not findings about the world. Test each against the real cases in It really happened, and against what you've built.

## The verbs

Everything here does one or more of eight things to data: **represent** it, **store** it, **move** it, **transform** it, **find** it, **decide** with it, **show** it, and **protect** it. A page names its verb in bold where the verb is the point, and leaves it unsaid where it isn't. The motifs below are the shapes the trade-offs take while doing those things.

## Every representation has an edge

A way of writing the world down works for the problems its makers had, and quietly fails on one they didn't.

- [0, Representations](00-representations.md): numbers, symbols and rules, each with a problem it couldn't handle.
- [Floating-point](math/floating-point.md): Oskar's money, in a format built for approximations.
- [Number systems](math/number-systems.md): Priyanka's fixed width, which was a date in the future.
- [Data modelling](data/modelling.md): Yasmin's model, drawn from the first screen that showed the data.
- [Pagination](data/pagination.md): Hamza's page numbers, which came from books that don't change while you read.
- [Encodings](info/encodings.md): Kasia's bytes, read with the wrong codebook.
- [Sampling and aliasing](signals/sampling.md): Henrik's samples, too slow for the vibration that mattered.
- [Designed for human senses](signals/perception.md): Zainab's pixel values, which weren't amounts of light.
- [Language](info/language.md): words, lossy between people who don't share a context.

## Copies disagree

Any copy, kept to be faster, safer or closer, is sometimes out of date. The work is deciding who owns the truth and what each copy may promise.

- [6, Anyone can publish](06-anyone-can-publish.md): Hannah's server and the copies in a million browsers.
- [8, Too many users, too much data](08-too-many-users-too-much-data.md): Maya's copies, and what to promise while they disagree.
- [Caching](latency/caching.md): every cache is a copy, and the system comes to depend on it.
- [Replication](data/replication.md): Kwame's replica, and making sure only one copy accepts writes.
- [Consistency](data/consistency.md): Tom's nine library branches, each with its own catalogue.

## Where the data is sets the cost

Near is fast, small and expensive; far is slow, big and cheap. The price of almost any operation depends on the distance between data and the work.

- [1, One machine, one program](01-one-machine-one-program.md): core memory near the processor, drums further away.
- [Arrays and linked lists](dsa/arrays-and-linked-lists.md): Marta's linked list, scattered across memory.
- [B-trees](dsa/b-trees.md): Leonard's tree, reshaped for the size of a disk block.
- [Latency numbers](latency/latency-numbers.md): Daniel's table of how far away everything is.
- [Round trips](latency/round-trips.md): Ayesha's users on trains.
- [Data gravity](data/data-gravity.md): Imogen's petabytes, which pulled everything towards them.
- [Tokens and context windows](ai/tokens.md): the context window as a small, expensive, fast tier.
- [9, Buying computers is too slow](09-buying-computers-is-too-slow.md): Tariq's bill, topped by moving data, not computing.

## Waiting is where the time goes

Most slowness isn't work; it's waiting for something shared. Systems near full use make everyone wait, and a little slack keeps the line short.

- [2, One machine, many programs](02-one-machine-many-programs.md): Ruth's programs, idle while a tape drive turned.
- [Queueing](latency/queueing.md): Signe's servers, run close to full.
- [Queues](dsa/queues.md): Yusuf's line, and deciding who goes next.
- [Event loops and threads](runtimes/event-loops-and-threads.md): Omar's two ways of sharing time.
- [Round trips](latency/round-trips.md): every reply you wait for.

## Costs move; they don't disappear

A design that makes one thing cheap usually makes something else dearer: later, rarer, or someone else's problem.

- [LSM trees](dsa/lsm-trees.md): Neha's writes, cheap now and paid for later in merging.
- [Serialization formats](data/serialization.md): Jonas's format, which felt free because its cost was deferred.
- [Sorting](dsa/sorting.md): Margit's order, paid for once so that finding and merging were cheap ever after.
- [Amortised cost](dsa/amortised-cost.md): Henrike's cheap average, paid for in a pause every two minutes.
- [Dynamic programming](dsa/dynamic-programming.md): Imelda's table, memory spent so the same question is never answered twice.
- [4, Data outlives programs](04-data-outlives-programs.md): the first program's shape, paid for by every later one.
- [Data gravity](data/data-gravity.md): each terabyte raising the price of changing your mind.
- [Queueing](latency/queueing.md): idle capacity saved, and paid for in other people's waiting.
- [13, Everything still exists at once](13-everything-still-exists-at-once.md): switching costs paid now, benefits arriving later to someone else.

## Layers hide things, until they leak

An abstraction lets you forget the layer below. You get to forget until the layer below does something the abstraction didn't mention.

- [3, Programs too big for one head](03-programs-too-big-for-one-head.md): Elena's layers, each trading control for ease.
- [9, Buying computers is too slow](09-buying-computers-is-too-slow.md): a virtual machine hides the hardware, but not the neighbours.
- [Managed services](vendors/managed-services.md): Tamsin's services, rungs someone else built and could move.

## Enforce it once, at the boundary

A rule that everyone must remember everywhere will eventually be forgotten somewhere. Put it at the edge, in one place, in something that can't forget.

- [7, Strangers on the network](07-strangers-on-the-network.md): every place where something crosses from outside to inside.
- [Input validation](auth/input-validation.md): Frank's line, which carried strangers' sound and the network's commands.
- [Multi-tenancy](auth/multi-tenancy.md): Chidi's one line in every query, remembered until it wasn't.
- [Type systems](runtimes/type-systems.md): a boundary enforced by a machine.
- [State machines](dsa/state-machines.md): Chloe's one function that every change to an order went through.
- [Encodings](info/encodings.md): decode at the border, and speak one convention inside.
- [10, Many people, one codebase](10-many-people-one-codebase.md): practices that only held once a tool enforced them.
- [CI pipelines](tooling/ci.md): the pipeline as the place a team's rules actually live.
- [11, Software that must not go down](11-software-that-must-not-go-down.md): the Therac-25, whose protection depended on the thing it protected.

## The least power, for the shortest time

Anything that grants power is a key, and its power is the size of the damage when it leaks. Keep it narrow, keep it short-lived, and keep a way to take it back. The same goes for languages.

- [7, Strangers on the network](07-strangers-on-the-network.md): give every party the least it needs.
- [Least privilege](auth/least-privilege.md): Grace's permissions, a decision about the worst day.
- [Cloud IAM](auth/cloud-iam.md): one administrator key, used everywhere and never expiring.
- [Sessions and tokens](auth/sessions-and-tokens.md): Ana Lucía's token, a password with a shorter life.
- [Key management](crypto/key-management.md): Bram's key, which failed because it was everywhere and lived forever.
- [12, Machines that learn from data](12-machines-that-learn-from-data.md): a model given only the power it needs.
- [Coding agents](tooling/coding-agents.md): an agent working inside the access it has.
- [Power and predictability](dsa/power-and-predictability.md): the least powerful language that does the job.

## A cheap check before an expensive one

A quick test that's sure about "no" and only hopeful about "yes" saves most of the work, as long as its "yes" is checked.

- [Bloom filters](dsa/bloom-filters.md): Joaquín's filter, which let a hint make a final decision.
- [LSM trees](dsa/lsm-trees.md): Neha's filter on each file.
- [Caching](latency/caching.md): look nearby before going far.
- [Computability](dsa/computability.md): Viktor's scanner, which accepts false alarms as the price of answering at all.

## The sign drifts from the thing

A number, a label or a description stands for something you can't see directly. Rely on it, reward it, or stop looking past it, and it drifts away from what it meant.

- [Measures and targets](info/measures-and-targets.md): Ottilie's coverage gate.
- [Sampling and observation](info/observation.md): Kofi's green squares, and the fridges they didn't show.
- [Labels and training data](data/labels.md): judgements made in ten seconds.
- [11, Software that must not go down](11-software-that-must-not-go-down.md): servers up, and nobody able to buy a ticket.
- [CI pipelines](tooling/ci.md): Noor's green build.
- [Coding agents](tooling/coding-agents.md): Rafael's passing test, and the bug behind it.
- [Distributions and percentiles](math/percentiles.md): Leo's average, which described nobody.
- [Statistical significance](math/statistics.md): Lucas's dashboard, read like a scoreboard.
- [Meaning as use](info/meaning-as-use.md): Rui's documentation, and what users actually relied on.

## Every correction acts on old news

A system that measures and corrects is always correcting what it saw a moment ago. Correct too hard, or too late, and it swings.

- [Feedback and control](signals/feedback.md): Astrid's drone, bobbing past its target.
- [5, Machines need to talk](05-machines-need-to-talk.md): retrying harder into a congested network, until backoff.
- [Queueing](latency/queueing.md): clients retrying into a full queue.
- [12, Machines that learn from data](12-machines-that-learn-from-data.md): gradient descent, and a learning rate that overshoots.
- [State estimation](signals/state-estimation.md): Dorota's tractor, which had to know how old and how sure its picture was.

## The old keeps running

Almost nothing is replaced cleanly. The old system keeps running beside the new one, and whatever enough people rely on can't easily change.

- [13, Everything still exists at once](13-everything-still-exists-at-once.md): Ines's bank, where every era still ran.
- [Migrations](data/migrations.md): Bilal's two shapes of the data, alive at once.
- [Meaning as use](info/meaning-as-use.md): Rui's ordering, promised by nobody and relied on by everyone.
- [JavaScript](runtimes/javascript.md): Zara's quirks, frozen by success.
