# Ten o'clock on Friday

A design case in the category **money that must be exact**. It draws on [rate limiting and backpressure](../../design/rate-limiting.md), [sagas](../../design/sagas.md), [consensus and leader election](../../design/consensus.md) and [timeouts](../../design/timeouts.md).

## The situation

A ticketing company sells seats for concerts. For most events, tickets trickle out over months. For the biggest tours, every ticket for a stadium goes on sale at ten o'clock on a Friday morning and is gone within twenty minutes. Fans choose their own seats on a map. Last year's biggest sale ended with 1,400 more tickets sold than the stadium had seats: two buyers had each been sold the same seat, and both had paid. The refunds and the apologies made the newspapers.

## Requirements and numbers

- Never sell the same seat twice, and never sell more tickets than exist.
- Let fans pick seats on a map, hold them while paying, and release them if payment doesn't finish.
- Be fair: people who arrived first should, roughly, get to choose first.
- Stay up for everyone else on the site while a big sale runs.
- A stadium has about 60,000 seats. About 2 million people try to buy in the first five minutes, each refreshing the seat map every few seconds.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What must always work?** Each seat is sold at most once. Everything else can be slower or rougher.
- **What's the peak?** Two million people for 60,000 seats: demand is more than thirty times the supply, all in one minute.
- **How does it fail?** Payment is slow and sometimes fails, and fans give up halfway.

## The tempting first design

Show the seat map from the database. When a fan picks a seat, check that it's free, take payment, then mark it sold.

Between the check and the "sold", another fan can pass the same check, so both pay for one seat. Two million people refreshing a map of 60,000 seats every few seconds is several hundred thousand reads a second against the table that also has to take every sale. And a fan whose payment takes a minute holds nothing, so their seat can be sold underneath them.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Only 60,000 people can possibly succeed. What if the other two million never reached the part of the system that sells seats at all, at least not all at once?

</details>

<details markdown="1"><summary>Hint 2</summary>

"Check, then sell" is two steps that someone else can slip between. What single operation could both check that a seat is free and take it?

</details>

<details markdown="1"><summary>Hint 3</summary>

Taking a seat and paying for it are separate steps, and paying can fail. What should a fan hold while they pay, for how long, and what happens when the time runs out?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

Two million people refreshing every five seconds is about 400,000 seat-map reads a second. The number of seats that can actually be sold is 60,000 in total, perhaps 100 a second at the peak. The design should let through only as many buyers as can be served, and serve the map from something that isn't the seat-selling database ([estimates](../../design/estimates.md)).

### Design A: a waiting room, holds, and one owner per section

- **A waiting room in front.** At ten o'clock, everyone who arrives is put in a queue in a random order (so refreshing early doesn't help), shown their place, and admitted a few thousand at a time as earlier buyers finish. Admission is a signed token with a time limit. Behind it, the seat-selling system sees a steady, bounded load ([rate limiting and backpressure](../../design/rate-limiting.md)).
- **A cheap, slightly stale map.** The map shows availability from a cache refreshed every second or two. A seat shown free may already be taken, and the fan is told so when they pick it; that's acceptable because the pick itself is exact.
- **One operation to take a seat.** Taking a seat is a single conditional write: "set seat 14-B-22 to held by this buyer, until 10:07, *only if* it's free or its hold has expired". Only one such write can succeed. Seats are partitioned by section, and each section's seats are owned by one database or one process, so the write never needs agreement between machines ([consensus](../../design/consensus.md) gives the leader of each partition, when one fails over).
- **Holds that expire.** A held seat stays held for, say, seven minutes while the fan pays. If the payment succeeds, the seat becomes sold in the same step that records the order; if it fails or the time runs out, the hold simply lapses and the seat is free again.
- **Order as a saga.** Hold the seat (cheap to undo), take payment with an idempotency key, then issue the ticket. If payment fails, release the hold; if the ticket can't be issued, refund ([sagas](../../design/sagas.md)).

**What it costs:** fans wait in a visible queue, and some see a seat as free that isn't. The waiting room itself has to survive two million arrivals in a minute, so it's built to do almost nothing per visitor.

### Design B: no seat choice, allocate in order

Fans don't pick seats. Each admitted buyer asks for a number of tickets in a price band, and the system allocates the best available seats from a counter per band, decremented atomically.

**What it gives:** one counter per band instead of 60,000 seats to contend over, no map to serve, and much higher throughput. Many large sales work this way.

**What it costs:** fans lose the choice of seat, and groups may be split. It's a business decision as much as a technical one, and worth putting to the people who sell the tickets.

</details>

## What breaks at ten times the size

- **A world tour on sale in ten cities at once.** Partition by event, so one sale's load can't affect another's; the waiting room becomes the busiest part of the system.
- **Bots.** At this demand, automated buyers are most of the traffic; the waiting room needs checks that make each place in the queue cost something.
- **Payment providers.** A hundred payments a second may hit the provider's own limits; holds must be long enough to cover slow payments, and timeouts short enough to keep seats moving ([timeouts](../../design/timeouts.md)).

## Where people slip

- **Check, then write.** Two buyers pass the check at once. Make taking a seat one conditional operation.
- **Selling before payment, or holding forever.** A hold needs an expiry, and only a confirmed payment turns it into a sale.
- **Letting everyone in.** Two million people can't all be served at once; admit them at the rate the system can sell.
- **Serving the map from the selling database.** The reads crowd out the writes that matter.
- **Rewarding refreshing.** A queue ordered by who refreshed fastest rewards bots; randomise arrivals at opening.

## Related

- The other case in this category: [the tutors' wages](payments-ledger.md), a payments ledger.
- Design pages: [rate limiting and backpressure](../../design/rate-limiting.md), [sagas](../../design/sagas.md), [consensus and leader election](../../design/consensus.md), [idempotency](../../design/idempotency.md), [timeouts](../../design/timeouts.md).
- Other pages: [11, Software that must not go down](../../11-software-that-must-not-go-down.md), [partitioning](../../data/partitioning.md), [caching](../../performance/caching.md), [queues](../../dsa/queues.md).
