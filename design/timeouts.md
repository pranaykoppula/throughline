# Timeouts and circuit breakers

Last reviewed: 2026-11-27

A concept page: deciding how long to wait, what to do instead, and when to stop asking a part that's failing. A slow dependency is more dangerous than a dead one, because a dead one fails fast and a slow one holds on to everything that's waiting for it.

## Problem

Every call to another service is a bet that it will answer soon. Most of the time it does, so the waiting is invisible. When it doesn't, every caller waits, and while it waits it holds on to something limited: a thread, a connection, memory, a user's patience. A system made of many services can be taken down by its least important part, not because that part failed, but because it got slow and everything else kept waiting for it. Somebody has to **decide**, in advance, how long each wait may last and what happens when it runs out.

## The story

In 2014 Ji-woo Han looked after the website of an online bookshop in Seoul. Each book's page was built by the shop's web servers from several smaller services: prices, stock, reviews, and a recommendations service that suggested what other readers had bought. The recommendations were worth having: about one sale in twelve started with a click on one. Each web server had two hundred worker threads, and every page used one while it waited for all the services to answer. The calls used the HTTP library's default settings, which, Ji-woo found out later, meant waiting up to a minute. Nobody had chosen that number. Nothing had ever needed more than a fraction of a second.

One Monday lunchtime, the recommendations service's database began rebuilding an index, and every recommendation took thirty seconds instead of thirty milliseconds. The book pages waited for them. Within about ninety seconds, all two hundred threads on every web server were waiting for recommendations, and there were none left for anything else. The home page stopped loading. So did search, and the basket, and checkout, which didn't use recommendations at all. For forty minutes the whole shop was down, because the least important box on a book's page had become slow.

*Before reading on: the recommendations were the least important thing on the page. How did they take checkout down with them?*

Ji-woo saw that the failure had spread through waiting, not through errors. The recommendations service never refused anything; it was just slow, and every caller held a thread while it waited. A crashed service would have been harmless by comparison: the calls would have failed in milliseconds, and the page would have been drawn without them. So she made every call fail fast enough to be harmless. Each page had a budget of 800 milliseconds, and each call got a share of it: 150 for recommendations, with a fallback of the week's bestsellers, kept in memory, if the time ran out. Recommendations got their own pool of twenty threads, so however slow they became, they could never take more than twenty from the page. And a **circuit breaker** watched the calls: if more than half had failed or timed out in the last ten seconds, it stopped calling the service for thirty seconds and used the fallback straight away, then let a single call through to test whether the service had recovered. A sick service now got a rest instead of a queue.

![A line chart of busy worker threads on one web server, during the minutes after the recommendations service slowed down. Without timeouts, busy threads climb from about twenty to the limit of two hundred within ninety seconds and stay there, so nothing else can be served. With a 150-millisecond timeout, a separate pool and a circuit breaker, they stay close to twenty throughout.](../images/figures/design-timeouts.svg)

*The slow service didn't fail. It held on to every thread that called it, until there were none left.*

Looking back, Ji-woo thought the dangerous setting had been the one nobody had chosen. Every call had always had a timeout: a minute, by default, which only meant that nobody had decided how long the shop could afford to wait. Deciding that, for every call, was most of the fix.

## Where it shows up

| Page | The wait | What it taught |
| --- | --- | --- |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Rosa's checkout, waiting on a slow payment provider | Waiting, not failing, is how most outages start; the machines were up and the customers couldn't buy. |
| [Queueing](../performance/queueing.md) | Signe's operators, close to fully busy | Threads in use equal arrivals times waiting time: when the wait grows a thousandfold, so does the number of threads held. |
| [Rate limiting and backpressure](rate-limiting.md) | Farida's database, flooded by a stranger's bug | A refusal is a fast failure on purpose, so the caller stops holding on. |
| [Load balancing](load-balancing.md) | Tomasz's broken server | Taking a failing server out of rotation for a while is a circuit breaker at the balancer. |
| [Idempotency](idempotency.md) | Valeria's charges, timed out at ten seconds | A timeout ends the wait but not the work; the outcome is unknown until you ask again. |
| [Feedback and control](../signals/feedback.md) | Loops that correct on old news | A breaker that opens and closes too eagerly oscillates; the half-open test is a slow, deliberate correction. |

It shows up elsewhere too: the fuse or breaker in a house's electrics, which cuts one circuit so the wiring doesn't burn, a ship's bulkheads, which keep one flooded compartment from sinking the rest, a restaurant that takes a dish off the menu for the night rather than keep tables waiting for it, and a meeting with an end time.

