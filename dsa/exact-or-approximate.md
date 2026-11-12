# Exact or approximate

Last reviewed: 2026-11-12

A concept page: some questions don't need an exact answer, and a good-enough answer can cost a tiny fraction of the space and time. The skill is knowing which questions those are, saying how approximate the answer is, and never letting an estimate quietly become a fact someone is billed for.

## Problem

Counting is easy until it isn't. How many different people visited each page today? How often has each search term been used? What's the slowest one per cent of requests? Answering exactly means remembering every item, and with millions of items across thousands of pages, the memory runs out before the day does. Many of these questions are asked to make decisions, where being within one per cent is plenty. But an approximate answer looks exactly like an exact one, and nothing stops it being used where only the exact one will do.

## The story

In 2016 Dmitri Sokolov built the analytics behind a news publisher's dashboards in Riga. Editors wanted to know, for each article, how many different readers it had reached today, this week and this month. Dmitri's first version kept, for each article and each day, the set of reader IDs that had opened it, and reported the size of the set. It was exact and simple. On a normal day it held about thirty million IDs. During an election week, with two thousand articles and readers clicking from article to article, the sets outgrew the server's memory, and the dashboard fell over on the night the editors most wanted it.

A colleague suggested a structure Dmitri hadn't heard of. Instead of remembering each reader, it ran each reader's ID through a hash and kept only a small summary of the hash values it had seen, built around how many leading zeros the rarest one had. Seeing the same reader twice changed nothing. From the summary, the number of different readers could be estimated to within about one per cent, using about twelve kilobytes per counter, however many readers there were. Better still, two summaries could be merged, so daily counters combined into weekly and monthly ones correctly, without double-counting readers who came back. Memory for the whole dashboard fell from tens of gigabytes to a few megabytes, and the election night went smoothly.

Six months later the commercial team, impressed with the dashboard, started using the same numbers to bill advertisers for "unique readers reached" by sponsored articles. One advertiser compared the bill with their own tracking and found it two per cent higher. The publisher's numbers were within the stated error. The advertiser didn't care about stated errors. They wanted to know why they had paid for eleven thousand readers who might not exist, and the publisher's lawyers wanted to know why its bills were estimates.

*Before reading on: the approximate count had done its job perfectly, and then started doing a different job. What would you have changed?*

Dmitri drew a line between two kinds of number. Numbers that guided decisions, which article to promote, which headline worked, could be approximate, and the dashboard now showed them with their error, "about 214,000 (±1%)", so nobody mistook them for exact counts. Numbers that money depended on had to be exact and reproducible. For those, every sponsored-article view was written to a log, and a nightly batch job counted distinct readers exactly, with time and disk to spare because it didn't have to answer in real time. The bills came from the batch; the dashboard came from the summaries. When the two were compared each morning, they agreed to within the stated error, which was itself a useful check.

Looking back, Dmitri thought the approximate counter had been one of the best decisions he'd made, and the worst thing about it was how exact it looked. An estimate needed its error shown next to it, and a list of the places it must never be used.

![A chart of memory against the number of different readers counted. Remembering every reader exactly grows in a straight line, from kilobytes to gigabytes. The approximate summary stays flat at about twelve kilobytes however many readers there are, with an error of about one per cent.](../images/figures/dsa-exact-or-approximate.svg)

*Exact counting grows with the readers; the approximate summary doesn't.*

## Where it shows up

| Page | The approximation | What it traded |
| --- | --- | --- |
| [Bloom filters](bloom-filters.md) | Joaquín's "possibly seen" | Memory for certainty about "yes", and the trouble came when a "yes" was trusted as final. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Maya's like counter for the champion | An exact count where exactness cost too much, approximated where nobody needed it to the last digit. |
| [Distributions and percentiles](../math/percentiles.md) | The slowest one per cent of requests | Percentiles over huge streams are usually computed from compact summaries, not every value. |
| [Sampling and aliasing](../signals/sampling.md) | Henrik's summaries per minute | A minute of readings reduced to a few numbers, with the raw data kept only when something looked unusual. |
| [Divide and conquer](divide-and-conquer.md) | Kwesi's distinct customers, which didn't add | Mergeable summaries are the approximate way out: they combine correctly without remembering every customer. |

