# Batch or stream

Last reviewed: 2026-11-27

A concept page: process data later, all at once, or as it arrives, one piece at a time. Batch is simpler and exact; stream is fast and harder. Most real systems need both, and the hard part of streaming is that data doesn't arrive in the order it happened.

## Problem

Data arrives continuously, and someone wants answers from it: totals, alerts, recommendations, bills. Waiting until the day is over and **transforming** everything in one run is simple, cheap and exact, because all the data is there and nothing changes underneath you. But the answer comes hours after the question mattered. Processing each record as it arrives gives answers in seconds, at the price of never quite having all the data: some of it is late, some arrives twice, and "the last ten minutes" turns out to have two meanings.

## The story

In 2016 Beatriz Lima led the fraud team at a digital bank in São Paulo. Every night at two o'clock, a job read the previous day's card transactions, scored each customer's activity against the patterns of known fraud, and blocked the cards that looked stolen. A batch job was the obvious design: the data was complete, the scoring could look at a whole day of a customer's history, and if the job failed it could simply be run again. Its decisions were good. The team rarely blocked an honest customer.

The trouble was the time. Fraudsters who copied a card in the afternoon used it that evening and overnight, as many times as they could, before the two o'clock run. One ring, operating for a fortnight, made forty or fifty purchases on each copied card between dinner and the small hours. The batch caught every one of those cards, the next morning, after the money had gone. The losses that year were the largest the bank had had.

So Beatriz's team built a stream: each transaction was scored as it arrived, in under a quarter of a second, before the payment was approved, against a running summary of the card's recent activity. One rule was simple: more than five purchases on one card in ten minutes was suspicious. In its first week, the stream blocked the cards of hundreds of honest bus passengers. The buses' card readers lost their mobile signal on parts of the route and sent the day's fares in a burst when they reconnected, so fifteen journeys made over six hours arrived in thirty seconds. To the stream, counting by when transactions arrived, that was fifteen purchases in ten minutes.

*Before reading on: the batch was right but too late, and the stream was fast but wrong. What had the stream misunderstood about time?*

Beatriz saw that there were two clocks in every transaction: when it happened, written by the card reader, and when it reached the bank. The batch had never noticed the difference, because by two in the morning every transaction from the day before had arrived. The stream lived in the gap between them. She changed the rules to count by when purchases *happened*, and gave each ten-minute window a grace period for stragglers: a window wasn't closed until the stream had good reason to think its late transactions had arrived, and anything later than that was handled separately rather than added to the wrong window.

She didn't throw the batch away. The stream made the decisions that couldn't wait, to approve or decline a payment now, and it worked from summaries that were nearly but not exactly right. The nightly batch still ran over the complete day, with every late transaction in place, and produced the numbers that had to be exact: the losses reported to the regulator, the customers' statements, and the check on how well the stream had done. When they disagreed, the batch won, and the disagreement was itself a measure of the stream's mistakes.

![Two panels. Top: a night's fraudulent purchases on copied cards, accumulating from evening until the two o'clock batch run blocks the cards; with stream scoring, each card is blocked after its first few purchases. Bottom: a bus's card reader, offline for six hours, sends fifteen fares at once when it reconnects; counted by arrival time they look like fifteen purchases in a moment, counted by when they happened they're spread across the day.](../images/figures/design-batch-or-stream.svg)

*A batch sees everything, late. A stream sees things as they arrive, which isn't the order they happened in.*

Looking back, Beatriz thought the question had never been batch or stream. It was which answers had to be fast and which had to be exact, and very few had to be both. The stream was for deciding; the batch was for the record.

## Where it shows up

| Page | The data, and when it's processed | What it taught |
| --- | --- | --- |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | Ruth's overnight jobs, then terminals that answered at once | Batch kept the machine busy; people wanted answers while they were still thinking about the question. |
| [Divide and conquer](../dsa/divide-and-conquer.md) | MapReduce, splitting a big job across many machines | Batch at scale: the data is complete, so it can be split, processed and combined. |
| [Append-only logs](../dsa/append-only-logs.md) | Teresa's ledger | A log of events can feed both: a stream reads it as it grows, and a batch rereads it from the start. |
| [Exact or approximate](../dsa/exact-or-approximate.md) | Dmitri's reader counts | Fast answers are often approximate; the exact ones can come later, from the full data. |
| [Asynchronous work and message queues](async-work.md) | Siobhán's resizing jobs | A queue of jobs is a stream of work, and the question of what to do when one is late or repeated is the same. |
| [State estimation](../signals/state-estimation.md) | Dorota's tractor, combining readings from different sensors | Every reading describes a moment already past; a good estimate accounts for when each one was taken. |

