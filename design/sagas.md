# Sagas

Last reviewed: 2026-11-27

A concept page: doing one piece of work across several services, without a transaction to make it all-or-nothing. Each step is committed on its own, and each has a planned way back.

## Problem

Inside one database, a transaction makes a group of changes happen together or not at all. Once the work is spread across services with their own databases, run by different teams or different companies, that promise is gone: a payment provider won't hold a lock while your warehouse thinks. So a piece of work that spans them can stop halfway, with some steps done and others not, and somebody has to **decide** what happens then. Pretending it can't happen is the usual answer, and the costly one.

## The story

In 2020 Tolu Oyelaran led the team building orders for an online grocery in Lagos. The shop had grown into separate services, each owned by a team and with its own database: payments, the warehouse's stock, and delivery slots. Placing an order meant three calls, in order: charge the customer's card, reserve the items in the warehouse, and book a delivery slot. If any call failed, the order service returned an error and the customer tried again. Each service was reliable on its own, and when Tolu looked at a week of orders, all three calls succeeded more than ninety-nine times in a hundred.

The other one time in a hundred was where the trouble was. On Saturday mornings delivery slots ran out between a customer opening the checkout and pressing *Pay*, so the card was charged, the stock reserved, and the slot refused. The customer saw an error and had paid for nothing. When the order service crashed between steps, stock stayed reserved for orders that would never come, and the website showed popular items as sold out while they sat on the shelves. By the time the support team noticed the pattern, about six hundred customers a week were being charged for orders that didn't exist.

Someone suggested a distributed transaction, with all three services voting before any of them committed. Tolu looked into it. The payment provider didn't take part in such protocols, and holding locks across three services while they voted would have frozen the warehouse's stock for seconds at a time on its busiest morning.

*Before reading on: the three steps couldn't be made all-or-nothing. What could Tolu promise instead?*

She stopped trying to make the steps happen together, and planned for them to happen apart. Each step got a partner that undid its effect as far as anything could be undone: releasing reserved stock, cancelling a booked slot, refunding a charge. The order service became a coordinator that wrote each step to its own log before doing it, so that after a crash it could read where it had got to and either carry on or work backwards through the partners it needed. Every step and every partner was made safe to repeat, because the coordinator would retry them.

Then she changed the order. Reserving stock and holding a slot were cheap to undo, and nobody outside the shop ever saw them. A charge was expensive to undo: a refund took days, and it appeared on the customer's statement whatever the shop did. So the card was now charged last, only after the stock and the slot were both secured. If the slot was gone, the stock was released and the customer was told before any money moved. The failures didn't disappear: a card could still be declined after everything else was held, and then the stock and slot were released. But the expensive, visible undo became rare instead of routine.

![Three steps of an order, left to right: reserve stock, hold a delivery slot, charge the card. Under each, an arrow down to its compensating step: release stock, release the slot, refund. The first two are cheap and invisible to the customer; the refund takes days and appears on their statement, which is why the charge comes last.](../images/figures/design-sagas.svg)

*Without one transaction, every step needs a way back, and the hardest one to take back goes last.*

Looking back, Tolu thought the original design hadn't been wrong about any single call. It had been wrong about the gaps between them, which it treated as if they couldn't happen. Planning the way back for each step, and choosing the order so that the hardest way back was needed least, turned the gaps into something the system handled instead of something customers found.

## Where it shows up

| Page | The work across parts | What it taught |
| --- | --- | --- |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Walter's payments batch, cut off by a power failure | Inside one database, the transaction undid the half-finished batch by itself. Tolu's services had no such promise to fall back on. |
| [Append-only logs](../dsa/append-only-logs.md) | Teresa's ledger, where a duplicate bonus was corrected | Mistakes aren't erased, they're reversed by a new entry, which is exactly what a compensation is. |
| [Idempotency](idempotency.md) | Valeria's retried charges | The coordinator retries steps and compensations, so all of them must be safe to repeat. |
| [Consistency](../data/consistency.md) | Copies that disagree for a while | Between steps, other customers can see the order half-done, such as stock reserved and not yet paid for; a saga gives up a transaction's isolation. |
| [State machines](../dsa/state-machines.md) | Chloe's order states | A saga is a state machine over a long-running order, where every state has a defined way forward and a defined way back. |

It shows up elsewhere too: a travel agent booking a flight, a hotel and a car, then cancelling the other two when the hotel is full; bookkeeping's reversing entries; a wedding called off, with deposits recovered one supplier at a time; and a contract's cancellation clauses, written before anyone needs them.