What the rows share is that a slow part is contagious and a failed part isn't. Every wait needs a limit chosen on purpose, a fallback for when the limit is reached, and a wall that stops one dependency from taking more than its share.

Motif: [waiting is where the time goes](../motifs.md#waiting-is-where-the-time-goes).

## It really happened

Ji-woo is fictional, and so is her bookshop. The patterns are well known. Michael Nygard's *Release It!* (2007) named the circuit breaker and the bulkhead for software, borrowing both from engineering outside it. In 2012 Netflix released Hystrix, a library that wrapped every call to another service with a timeout, a separate pool of threads and a circuit breaker; Netflix said it was making tens of billions of such isolated calls a day ([Netflix Technology Blog, "Introducing Hystrix for Resilience Engineering"](https://netflixtechblog.com/introducing-hystrix-for-resilience-engineering-13531c1ab362)). Netflix later stopped developing it, in favour of approaches that adjust limits automatically.

Not everyone recommends breakers. Marc Brooker, writing about how Amazon handles retries, warns that circuit breakers introduce modes that are hard to test and can slow recovery, and describes limiting retries with a token bucket instead. The same article explains why retries at every layer are dangerous: five layers each trying three times can multiply the load on a struggling database by 243 ([Amazon Builders' Library, "Timeouts, retries, and backoff with jitter"](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)).

## What it is

A **timeout** limits how long a caller waits. Good ones come from a budget: the time the whole operation can afford, divided between the calls it makes, and often set from the dependency's measured latency at a high percentile. A **deadline** passes the remaining budget along, so that services further down stop work nobody is still waiting for. A **fallback** says what to do when the time runs out: a cached answer, a default, or a page without that part. A **circuit breaker** tracks recent failures to a dependency; when they pass a threshold it *opens* and fails calls immediately, then after a pause goes *half-open* and lets a few through to test recovery. A **bulkhead** gives a dependency its own limited pool of threads or connections, so its slowness can't use up everyone else's. Retries belong with all of these, at one layer only, with backoff, and only for requests that are safe to repeat.

## Where it gets misapplied

- **Default timeouts.** A library's default is usually long or infinite, chosen by someone who didn't know your system.
- **The same timeout everywhere.** A caller with a two-second limit that calls something with a five-second limit waits for work it will throw away.
- **Retrying at every layer.** The retries multiply, and turn a slow database into a flood.
- **A breaker without a fallback.** Failing fast is only useful if there's something sensible to show instead.
- **The mirror:** timeouts so short that ordinary slow moments become failures, and a breaker that opens on a normal blip and takes a healthy service out of use.

## Connections

- Learning this is also learning [queueing](../performance/queueing.md), because every waiting call holds something, and the number held grows with how long the wait lasts.
- Learning this is also learning [idempotency](idempotency.md), because a timeout leaves the outcome unknown, and retrying is only safe when repeating is harmless.
- Learning this is also learning [rate limiting and backpressure](rate-limiting.md), because both turn slow failure into fast failure, one on the caller's side and one on the server's.
- Learning this is also learning [feedback and control](../signals/feedback.md), because a circuit breaker is a control loop, and a careless one oscillates.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because a sensible timeout is set from the tail of the latency distribution, not its average.
- Learning this is also learning [round trips](../performance/round-trips.md), because a budget is spent one round trip at a time.

## Resources

1. Amazon Builders' Library, ["Timeouts, retries, and backoff with jitter"](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) (start here: short, and honest about the trade-offs).
2. Michael Nygard, *Release It!*, second edition (2018) (go deeper: stability patterns and anti-patterns, with stories).
3. Google, *Site Reliability Engineering*, ["Addressing Cascading Failures"](https://sre.google/sre-book/addressing-cascading-failures/) (reference: deadlines, retries and overload at scale).

## Names you'll hear

- **Timeout, deadline, deadline propagation:** how long to wait, and passing the remaining time along.
- **Circuit breaker: closed, open, half-open:** calling normally, failing fast, testing recovery.
- **Bulkhead:** a separate pool for one dependency.
- **Fallback, graceful degradation:** what to show when a part is missing.
- **Cascading failure:** one part's trouble spreading to the parts that depend on it.
- **Retry budget:** a cap on how much retrying is allowed.

## Go and look

Find three calls in something you run that go to another service, and find each one's timeout. If any of them is the library's default, find out what that default is. Then ask what the caller is holding on to while it waits.

Practise this: [the crawl](../exercises/design/web-crawler.md), where slow sites mustn't tie up the fetchers, and [the nearest car](../exercises/design/ride-hailing.md), where an unanswered offer has to expire.
