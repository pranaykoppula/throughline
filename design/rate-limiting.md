# Rate limiting and backpressure

Last reviewed: 2026-11-27

A concept page: when more work arrives than a system can do, saying no early, clearly and fairly is kinder than saying yes and failing slowly. A limit protects the system, and it also protects every caller from the one caller who sends too much.

## Problem

A service that accepts every request seems generous, and for a while it is. But capacity is finite, and when demand passes it, the extra work doesn't vanish. It waits, in queues and buffers and threads, and while it waits, callers give up and retry, adding more work that will also be thrown away. The system ends up busy doing nothing useful. Somebody has to **decide** what to refuse, and the choice is only whether that happens by design, at the edge, or by accident, everywhere at once.

## The story

In 2019 Farida Rahimi ran the public API for a city's bike-share scheme in Lisbon. It answered two kinds of question. Anyone could ask which docking stations had bikes and spaces free, and the city published that openly, because the point was for other people's apps to use it. And the scheme's own app sent the request that unlocked a bike when a rider scanned it. Both went to the same servers and the same database.

Farida set no limits on the open data. It was public, it was free, and she didn't want to be the person who turned away a student's project. The servers ran on rented machines that added more of themselves as traffic grew. When a journey-planning app added bike availability, traffic doubled, and the system quietly scaled up. It was a reasonable design, and for a year it was the generous one.

Then a popular map app shipped an update with a mistake in it: every phone with the app open asked for every station's status once a second instead of once a minute. Traffic rose about forty times in an afternoon. The web servers multiplied, as designed, but the database behind them couldn't, and every request slowed. Phones whose requests took too long gave up and asked again straight away, which added more requests. By the evening rush, the database spent most of its time on answers nobody waited to receive. And riders standing at docks, scanning bikes to go home, waited thirty seconds and saw *Could not unlock*. The scheme's own most important request was failing behind a flood of status checks from someone else's bug.

*Before reading on: the open data was meant to be open, and the scaling had worked. What would you have changed?*

Farida kept the data open and free. What she changed was the promise. Every app now used a free key, and each key got a **token bucket**: tokens dripped in at a steady rate, a request took one, and a full bucket allowed a short burst. An app that went over got a quick, cheap answer straight away, *429 Too Many Requests*, with a header saying how many seconds to wait. The map app's bug now cost the map app's users, not everyone. She also stopped treating all work as equal. Unlocking a bike had its own budget, and when the database got busy, the servers began refusing status checks before they touched an unlock. And the queues in front of the database were given a fixed length: a request that couldn't start within a second was refused at once, instead of waiting until its caller had given up.

