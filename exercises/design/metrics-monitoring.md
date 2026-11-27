# A million numbers a second

A design case in the category **writes at volume**. It draws on [batch or stream](../../design/batch-or-stream.md), [partitioning](../../data/partitioning.md), [distributions and percentiles](../../math/percentiles.md) and [exact or approximate](../../dsa/exact-or-approximate.md).

## The situation

A company runs about 20,000 servers and a few hundred services, and its engineers want to see how every one of them is doing: requests per second, errors, how long requests take, memory, disk. They want charts that update every ten seconds, alerts that fire within a minute of something going wrong, and a year of history to compare against. The first version had every server write its numbers into a relational database every ten seconds. It fell over within a month, and on the day of the company's worst outage, the monitoring was down too.

## Requirements and numbers

- Each server reports about 500 different measurements every 10 seconds: counters, gauges, and request durations.
- Charts and alerts within about a minute; the slowest 1% of requests (the 99th percentile) must be shown, not just averages.
- Query any service's numbers over the last hour in under a second, and over the last year in a few seconds.
- Keep a year of history.
- Keep working when the systems it watches are failing.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** Small numbers, written constantly, almost never changed, mostly read as recent ranges.
- **What breaks at ten times?** The number of distinct series, more than the number of points.
- **How does it fail?** Monitoring that shares a fate with what it monitors goes dark exactly when it's needed.

## The tempting first design

One table: server, measurement name, time, value. Every server inserts its 500 rows every ten seconds. Charts select a range and group by minute. Durations are recorded as an average per server per ten seconds.

20,000 servers × 500 numbers every 10 seconds is a million rows a second, into one table with indexes that every insert has to update. A year is about 30 trillion rows. And averages of request times can't be combined into a percentile: the 99th percentile of a service can't be worked out from each server's average, or even from each server's own 99th percentile.

## Hints

<details markdown="1"><summary>Hint 1</summary>

A series is one measurement from one source over time. The points in a series arrive in time order and are very similar to each other. How could you store them so that writing is cheap and they take little space?

</details>

<details markdown="1"><summary>Hint 2</summary>

Nobody looks at last March's numbers ten seconds at a time. What could you keep instead of every point, once data is old?

</details>

<details markdown="1"><summary>Hint 3</summary>

To combine durations from many servers into one percentile, each server has to report something that can be added up. What summary of a set of durations can be merged with another?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

20,000 servers × 500 measurements is 10 million series, each with a point every 10 seconds: a million points a second. At 16 bytes a point, raw, that's about 16 megabytes a second, about 1.4 terabytes a day, and about 500 terabytes a year. Time series compress extremely well, often to one or two bytes a point, because consecutive values and timestamps are close together, which brings a year down to tens of terabytes before any summarising ([estimates](../../design/estimates.md)).

### Design A: a time-series store, partitioned by series

- **Series, not rows.** Each series is identified by its name and labels, such as `requests{service=checkout, server=web-14}`, and its points are appended in time order into compressed blocks, two hours at a time. Writes are appends to memory, flushed in bulk ([append-only logs](../../dsa/append-only-logs.md), [LSM trees](../../dsa/lsm-trees.md)).
- **Partitioned by series.** Series are spread across storage nodes by hashing their names, so a million points a second is shared by many machines, and each is copied to a second node ([partitioning](../../data/partitioning.md), [replication](../../data/replication.md)).
- **Summaries for old data.** After two days, ten-second points are rolled up into one-minute summaries (minimum, maximum, sum, count); after a month, into hourly ones. A year of history then takes a small fraction of the raw space, at the cost of detail nobody uses.
- **Histograms, not averages.** Servers report request durations as counts in fixed buckets (under 10 ms, under 25 ms, and so on). Buckets from many servers add up, so a service's 99th percentile can be estimated from the summed histogram, with a known error set by the bucket edges ([distributions and percentiles](../../math/percentiles.md), [exact or approximate](../../dsa/exact-or-approximate.md)).
- **Alerts as a stream.** Alert rules are evaluated every few seconds against the newest points as they arrive, not by querying the store ([batch or stream](../../design/batch-or-stream.md)).
- **Separate fate.** The monitoring runs on its own machines and network path, and a second, much simpler monitor watches the monitoring.

**What it costs:** detail is lost on purpose as data ages, and percentiles are estimates with a stated error.

### Design B: collect events, compute later

Instead of numbers, services send an event for every request, with its duration and labels, into a log; queries and dashboards compute counts and percentiles from the events, sampled when volume is high.

**What it gives:** any question can be asked afterwards, including ones nobody thought of, such as "the slowest requests from one customer".

**What it costs:** far more data, since a busy service makes millions of requests a minute, so in practice heavy sampling, and slower, costlier queries. Many companies run both: metrics for dashboards and alerts, sampled events for investigating.

</details>

## What breaks at ten times the size

- **Too many series.** Adding a label like a customer ID or a request ID turns one series into millions; limit labels to things with few values.
- **The query that reads a year.** Without the summaries, it reads every point; with them, a few thousand.
- **The store itself.** At ten million points a second, ingestion needs its own buffering, such as a log in front of the store, so that a slow node doesn't drop data.

## Where people slip

- **Averaging percentiles.** The average of each server's 99th percentile is not the service's 99th percentile; merge histograms instead.
- **Unbounded labels.** One label with a user ID in it multiplies the number of series by the number of users.
- **Keeping every point for ever.** Nobody needs last year at ten-second resolution.
- **Monitoring on the same infrastructure it watches.** It fails at the moment it's needed.

## Related

- The other case in this category: [every click, once](ad-click-counter.md), an ad-click counter that bills.
- Design pages: [batch or stream](../../design/batch-or-stream.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [distributions and percentiles](../../math/percentiles.md), [exact or approximate](../../dsa/exact-or-approximate.md), [partitioning](../../data/partitioning.md), [LSM trees](../../dsa/lsm-trees.md), [sampling and observation](../../info/observation.md), [11, Software that must not go down](../../11-software-that-must-not-go-down.md).
