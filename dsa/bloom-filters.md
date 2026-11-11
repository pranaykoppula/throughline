# Bloom filters

Last reviewed: 2026-11-11

A concept page: a tiny summary of a set that can say "definitely not in here" for certain, and "possibly in here" with a known chance of being wrong. It's useful as a cheap first test before an expensive exact one, and dangerous as the final answer.

## Problem

Many systems spend most of their time asking whether something is in a large collection: has this page been crawled, is this key in that file, is this address on the blocklist? Keeping the whole collection in fast memory can cost too much, and checking the slow, exact copy every time costs too much time. A Bloom filter keeps a summary small enough to hold in memory. The price is that its "yes" can be wrong. Everything depends on what you do with that "yes".

## The story

In 2010 Joaquín Duarte ran the web crawler for a price-comparison site. Each day the crawler found hundreds of millions of links and had to skip the pages it had already fetched that day. At first it kept every URL it had seen in an in-memory set: exact, fast and simple. Then the crawl grew past what the machines' memory could hold, and checking a database on disk for every link slowed everything down badly.

A colleague suggested a Bloom filter. For each URL seen, a few hash functions picked positions in a large array of bits, and those bits were set to one. To test a new URL, the crawler looked at its positions. If any bit was zero, the URL had certainly never been seen. If all were one, it had probably been seen, though other URLs might have set those bits by chance. Sized for the expected crawl, the filter fitted in a fraction of the memory and gave a wrong "probably seen" about one time in a hundred. Joaquín decided the crawler would simply skip any URL the filter said it had probably seen. Missing one new page in a hundred seemed a fair price for a crawl that was fast again, and it was.

Over the next year the site added shops in three more countries, and the crawl tripled. Nobody resized the filter. As more URLs set more bits, more new URLs found all their bits already set, and the wrong answers rose from one in a hundred to about one in seven. The crawler raised no errors; skipped pages don't complain. The problem surfaced only when shops asked why their new products took weeks to appear on the site, and an analyst noticed that the newest products were missing far more often than old ones.

*Before reading on: the filter's "no" had been right every time, and its "yes" had been quietly wrong more and more often. What would you have changed?*

Joaquín kept the filter and changed what its answers were allowed to decide. A "no" still meant fetch the page straight away, with no further check, which was the case for most new links and where nearly all the saving came from. A "probably yes" now meant check the exact list on disk before skipping. The filter's mistakes became an extra disk read, not a missing product. He sized the filter for twice the current crawl, and started a fresh filter each day, so it never filled up and old entries never needed deleting. And because the failure had been silent, he made it visible. Every hour the crawler tested the filter with a sample of URLs it knew were new and recorded how often it wrongly answered "probably yes". When that rate rose, the dashboard showed it.

Looking back, Joaquín thought the filter had never lied about "no". Its "yes" had only ever been a hint, and he'd let a hint make a final decision. The filter's job was to make most questions cheap, not to answer the hard ones.

## Where it shows up

| Page | The cheap first test | What it was trusted with |
| --- | --- | --- |
| [LSM trees](lsm-trees.md) | Neha's filter on each file of sorted keys | Ruling files out, so a read checks only the few that might hold the key; a "maybe" still means reading the file. |
| [Computability](computability.md) | Viktor's virus scanner | Living with an imperfect test: antivirus accepts false alarms and misses as the price of answering at all. |
| [Sampling and observation](../info/observation.md) | Kofi's dashboard | The cost of a silent failure: skipped pages, like a dead sensor, raised no alarm until someone looked. |

It shows up elsewhere too: databases such as Cassandra and RocksDB, which keep a filter per file; browsers checking addresses against lists of dangerous sites; spam and fraud systems running fast checks before slow ones; and, beyond computing, medical screening tests, which are designed to miss as few cases as possible and send every positive for a more careful test.

What these share is a cheap test with a lopsided error. When it says "no", you can act on it at once. When it says "yes", you've only learned that the expensive question is worth asking. Systems go wrong when the "yes" is allowed to stand in for the answer, or when nobody watches how often it's wrong as the collection grows.