![A line chart of useful answers per second against requests arriving per second. Without limits, useful answers rise with demand up to the database's capacity of about 2,000 a second, then fall towards almost nothing as timeouts and retries take over. With limits and load shedding, useful answers rise to the same capacity and stay there, however much more arrives.](../images/figures/design-rate-limiting.svg)

*Past capacity, accepting everything doesn't do more work. It does less. Saying no early keeps the useful work at its maximum.*

Looking back, Farida thought her mistake had been to treat a limit as a refusal, when it was a promise. With no limits, nobody had been promised anything, and the riders had paid for a stranger's bug. With them, every app knew what it could count on, and the scheme knew it could always unlock a bike.

## Where it shows up

| Page | The limit, or the lack of one | What it taught |
| --- | --- | --- |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Lin's backups retrying into a congested network | Retrying harder made the collapse worse; TCP's fix was for senders to treat loss as a signal to slow down, which is backpressure built into a protocol. |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Rosa's ticket on-sales | A burst of demand many times the usual is predictable; deciding in advance who waits, and how they're told, is part of staying up. |
| [Queueing](../performance/queueing.md) | Signe's callers, and the ones who hung up and tried again | A queue near capacity grows without limit, and retries add to it. A bounded queue turns waiting into a quick no. |
| [Queues](../dsa/queues.md) | Yusuf's newsletters ahead of a password reset | Separate lines and guaranteed shares stop one big sender from holding up everyone else. |
| [Multi-tenancy](../security/multi-tenancy.md) | Chidi's customers sharing one database | Sharing is cheap only while each tenant is kept within bounds; a per-customer limit is that boundary for capacity. |
| [Feedback and control](../signals/feedback.md) | Loops that correct on old news | Telling callers to back off is a feedback loop, and if everyone retries at the same moment it oscillates. |

It shows up elsewhere too: motorway ramp meters that let one car on at a time so the main road keeps flowing, a club's one-in-one-out door, the engaged tone when a telephone exchange is full, and a hospital diverting ambulances when its emergency department can't take more.

What the rows share is a choice between two ways of failing. Without a limit, overload is everyone's problem and arrives as slowness. With one, it's the sender's problem and arrives as a clear answer, early and cheap, while the work that matters most keeps going.

Motif: [waiting is where the time goes](../motifs.md#waiting-is-where-the-time-goes).

## It really happened

Farida is fictional, and so is her bike scheme. The techniques are standard. In 2017 Stripe described the four limiters it ran on its payments API: a per-user token bucket on request rate, a limit on concurrent requests, and two load shedders that refused less critical traffic when the fleet or its workers were nearly full, so that critical requests such as creating charges kept working ([Stripe, "Scaling your API with rate limiters"](https://stripe.com/blog/rate-limiters)). Google's *Site Reliability Engineering* book describes the same ideas at larger scale: requests marked with how critical they are, servers shedding load by returning errors early, and clients that throttle themselves when many of their requests are being rejected, because even rejecting a request costs the server something ([Handling Overload](https://sre.google/sre-book/handling-overload/), [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)).

The answer Farida's apps received is part of HTTP. Status code 429, *Too Many Requests*, was defined in 2012, with the suggestion that servers include a Retry-After header saying how long to wait ([RFC 6585](https://www.rfc-editor.org/rfc/rfc6585)).

## What it is

Rate limiting caps how much work each caller can ask for in a period. A **token bucket** refills at a steady rate up to a maximum, so it allows bursts up to the bucket's size and a long-run average equal to the refill rate; a **leaky bucket** smooths output to a steady rate; fixed and sliding **windows** count requests per interval. **Concurrency limits** cap work in progress rather than arrival rate. **Load shedding** refuses work when the system as a whole is near capacity, best done by priority, so the least important work goes first. **Backpressure** is the general idea of a full stage telling the one before it to slow down, whether by a refusal, a bounded queue that blocks, or a protocol signal; it pushes the cost of overload back towards whoever is causing it. Clients that are refused should retry with **exponential backoff and jitter**, waiting longer each time and by a random amount, so that refusals don't turn into synchronised storms.

## Where it gets misapplied

- **An unbounded queue as a safety net.** It turns a short overload into a long one, full of work whose callers have already gone.
- **One limit for everything.** A global cap lets one noisy caller use it up; limits need to be per caller, and work needs priorities.
- **Refusing slowly.** A rejection that takes as long as a real answer protects nothing. Refuse early, before the expensive part.
- **Limits nobody can see.** Without a clear status code and a time to retry, clients guess, and they usually guess "now".
- **The mirror:** limits so tight they turn away the users the system exists for, or a limit standing in for capacity that should have been bought.

## Connections

- Learning this is also learning [queueing](../performance/queueing.md), because a limit is a decision about how long the line may get.
- Learning this is also learning [queues](../dsa/queues.md), because separate lines and fair shares are how one caller is kept from blocking the rest.
- Learning this is also learning [feedback and control](../signals/feedback.md), because backpressure is a correction loop, and retries without backoff make it oscillate.
- Learning this is also learning [multi-tenancy](../security/multi-tenancy.md), because many customers sharing one system need limits on capacity as well as on data.
- Learning this is also learning [load balancing](load-balancing.md), because spreading load evenly only helps while there's capacity left to spread it into.
- Learning this is also learning [back-of-the-envelope estimates](estimates.md), because knowing the peak tells you where the limit has to be.

## Resources

1. Stripe, ["Scaling your API with rate limiters"](https://stripe.com/blog/rate-limiters) (2017) (start here: four limiters, with the reasons for each).
2. Google, *Site Reliability Engineering*, ["Handling Overload"](https://sre.google/sre-book/handling-overload/) and ["Addressing Cascading Failures"](https://sre.google/sre-book/addressing-cascading-failures/) (go deeper).
3. Marc Brooker, ["Exponential Backoff and Jitter"](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) (2015) (short: why randomised retries matter).
4. [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585), section 4 (reference: status 429).

## Names you'll hear

- **Rate limit, quota, throttling:** a cap on how much a caller can ask for.
- **Token bucket, leaky bucket, sliding window:** ways of counting against the cap.
- **429 Too Many Requests, Retry-After:** the HTTP answer, and how long to wait.
- **Load shedding, graceful degradation:** refusing the least important work first when full.
- **Backpressure:** a full stage pushing back on the one before it.
- **Exponential backoff, jitter:** retrying later each time, at a random moment.
- **Retry storm, thundering herd:** many clients retrying at once.

## Go and look

Find the busiest API you call from something you've built. Find out what it does when you send too much: the status code, whether it says when to retry, and whether your code reads it. Then check what your own service does when it's full, and how long it takes to say so.

Practise this: [ten o'clock on Friday](../exercises/design/flash-ticket-sale.md), a waiting room in front of a sale thirty times oversubscribed.