It shows up elsewhere too: a newspaper's print edition and its live web page, the day's takings counted after closing and the till's running total, the census and an opinion poll, and a weather forecast revised each hour and a climate record compiled once a year.

What the rows share is a choice between two promises. A batch promises an answer that's complete and correct, eventually. A stream promises an answer now, built from what has arrived so far. Knowing which promise each answer needs, and keeping both clocks apart, is most of the design.

## It really happened

Beatriz is fictional, and so is her bank. The arguments are real. In 2011 Nathan Marz proposed what he called the Lambda architecture: a batch layer that recomputes exact results from all the data, and a speed layer that covers the hours since the last batch with fast, approximate ones. In 2014 Jay Kreps, one of the creators of Kafka, questioned it, arguing that maintaining the same logic twice was a heavy burden, and that a stream processor reading from a durable log could do both jobs by replaying the log when the logic changed ([Kreps, "Questioning the Lambda Architecture"](https://www.oreilly.com/radar/questioning-the-lambda-architecture/)). Both designs are still in use.

The distinction between when an event happened and when it's processed was set out carefully in 2015 by Tyler Akidau and colleagues at Google, in the paper that became the basis of Apache Beam. It describes *event time* and *processing time*, windows defined by event time, and *watermarks*, a system's estimate that no more events before a given time are expected ([Akidau et al., "The Dataflow Model", VLDB 2015](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf)).

## What it is

**Batch processing** runs over a bounded set of data, such as yesterday's records, all at once; it's simple, efficient, repeatable and exact, and its answers are as old as the batch. **Stream processing** handles unbounded data record by record, keeping running state such as counts or recent history, and answers within seconds or less. Streams must handle **event time** (when something happened) separately from **processing time** (when it arrived), group events into **windows** by event time, decide when a window is complete using **watermarks**, and decide what to do with **late data**. They usually also need deduplication, since sources retry. Many systems run both: a stream for fast, provisional answers and a batch for exact ones, or a stream processor that can replay a durable log from the beginning to recompute.

## Where it gets misapplied

- **Counting by arrival time.** Late and bursty data lands in the wrong window; the bus passengers' fifteen fares.
- **A stream for answers nobody needs quickly.** A monthly report doesn't need second-by-second updates, and the complexity costs far more than a nightly job.
- **Treating the stream's answers as the record.** Fast answers are provisional; money and regulators need the exact ones.
- **Two copies of the logic, drifting apart.** The batch and the stream compute "the same" number differently, and nobody notices until they disagree in public.
- **The mirror:** a nightly batch for a decision that has to be made while the customer waits, such as approving a payment.

## Connections

- Learning this is also learning [append-only logs](../dsa/append-only-logs.md), because a durable log is what both a batch and a stream read from, and replaying it is how a stream recomputes.
- Learning this is also learning [exact or approximate](../dsa/exact-or-approximate.md), because fast answers are usually approximate, and the exact ones can arrive later.
- Learning this is also learning [divide and conquer](../dsa/divide-and-conquer.md), because batch processing at scale is splitting complete data and combining the results.
- Learning this is also learning [state estimation](../signals/state-estimation.md), because readings arrive after they were taken, and the time they were taken is what matters.
- Learning this is also learning [time and ordering](time-and-ordering.md), because event time and processing time are two clocks, and confusing them is the commonest streaming bug.
- Learning this is also learning [asynchronous work and message queues](async-work.md), because a queue feeding workers is a small stream, with the same late and repeated messages.

## Resources

1. Tyler Akidau, ["Streaming 101"](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/) (2015) (start here: event time, processing time and windows, with pictures). <!-- verify -->
2. Jay Kreps, ["Questioning the Lambda Architecture"](https://www.oreilly.com/radar/questioning-the-lambda-architecture/) (2014) (short: one pipeline or two).
3. Martin Kleppmann, *Designing Data-Intensive Applications*, chapters 10 and 11 (go deeper: batch and stream processing side by side).
4. Akidau et al., ["The Dataflow Model"](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf) (2015) (reference).

## Names you'll hear

- **Batch, stream:** bounded data processed all at once, or unbounded data processed as it arrives.
- **Event time, processing time:** when it happened, and when it was handled.
- **Window: tumbling, sliding, session:** fixed blocks, overlapping blocks, and bursts of activity.
- **Watermark, allowed lateness:** the estimate that a window is complete, and how long to wait beyond it.
- **Lambda and Kappa architectures:** two pipelines, batch and stream, or one stream that can replay.
- **Spark, Flink, Beam, Kafka Streams:** widely used processing systems.

## Go and look

Find a number on a dashboard you use that updates through the day. Find out whether it's computed as data arrives or in a periodic batch, and whether yesterday's value ever changes after the fact. If it never changes, ask what happens to data that arrives late.