Motif: [a cheap check before an expensive one](../motifs.md#a-cheap-check-before-an-expensive-one).

## It really happened

Joaquín is fictional; the structure and its uses are real. Burton Bloom described it in 1970 as a way to save memory when an occasional wrong "yes" was tolerable, at a time when memory was scarce and checks were done against slow storage ([Bloom, *Communications of the ACM*](https://dl.acm.org/doi/10.1145/362686.362692) <!-- verify -->). Google's Bigtable paper (2006) described keeping Bloom filters for its sorted files so that most reads for missing data never touched the disk ([Chang et al.](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/)), and later storage engines did the same.

The trade can also be undone when circumstances change. Chrome's Safe Browsing check, which tests visited addresses against Google's lists of dangerous sites, kept those lists locally as a Bloom filter. In 2011 its engineers added an exact compressed structure they called a prefix set. On their data it used less memory than the Bloom filter and gave no false matches at that stage, and they ran the two side by side, comparing results, while they switched ([Chromium code review](https://codereview.chromium.org/6286072) <!-- verify -->).

## What it is

A Bloom filter is a bit array with several hash functions. Adding an item sets the bits at its hashed positions. Testing an item returns "definitely absent" if any of its bits is zero, and "possibly present" if all are one. It never gives a false "absent" for an item that was added, but it gives false "present" answers at a rate set by the number of bits, the number of hash functions and the number of items added; the rate rises as the filter fills. A standard filter can't delete items, because clearing a bit might erase evidence of another item; variants such as counting filters can, at a cost in memory. Its use is as a cheap first test in front of an exact one.

## Where it gets misapplied

- **Treating "possibly present" as "present".** Joaquín's skipped pages. Act on the filter's "no"; check its "yes" whenever being wrong matters.
- **Sizing it once and forgetting it.** The false-positive rate rises as items are added, without any error to say so. Size for growth, rebuild or rotate, and measure the rate.
- **Using it where a false "yes" is costly and can't be checked.** Access decisions, billing and anything legal need the exact answer.
- **The mirror:** keeping a huge exact set in memory when nearly all the lookups are for things that aren't there. The cheap "no" is exactly what a filter is for.

## Connections

- Learning this is also learning [hashing](hashing.md), because a filter is several hashes of each key, packed into one shared array of bits.
- Learning this is also learning [LSM trees](lsm-trees.md), because a filter per file is what keeps their reads fast.
- Learning this is also learning [caching](../latency/caching.md), because both keep something small in memory to avoid slow reads, but a cache remembers answers and a filter only remembers what's certainly absent.
- Learning this is also learning [observation](../info/observation.md), because a filter that's filling up fails silently, and only a measurement you set up will show it.
- Learning this is also learning [statistical significance](../math/statistics.md), because false positives and false negatives are a trade-off you choose, and the right balance depends on what each mistake costs.

## Resources

1. Burton H. Bloom, ["Space/Time Trade-offs in Hash Coding with Allowable Errors"](https://dl.acm.org/doi/10.1145/362686.362692), *Communications of the ACM* (1970) (start here: short, and the motive is on the first page). <!-- verify -->
2. Chang et al., ["Bigtable: A Distributed Storage System for Structured Data"](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/) (2006) (go deeper: a filter in a production storage system).
3. RocksDB, ["RocksDB Bloom Filter"](https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter) (reference: sizing and the practical trade-offs). <!-- verify -->

## Names you'll hear

- **False positive, false negative:** a wrong "yes" and a wrong "no"; a Bloom filter has only the first.
- **False-positive rate:** how often an item that was never added tests as "possibly present".
- **Bits per item, hash functions:** the two settings that decide the rate.
- **Counting Bloom filter:** a variant with small counters instead of bits, so items can be removed.
- **Cuckoo filter, prefix set:** newer alternatives with different trade-offs.

## Go and look

Find a fast check in something you run that sits in front of a slower one, such as a cache, a filter or a blocklist. Write down what happens when it says "yes" wrongly, and find out whether anyone measures how often it does.
