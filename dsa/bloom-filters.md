# Bloom filters

Last reviewed: 2026-11-10

A concept page: a small memory summary that can rule out an item, but cannot prove it is present.

## Problem

Sometimes the expensive question is whether an item might be in a large collection: whether a URL has been seen, a key is in a disk file, or a username exists. Keeping every key in fast memory may cost too much, while checking the slow store every time costs too much time. A Bloom filter trades a small chance of an unnecessary check for far fewer checks overall.

## The story

In 2017, Priya maintained a web crawler that checked a disk-backed index before fetching each URL. Most candidate URLs were new, but checking even a new one meant a random disk read. The crawler spent more time asking whether it had seen a page than downloading pages.

Priya could keep the whole index in memory, but it was already larger than the machine's memory. She instead kept a compact bit array. For each URL in the index, several hash functions chose positions in the array, and she set those bits. To check a candidate, she looked at the same positions. If any bit was clear, the URL definitely was not in the index. If all were set, it might be there, so she still checked the disk.

Some new URLs had all their bits set by other URLs. Those were false positives: a few extra disk reads, not missed pages. Priya measured the rate, enlarged the bit array, and reduced the unnecessary reads until the trade was worth the memory.

Looking back, Priya thought the useful part was not that the filter answered membership questions. It could not answer them exactly. Its value was that it cheaply ruled out most of the items that would otherwise trigger an expensive exact check.

## Where it shows up

| Page | The collection | What the filter saves |
| --- | --- | --- |
| [LSM trees](lsm-trees.md) | Keys in sorted files on disk | Skips reading files that definitely cannot contain a key. |
| [Hashing](hashing.md) | A set of keys mapped to bits | Reuses hashes to summarize many keys in little space, accepting occasional false positives. |

It also shows up in web crawlers, databases, and distributed systems that want to avoid an expensive lookup when an item is absent.

What these share is an asymmetric cost: a false alarm is acceptable, but saying "absent" when the item is present is not. A Bloom filter is useful only when the system can tolerate extra checks and must not treat a possible match as proof.

## It really happened

Burton Bloom introduced the structure in 1970 to save computer space when testing whether a word belonged to a set. Google's Bigtable paper later described using Bloom filters to reduce disk reads for queries on its sorted files. In both cases the filter is a hint: a possible match still needs an exact check.

## What it is

A Bloom filter is a bit array with several positions chosen by hash functions. Inserting an item sets its positions; testing an item returns "definitely absent" if any position is clear, and "possibly present" otherwise. It has no false negatives when used correctly, but can have false positives. More bits per item lower the false-positive rate; adding too many items raises it. A standard Bloom filter cannot remove individual items, because clearing a shared bit could make another item appear absent.

## Where it gets misapplied

- **Treating a possible match as proof.** Check the exact store before acting on membership.
- **Sizing it once and forgetting it.** As more items are inserted, false positives rise; rebuild or replace the filter before it stops saving work.
- **Using it when false positives are costly.** A security decision or a billing decision needs an exact answer.
- **The mirror:** keeping a huge exact set in memory when the filter only needs to prevent most slow misses.

## Connections

- Learning this is also learning [LSM trees](lsm-trees.md), because their filters avoid disk reads for keys that cannot be in a file.
- Learning this is also learning [hashing](hashing.md), because hashes choose the bits that summarize each item.
- Learning this is also learning [caching](../latency/caching.md), because both trade memory for fewer expensive reads, but a cache stores answers while a Bloom filter stores only a lossy membership summary.

## Resources

1. Burton H. Bloom, ["Space/Time Trade-offs in Hash Coding with Allowable Errors"](https://dl.acm.org/doi/10.1145/362686.362692), *Communications of the ACM* (1970) (the original paper).
2. Chang et al., ["Bigtable: A Distributed Storage System for Structured Data"](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/) (2006) (a production use in storage).
3. RocksDB, [Bloom Filter](https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter) (reference: practical options and trade-offs).

## Names you'll hear

- **False positive:** the filter says "possibly present" for an absent item.
- **False negative:** the filter says "absent" for an item that is present; a correctly maintained Bloom filter does not do this.
- **False-positive rate:** the share of absent-item checks that trigger an unnecessary exact lookup.
- **Counting Bloom filter:** a variant that uses counters instead of bits so items can be removed, at greater memory cost.

## Go and look

Find a slow lookup in something you work on and measure how often it asks about an item that is absent. Would a false positive merely cost one extra lookup, or could it change a decision?
