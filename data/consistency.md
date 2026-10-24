# Consistency

Last reviewed: 2026-10-24

A concept page: copies that disagree, and what you promise while they do.

## Problem

The moment data exists in two places, a cache, a replica, a browser, a second system, the two copies can disagree. You can't make that impossible without giving something up. You can only decide who notices, for how long, and what you promise them.

## The story

In 1986 Tom Avery looked after the computers for a county library service with nine branches. Each branch kept its own copy of the catalogue, including which books were on loan, and every night the copies were sent to the central library, merged, and sent back. It worked well for years. Readers could see from any branch whether a book was in.

Then the county added online reservations. A reader at one branch reserved the last copy of a popular novel; twenty minutes later a reader at another branch reserved the same copy, because that branch's catalogue still showed it as available. Both were told it was theirs. Within a month the complaints were a weekly event.

Tom's first fix was the obvious one: send the changes more often. He moved the nightly exchange to every hour, then every fifteen minutes, which tied up the phone lines all day. The double reservations got rarer and never stopped. However often he copied, there was always a gap, and someone always fell into it.

*Before reading on: copying faster only shrank the gap. What would you have changed instead?*

He stopped trying to make the copies agree, and started deciding what each copy was allowed to promise. Every book now had one owner: the branch that held it. Only the owner could say a book was reserved. Other branches still showed what their copy said, labelled *as of this morning*, and when a reader wanted to reserve, the branch phoned the owner's computer and asked. The answer took a few seconds longer, and it was always right.

Looking back, Tom thought the mistake had been treating the copies as the truth. They were only ever copies. The useful question wasn't *how do I keep them identical?* but *who is allowed to decide, and what do I tell everyone else while they wait?*

## Where it shows up

| Page | The copies | What was promised |
| --- | --- | --- |
| [4, Data outlives programs](../04-data-outlives-programs.md) | The actuaries' second copy of the claims, in a different shape | Nothing, at first. Someone had to keep it in step by hand, and it drifted. |
| [6, Anyone can publish](../06-anyone-can-publish.md) | Each receptionist's browser and the server | The browser may assume, but the server decides. One owner, like Tom's branches. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | The main database and its read replicas | You always see your own posts; everyone else sees them within a second or so. |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | The old payments system and the new one | Neither is trusted until they've matched every night for a month. |

It shows up elsewhere too: every cache ([caching](../latency/caching.md)), every offline-capable app, and every learned model, which is a copy of the world as it was when the training data was collected ([page 12](../12-machines-that-learn-from-data.md)).

The pages use four different answers. You can have **one owner** decide, as Tom, Hannah and every primary database do. You can promise **read-your-writes**, as Maya does: you see your own changes, and others catch up. You can **merge** later, as Amazon's shopping cart does, accepting that a deleted item may come back. Or you can **compare and reconcile**, as Ines does, trusting nothing until the copies agree. None of them is free.

## It really happened

Tom is fictional. The deeper problem, that machines can't agree on the order of events without communicating, was set out by Leslie Lamport in 1978 ("Time, Clocks, and the Ordering of Events in a Distributed System"). Amazon's Dynamo paper chose merging on purpose, because a shopping cart you can't add to loses sales ([page 8](../08-too-many-users-too-much-data.md)). Werner Vogels, Amazon's CTO, later explained the trade for a general audience in "Eventually Consistent" (*ACM Queue*, 2008). Kyle Kingsbury's [Jepsen](https://jepsen.io/analyses) <!-- verify --> tests have repeatedly found databases that promised more consistency than they delivered.

## What it is

Consistency is what a system promises about how copies of data relate to each other, and to what readers see. Strong consistency means every reader sees the latest write, which costs waiting or refusing requests when copies can't talk. Weaker promises, such as read-your-writes or eventual consistency, let copies disagree for a while in exchange for speed and availability. Every copy is a promise about staleness, whether or not anyone wrote it down.

## Where it gets misapplied

- **Copying faster instead of deciding.** Tom's fifteen-minute sync. A shorter gap is still a gap.
- **Strong consistency everywhere.** Paying in latency and outages for promises nobody needed, such as an exact like count.
- **Unwritten promises.** A cache with no stated staleness is a bug report waiting to happen.
- **The mirror:** "eventual consistency" as an excuse not to think. Eventually can mean a second or a week, and some things, like money and reservations, need one owner.

## Connections

- Learning this is also learning [replication](replication.md), because replicas are the copies most systems deliberately make.
- Learning this is also learning [caching](../latency/caching.md), because a cache is a copy you've agreed to let go stale.
- Learning this is also learning [queueing](../latency/queueing.md), because asking the owner means waiting for it, and everyone who asks waits in line.
- Learning this is also learning [migrations](migrations.md), because running old and new side by side is two copies on purpose.
- Learning this is also learning [state machines](../dsa/state-machines.md), because agreeing copies are often built by applying the same changes in the same order.

## Resources

1. Werner Vogels, "Eventually Consistent" (*ACM Queue*, 2008) (start here: short, and written by someone who had to choose).
2. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapters 5 and 9 (go deeper).
3. Leslie Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System" (1978).
4. [Jepsen analyses](https://jepsen.io/analyses) (reference: what databases actually do). <!-- verify -->

## Names you'll hear

- **Strong consistency, linearizability:** every read sees the latest write.
- **Eventual consistency:** if writes stop, copies will agree. No promise about when.
- **Read-your-writes:** Maya's promise.
- **Single source of truth:** one owner for each piece of data.
- **CRDT:** a data structure designed so that copies always merge to the same result.

## Go and look

Pick one piece of data you see on a screen every day and count how many copies of it exist between where it's stored and your eyes. For each one, ask how stale it's allowed to be, and who decided.
