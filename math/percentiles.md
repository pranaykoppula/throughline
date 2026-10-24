# Distributions and percentiles

Last reviewed: 2026-10-24

A concept page: why the average hides the cases people actually feel.

## Problem

A single number, usually the average, is the natural way to summarise how fast or how reliable something is. But users don't experience the average. Each of them experiences one request, and enough of them land in the slow tail that the tail decides how the product feels.

## The story

In 2004 Leo Marsh was responsible for the speed of a search startup's results page. His dashboard showed one number: average response time, two hundred milliseconds. It had been flat for months. The founders were happy with it.

The support inbox wasn't. Every week a few people wrote that search was "sometimes painfully slow". Leo tried it himself, again and again, and it was always quick. He put the complaints down to people's own internet connections.

One evening, out of stubbornness, he logged every request for an hour and sorted them by time taken. Half finished within 120 milliseconds. Ninety percent within 300. But the slowest one in a hundred took more than three seconds, and the slowest one in a thousand took over eight. The average had swallowed them. A handful of eight-second requests barely moved a mean that millions of fast ones were holding down.

Then he worked out what it meant for a real page. Each results page asked twenty backend servers for pieces of the answer and waited for all of them. If each server was slow one time in a hundred, the chance that at least one of the twenty was slow was almost one in five. Leo had been measuring each server and calling it fine. Nearly a fifth of the people using his search were waiting seconds.

*Before reading on: the average was fine, and one page in five was slow. What would you have measured instead, and what would you have done about the slow ones?*

He replaced the average on the dashboard with three numbers: the time within which half, ninety-five percent and ninety-nine percent of requests finished. The founders found the third number alarming, which was the point. Then he went after the tail directly. Most slow responses came from a server that was briefly busy with something else, so when a backend took noticeably longer than usual, the page sent the same request to a second copy and used whichever answered first. It cost a few percent more traffic. The ninety-ninth percentile fell from three seconds to four hundred milliseconds.

Looking back, Leo thought the average had been an honest number that answered the wrong question. Nobody experiences an average. Each person gets one draw from the distribution, and the more pieces a page depends on, the more likely they draw from its worst end.

## Where it shows up

| Page | The distribution | What the average hid |
| --- | --- | --- |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Followers per account | The average account was fine for precomputed feeds. The champion, far out in the tail, broke them. |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Checkout success by customer group | 99.95% overall hid customers in Brazil, on one card, on Android, all failing. |
| [Queueing](../latency/queueing.md) | Waiting times near full capacity | The average wait looked acceptable while the unluckiest waited minutes. |

It shows up elsewhere too: response times on every dashboard, file sizes, how many items customers buy, and how often each key in a cache is read.

The pages show two different tails. One is a long tail of *values*, where a few accounts or requests are far larger or slower than the rest, as with Maya. The other is a small *group* whose experience is very different from everyone else's, as with Rosa's Brazilian customers. Both disappear inside an average. Both are found by looking at the whole distribution, sliced in more than one way.

## It really happened

Leo is fictional; his arithmetic is the subject of a famous paper. Jeffrey Dean and Luiz André Barroso of Google wrote in 2013 that if a server is slow one time in a hundred and a request needs answers from a hundred such servers, about 63% of requests will be slow. Their remedies included sending a second copy of a slow request, as Leo did ([summary of "The Tail at Scale"](https://blog.acolyer.org/2015/01/15/the-tail-at-scale/)). Amazon's Dynamo paper (2007) set its performance targets at the 99.9th percentile rather than the average, for the same reason ([page 8](../08-too-many-users-too-much-data.md)).

## What it is

A distribution is the full spread of values something takes. A percentile is a point in it: the 99th percentile is the value that 99% of cases are at or below. Averages describe the middle and are pulled very little by rare extremes, so they hide tails. Measure several percentiles, slice by group as well as overall, and remember that a request depending on many parts inherits the worst of them.

## Where it gets misapplied

- **Averages on dashboards.** Leo's flat two hundred milliseconds.
- **Averaging percentiles.** The average of each server's 99th percentile isn't the 99th percentile of the whole; you need the raw data or a proper summary of it.
- **Only one slice.** A fine overall number can hide one group's terrible one.
- **The mirror:** chasing the single slowest request ever recorded. Some outliers are noise. Decide which percentile matters to users and work on that.

## Connections

- Learning this is also learning [queueing](../latency/queueing.md), because queues are what turn small variations into long tails.
- Learning this is also learning [statistical significance](statistics.md), because telling a real difference from noise is the next question after "what does the distribution look like?"
- Learning this is also learning [hashing](../dsa/hashing.md), because skewed keys are a long tail too, and they decide where hot spots form.
- Learning this is also learning [profiling](../tooling/profiling.md), because a profile of averages can hide the slow cases users feel.
- Learning this is also learning [round trips](../latency/round-trips.md), because the more calls a page waits on, the more it pays for each one's tail.

## Resources

1. Dean and Barroso, "The Tail at Scale" (*CACM*, 2013), or [Adrian Colyer's summary](https://blog.acolyer.org/2015/01/15/the-tail-at-scale/) (start here).
2. Gil Tene, "How NOT to Measure Latency" (talk) (go deeper: the common mistakes, including averaging percentiles).
3. Google, [*Site Reliability Engineering*](https://sre.google/sre-book/table-of-contents/), the chapter on service level objectives (reference). <!-- verify -->

## Names you'll hear

- **p50, p95, p99:** the 50th, 95th and 99th percentiles. p50 is the median.
- **Tail latency:** the slow end of the response-time distribution.
- **Long tail, heavy tail:** distributions where rare values are far larger than typical ones.
- **Hedged request:** sending a backup copy of a slow request, Leo's fix.
- **Histogram:** counts of values in ranges, the usual way to store a distribution without keeping every value.

## Go and look

Find a latency chart for something you run. If it shows only an average, find the 99th percentile. If it shows percentiles, slice them by one dimension you've never checked: country, device, or customer size.
