# Every click, once

A design case in the category **writes at volume**. It draws on [batch or stream](../../design/batch-or-stream.md), [idempotency](../../design/idempotency.md), [exact or approximate](../../dsa/exact-or-approximate.md) and [partitioning](../../data/partitioning.md).

## The situation

An advertising network places ads for local businesses on thousands of websites, and charges each advertiser for every click. Advertisers watch a dashboard during the day and expect it to be up to date within a minute. Each campaign has a daily budget, and once it's spent the network must stop showing that campaign's ads, or give the clicks away free. At the end of the month each advertiser gets an invoice, and some of them check it. The network also has a fraud team, whose systems find bots' clicks up to three days later, and those clicks must not be billed.

## Requirements and numbers

- Count clicks per campaign, per minute and per day.
- Dashboards within about a minute; a small error, say 1%, is acceptable there.
- Budgets enforced within a minute or so.
- Invoices exact, explainable click by click, and without fraudulent clicks found up to three days later.
- About 1.5 billion clicks a day, with a peak of about 50,000 a second. One large chain of shops accounts for a fifth of all clicks.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** A flood of small, immutable events, some of them duplicates, some fraudulent, many arriving late from phones with poor connections.
- **Which answers must be fast, and which exact?** Not the same ones.
- **What breaks at ten times?** Any single counter that every click touches.

## The tempting first design

A table with one row per campaign per day, and a click handler that adds one to the right row. The dashboard reads the rows; the invoice sums them.

At 50,000 clicks a second, the rows of the biggest advertiser are updated 10,000 times a second, and every update waits for the one before. A browser that retries a click because the first request was slow adds a second click. A bot's click found on Thursday can't be taken out of Monday's count, because the count doesn't remember which clicks made it. And an advertiser who questions the invoice can be shown only a number.

## Hints

<details markdown="1"><summary>Hint 1</summary>

To explain an invoice and remove fraud later, what do you need to keep: counts, or clicks?

</details>

<details markdown="1"><summary>Hint 2</summary>

The dashboard and the budget need an answer in a minute; the invoice needs it to be right. Do they have to come from the same calculation?

</details>

<details markdown="1"><summary>Hint 3</summary>

A retried click and a genuine second click look alike when they arrive. What would make them different, and when would it have to be created?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

1.5 billion clicks a day is about 17,000 a second on average, and the peak is about three times that. At about 200 bytes per click, the raw events are about 300 gigabytes a day, or about 9 terabytes a month: too much for one ordinary database, easy for a partitioned log and cheap storage ([estimates](../../design/estimates.md)).

### Design A: a stream for speed, a batch for money

- **A click ID, made when the ad is shown.** Each ad served carries a unique, signed ID. A click carries it back, so a retried click has the same ID as the original and can be recognised ([idempotency](../../design/idempotency.md)).
- **Keep every click.** Click events are written to a durable, partitioned log and kept as the record, in cheap storage, for as long as invoices can be disputed ([append-only logs](../../dsa/append-only-logs.md)).
- **The stream: fast and nearly right.** A stream job reads the log, drops duplicates it has seen in the last hour, and counts per campaign per minute by **when the click happened**, not when it arrived ([batch or stream](../../design/batch-or-stream.md)). Its counts feed dashboards and budget checks. They're allowed to be slightly off.
- **The batch: slow and exact.** Each night, a batch job reads the day's raw clicks, removes duplicates exactly, removes clicks the fraud team has flagged, and produces the counts that go on invoices. When the fraud team finds more bots three days later, the batch for that day is run again. The batch's numbers win; the difference from the stream's is reported, as a check on the stream.
- **Split the hot counter.** For the largest advertiser, the stream counts into several sub-counters chosen at random and adds them up when read, so no single counter takes a fifth of all traffic ([partitioning](../../data/partitioning.md)).

**What it costs:** two pipelines that must agree on what a click is, and so two places to keep in step when the rules change.

### Design B: one stream, replayed

A single stream processor keeps exact state: it stores every click ID it has seen in its state, writes counts to the output transactionally, and when the fraud rules or the code change, it replays the log from the beginning of the affected period to recompute.

**What it gives:** one set of logic, so the dashboard and the invoice can't disagree about what a click is.

**What it costs:** large state (at the peak, an hour of click IDs is over 100 million entries), harder operations, and replays that must be run carefully so they don't double-write invoices. It's the right choice when the team can run it well; Design A is easier to get right first.

</details>

## What breaks at ten times the size

- **Deduplication state.** Exact deduplication over a long window grows with traffic. In the stream, a [Bloom filter](../../dsa/bloom-filters.md) can stand in, accepting that it will sometimes drop a real click; in the batch, where money is involved, deduplicate exactly.
- **Late clicks.** More traffic from phones means more clicks arriving hours late; the stream needs a policy for lateness, and the batch has to wait long enough.
- **Budgets.** At ten times the rate, a minute's delay lets a campaign overspend noticeably; budget checks may need their own faster, approximate counter.

## Where people slip

- **Counting by arrival time.** Clicks from phones arrive late and in bursts, and land in the wrong minute.
- **No click ID.** Retries look like new clicks, and the invoice is wrong.
- **Throwing away the raw clicks.** Fraud found later can't be removed, and invoices can't be explained.
- **One counter for everything.** The hottest key sets the speed of the whole system.
- **Using approximate structures for money.** A Bloom filter's false positives are fine on a dashboard and not on an invoice.

## Related

- The other case in this category: a metrics and monitoring system (coming in a later batch).
- Design pages: [batch or stream](../../design/batch-or-stream.md), [idempotency](../../design/idempotency.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [exact or approximate](../../dsa/exact-or-approximate.md), [Bloom filters](../../dsa/bloom-filters.md), [partitioning](../../data/partitioning.md), [append-only logs](../../dsa/append-only-logs.md).