What the rows share is that once work crosses a boundary nobody controls on both sides, "all or nothing" becomes "all, or a planned way back". The way back is new work, not undoing, and it's worth choosing the order of steps so that the most expensive way back is needed least.

Motif: [costs move; they don't disappear](../motifs.md#costs-move-they-dont-disappear).

## It really happened

Tolu is fictional, and so is her grocery. The pattern is named after a 1987 paper by Hector Garcia-Molina and Kenneth Salem, written about long transactions inside a single database, which held locks for so long that they blocked everything else. They proposed splitting such a transaction into a sequence of smaller ones, each with a *compensating transaction*, so that the system could guarantee that either the whole sequence ran or the completed parts were compensated ([Garcia-Molina and Salem, "Sagas", SIGMOD 1987](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf)). The idea found its larger use decades later, when systems split into services with separate databases.

In 2007 Pat Helland argued that very large systems would have to give up distributed transactions altogether and design the business itself to cope with uncertainty, with apologies and compensations as ordinary parts of the work ("Life beyond Distributed Transactions: an Apostate's Opinion", CIDR 2007). Bookkeepers had worked that way for centuries: Luca Pacioli's 1494 description of double-entry bookkeeping already corrected errors with new entries rather than erasures.

## What it is

A **saga** is a sequence of local transactions, each committed in its own service, where every step except possibly the last has a **compensating action** that semantically undoes it. If a step fails, the compensations for the completed steps run in reverse order. Sagas can be **orchestrated**, by a coordinator that records progress in a durable log and calls each service, or **choreographed**, with each service reacting to events from the previous one. Steps and compensations must be idempotent, because they'll be retried. A useful ordering is to put steps that are easy to compensate first, steps that can't be compensated last (sometimes called the *pivot*), and steps that can only succeed after the pivot. A saga doesn't give isolation: other work can see its intermediate states, so designs add things like "pending" states or reservations to make those states safe to see.

## Where it gets misapplied

- **Ignoring the gaps.** A sequence of calls with an error message at the end is a saga with no way back.
- **Compensations that can fail and aren't retried.** A refund that fails once and is forgotten leaves the customer charged for nothing.
- **Treating compensation as undo.** A refund isn't the same as never having been charged; an email can't be unsent. Design the visible steps to come last.
- **No durable record of progress.** A coordinator that crashes and forgets where it was can't finish or compensate.
- **The mirror:** sagas inside one database. If all the data lives in one place, a transaction is simpler, safer and already built.

## Connections

- Learning this is also learning [idempotency](idempotency.md), because every step and compensation will be retried and must be safe to repeat.
- Learning this is also learning [append-only logs](../dsa/append-only-logs.md), because a coordinator's log of steps is what lets it recover, and a compensation is a reversing entry.
- Learning this is also learning [state machines](../dsa/state-machines.md), because each order's progress through a saga is a state machine with ways forward and ways back.
- Learning this is also learning [consistency](../data/consistency.md), because between steps the world can see a half-finished order, and the design has to say what that means.
- Learning this is also learning [consensus and leader election](consensus.md), because a distributed transaction needs every participant to agree, and a saga is what you do when they can't or won't.

## Resources

1. Hector Garcia-Molina and Kenneth Salem, ["Sagas"](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf) (1987) (start here: short and readable).
2. Pat Helland, "Life beyond Distributed Transactions: an Apostate's Opinion" (CIDR 2007; revised in *ACM Queue*, 2016) (go deeper: why large systems end up working this way).
3. Chris Richardson, ["Pattern: Saga"](https://microservices.io/patterns/data/saga.html) (reference: orchestration and choreography, with examples). <!-- verify -->

## Names you'll hear

- **Saga:** a sequence of local transactions with compensations.
- **Compensating transaction, compensation:** the step that semantically undoes another.
- **Orchestration, choreography:** a coordinator calling each step, or services reacting to each other's events.
- **Pivot transaction:** the step after which the saga can only go forward.
- **Two-phase commit (2PC):** the all-or-nothing protocol sagas avoid, where every participant votes before anyone commits.
- **Outbox:** writing an event to the same database as the change, so the two can't disagree.

## Go and look

Find a piece of work in something you've built that calls two or more services that change something. Pick a point between two of the calls and ask what happens if the process dies right there: what's been done, who would notice, and what would undo it.

Practise this: [the tutors' wages](../exercises/design/payments-ledger.md), where payouts to tutors' banks are a saga.