It shows up elsewhere too: database query planners estimating how many rows a query will return, opinion polls, approximate "about 2,000,000 results" in search engines, trending topics, network monitoring of the heaviest traffic, machine learning in general, and the sampling behind every survey.

What these share is a trade of exactness for space or time, made deliberately. It works when the question is for a decision, the error is known and shown, and there's an exact path for the answers that money, law or safety depend on.

## It really happened

Dmitri is fictional. In 1977 Robert Morris at Bell Labs described *approximate counting*, a way to count up to very large numbers of events in a single byte by increasing the counter with decreasing probability. In 2007 Philippe Flajolet and colleagues published HyperLogLog, the distinct-count summary Dmitri used. Redis, the widely used in-memory database, added it in 2014: each counter uses at most 12 kilobytes and has a standard error of 0.81%, and counters can be merged ([Redis documentation](https://redis.io/docs/data-types/hyperloglogs) <!-- verify -->; [antirez, "Redis new data structure: the HyperLogLog"](https://www.antirez.com/news/75) <!-- verify -->). Many analytics databases offer an approximate distinct count alongside the exact one, and say so in its name.

## What it is

Approximate, or probabilistic, data structures answer questions with a known error in exchange for far less memory or time. Bloom filters answer membership with false positives; HyperLogLog estimates the number of distinct items; count-min sketches estimate how often each item appears; quantile sketches such as t-digest estimate percentiles; sampling estimates almost anything from a subset. Many are mergeable, so they combine across time windows or machines. The error is a parameter, chosen by the memory you give them. Approximate answers suit monitoring, dashboards and decisions; exact answers are still needed for billing, accounting, legal and safety uses.

## Where it gets misapplied

- **An estimate that looks exact.** "214,183 readers" with no error shown invites someone to bill for it.
- **Approximate numbers used for money, law or safety.** Dmitri's advertisers.
- **Combining summaries that don't combine.** Averages of percentiles are not percentiles; use summaries designed to merge.
- **The mirror:** insisting on exact counts for a dashboard nobody reads past two significant figures, and paying for gigabytes of memory to get them.

## Connections

- Learning this is also learning [Bloom filters](bloom-filters.md), because they're the approximate answer to "is it in the set?", with the same rule about trusting their "yes".
- Learning this is also learning [divide and conquer](divide-and-conquer.md), because mergeable summaries are what make distinct counts combine across pieces.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because percentiles over large streams are almost always estimated.
- Learning this is also learning [statistical significance](../math/statistics.md), because an approximate answer needs its error stated, like any measurement.
- Learning this is also learning [hashing](hashing.md), because most probabilistic structures rely on hashes spreading items evenly.

## Resources

1. antirez, ["Redis new data structure: the HyperLogLog"](https://www.antirez.com/news/75) (2014) (start here: a clear, practical explanation from the person who added it to Redis). <!-- verify -->
2. Philippe Flajolet and others, "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm" (2007) (go deeper).
3. Graham Cormode and Shan Muthukrishnan, "An Improved Data Stream Summary: The Count-Min Sketch and its Applications" (2005) (reference).

## Names you'll hear

- **Cardinality:** the number of distinct items.
- **HyperLogLog:** a small, mergeable summary that estimates cardinality.
- **Count-min sketch:** estimates how often each item appears.
- **t-digest, quantile sketch:** estimate percentiles from a stream.
- **Standard error:** how far an estimate typically is from the truth.
- **Mergeable summary:** one that combines across pieces without losing correctness.

## Go and look

Find a count on a dashboard you use and ask whether it's exact or estimated. If nobody knows, find out, and then check whether anyone uses that number for something that needs it exact.
