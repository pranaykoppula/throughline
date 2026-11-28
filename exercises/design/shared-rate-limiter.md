# A hundred requests a minute, across forty servers

A design case in the category **coordination**. It draws on [rate limiting and backpressure](../../design/rate-limiting.md), [consistency](../../data/consistency.md), [partitioning](../../data/partitioning.md) and [timeouts](../../design/timeouts.md).

## The situation

A company sells access to a public API for weather data. Each customer's plan sets a limit, from 60 requests a minute on the free plan to 100,000 on the largest, and customers are billed by the plan. The API runs on forty servers behind a load balancer. The first version kept a counter in each server's memory, so a customer limited to 100 a minute could in fact make 100 a minute *on each server*, 4,000 in total. When the company fixed that by counting every request in one central database, every API call got slower, and when the database had a bad afternoon, so did the whole API.

## Requirements and numbers

- Enforce each customer's limit across all servers, closely enough that nobody gets much more than they pay for.
- Add at most a millisecond or two to each request.
- Allow short bursts within the limit, and answer 429 with a time to retry when it's exceeded.
- If the limiting system fails, the API should keep serving.
- About 200,000 customers, 50,000 requests a second at the peak, and one customer making a fifth of all traffic.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What must always work?** The API itself. Limiting protects it and enforces plans, but mustn't become the thing that takes it down.
- **How exact does it need to be?** A customer getting 103 requests in a minute instead of 100 harms nobody; one getting 4,000 does.
- **How does it fail?** The counter store is slow or down.

## The tempting first design

One central store holds a counter per customer per minute. Every request increments the counter and checks it against the limit before continuing.

At 50,000 requests a second, every request now waits for a round trip to the central store, and the counter of the largest customer is incremented 10,000 times a second, all on one key. If the store is slow, every API call is slow; if it's down, the choice is between refusing everyone and limiting no one.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Does every request need to ask the central store, or could each server be given a share of each customer's allowance and ask only when its share runs out?

</details>

<details markdown="1"><summary>Hint 2</summary>

A counter per fixed minute lets a customer send their whole limit at 12:00:59 and again at 12:01:00. What way of counting avoids that edge?

</details>

<details markdown="1"><summary>Hint 3</summary>

If the counter store disappears, what's the least harmful thing for the API to do, and for how long?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

50,000 requests a second across forty servers is about 1,250 a second per server. A central check on every one is 50,000 round trips a second to the store, adding perhaps half a millisecond each on a good day. The largest customer alone is 10,000 a second, on one key. 200,000 customers × a few counters each is small: the limiter's state fits in memory on one machine; the traffic to it is the issue ([estimates](../../design/estimates.md)).

### Design A: a shared store, with local allowances

- **Token buckets in a shared store.** Each customer has a token bucket in an in-memory store, partitioned across a few machines by customer ID: a count of tokens and the time it was last refilled. Taking tokens is one atomic operation that refills by elapsed time and subtracts, so there's no edge at the minute boundary ([rate limiting](../../design/rate-limiting.md), [partitioning](../../data/partitioning.md)).
- **Local allowances.** Instead of asking the store for every request, each API server takes a batch of tokens for a customer at a time, say a tenth of the customer's per-second rate, and spends them locally, asking for more when they run out. Most requests never leave the server. The cost is a little imprecision: tokens taken by a server that then goes quiet are briefly unused, and a customer can exceed the limit by up to one batch per server.
- **Big customers, small customers.** The largest customer's bucket is spread over several sub-buckets, each holding a share of the limit, so no single key takes 10,000 operations a second. Small customers, with limits of a request a second, need no local batching at all.
- **Fail open, briefly.** If the store doesn't answer within a couple of milliseconds, the server allows the request and falls back to a local estimate: the customer's limit divided by the number of servers. The API keeps working; for a few minutes, customers might get somewhat more than they paid for, which is a far smaller cost than an outage ([timeouts](../../design/timeouts.md)).
- **Clear answers.** A request over the limit gets 429 with the number of seconds until enough tokens will have refilled.

**What it costs:** limits are enforced within a few percent, not exactly, and the store is one more thing to run.

### Design B: each server enforces a share, with gossip

There's no central store. Each server enforces the customer's limit divided by the number of servers, and every second the servers share their recent counts with each other, so a server can lend unused allowance to the ones that are busy with that customer.

**What it gives:** no dependency on a store at all, and no extra latency.

**What it costs:** with an uneven load balancer, a customer whose requests happen to land on a few servers is limited below their plan until the gossip catches up; and the number of servers must be known everywhere. It suits limits that protect capacity more than limits that enforce billing ([consistency](../../data/consistency.md)).

</details>

## What breaks at ten times the size

- **More servers in more regions.** A global limit across continents can't afford a round trip to one store; give each region a share of each customer's limit and rebalance slowly.
- **Limits by more than customer.** Per endpoint, per IP address, per API key within a customer: each multiplies the number of buckets. Keep the expensive limits central and the cheap ones local.
- **Abuse.** At ten times the traffic, most excess may come from people trying to get around limits with many free accounts; that's a different problem, solved by sign-up checks, not by the limiter.

## Where people slip

- **A counter per server.** Forty servers, forty times the limit.
- **A central check on every request.** The limiter becomes the slowest and least reliable part of the API.
- **Fixed windows.** Twice the limit is allowed across the boundary between two windows.
- **Failing closed.** When the limiter is down, refusing everything turns a limiter outage into an API outage.
- **Pretending it's exact.** Say what the tolerance is, and design for it.

## Related

- The other case in this category: [every hour, on the hour](job-scheduler.md), a job scheduler for millions of timed tasks.
- Design pages: [rate limiting and backpressure](../../design/rate-limiting.md), [timeouts and circuit breakers](../../design/timeouts.md), [load balancing](../../design/load-balancing.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [consistency](../../data/consistency.md), [partitioning](../../data/partitioning.md), [multi-tenancy](../../security/multi-tenancy.md), [exact or approximate](../../dsa/exact-or-approximate.md).
