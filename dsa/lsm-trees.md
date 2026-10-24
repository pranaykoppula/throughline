# LSM trees

Last reviewed: 2026-10-24

A concept page: a storage structure that makes writes cheap by doing them later, in bulk.

## Problem

Indexes built as B-trees are good at reading, but each new record means finding its place and updating a page somewhere on disk. When writes arrive by the hundred thousand a second, all those small scattered updates become the bottleneck, however fast the disk.

## The story

In 2008 Neha Kapoor built the system that stored monitoring data at a hosting company: every server reported dozens of measurements every few seconds, a hundred and fifty thousand data points a second in total. She stored them in a well-known relational database, indexed by server and time. It was the obvious choice, and at first it was fine.

As the company grew, the database fell behind. Writes queued, the disks were busy all the time, and dashboards showed data from minutes ago. Neha looked at what the disks were doing. Each new data point meant updating the index, and the index was a B-tree spread across the whole disk. Points from thousands of servers arrived interleaved, so each update landed on a different page in a different place. The disk spent its time jumping around to change a few bytes here and a few bytes there.

*Before reading on: the disk was slow at many small scattered writes and fast at long sequential ones. How would you have arranged the writes?*

Neha changed the order of work. New data points went first into a sorted structure in memory, and into a plain log on disk in the order they arrived, so nothing was lost if the machine crashed. When the in-memory structure reached a few hundred megabytes, it was written out to disk in one long sequential write, as a sorted, unchangeable file. Writing became fast, because the disk only ever wrote long runs.

Reading got harder. To find a value, the system had to check memory and then several files on disk, newest first. Neha added a small summary to each file, a compact filter that could say "definitely not in here" without reading it, so most files could be skipped. In the background, a process merged the small files into fewer, larger ones, discarding overwritten values as it went.

That background merging caused the next problem. During heavy traffic, merging fell behind, the number of files grew, and reads slowed down. Neha tuned how often merges ran and how many files were allowed to pile up, and learned to watch merge backlog as closely as she watched disk space.

Looking back, Neha thought she'd learned that there's no free write. The B-tree paid for each write immediately, in scattered updates. The new design paid later, in merging, and in reads that had to look in several places. For a system that wrote far more than it read, paying later in bulk was the better deal.

## Where it shows up

| Page | The writes | The trade |
| --- | --- | --- |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Walter's nightly claims load with fourteen indexes | Every index made reads faster and each write slower; an LSM tree is a different answer to the same tension. |
| [B-trees](b-trees.md) | The structure LSM trees are usually compared with | B-trees favour reads and updates in place; LSM trees favour writes and append-only files. |
| [Access patterns](../data/access-patterns.md) | Write-heavy workloads | Monitoring, logging and event data, written constantly and read less often. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Data spread across many machines | The open-source stores descended from Dynamo, such as Cassandra, store data on each machine in LSM trees. |

It shows up elsewhere too: most time-series databases, many key-value stores, search engine indexes, and the storage underneath several distributed databases.

What these share is the same choice of when to pay for a write: now, in a scattered update, or later, in bulk.

## It really happened

Neha is fictional; the structure is from a 1996 paper by Patrick O'Neil and colleagues, "The Log-Structured Merge-Tree" (*Acta Informatica*). Google's Bigtable paper (2006) described the same pattern at scale: writes into an in-memory table, flushed into sorted immutable files and merged in the background. Google later released LevelDB, and Facebook built RocksDB on it; both are widely used storage engines. The small per-file filters Neha added are Bloom filters, described by Burton Bloom in 1970.

## What it is

A log-structured merge tree buffers writes in memory and in an append-only log, flushes them to disk as sorted, immutable files, and merges those files in the background. Writes are fast and sequential. Reads may check several files, helped by filters that rule files out cheaply. The cost moves into compaction, the background merging, which uses disk and processor time and must keep up with incoming writes.

## Where it gets misapplied

- **An LSM store for read-heavy data.** Every read may check several files; a B-tree is usually better when reads dominate.
- **Ignoring compaction.** A store that can't merge as fast as it writes slowly gets slower until it falls over.
- **Frequent updates to the same keys.** Old versions pile up until compaction removes them, using space in the meantime.
- **The mirror:** forcing a write-heavy firehose into a B-tree index because it's the default, and buying ever faster disks.

## Connections

- Learning this is also learning [B-trees](b-trees.md), because they make the opposite trade between reads and writes.
- Learning this is also learning [access patterns](../data/access-patterns.md), because the ratio of writes to reads decides which structure fits.
- Learning this is also learning [latency numbers](../latency/latency-numbers.md), because sequential disk writes are far faster than scattered ones.
- Learning this is also learning [replication](../data/replication.md), because the same append-only log that protects against crashes is often what's shipped to replicas.
- Learning this is also learning [queueing](../latency/queueing.md), because compaction is a background queue that has to keep up.

## Resources

1. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapter 3 (start here: LSM trees and B-trees side by side).
2. O'Neil et al., "The Log-Structured Merge-Tree" (1996) (go deeper).
3. Chang et al., "Bigtable: A Distributed Storage System for Structured Data" (OSDI 2006) (reference: the pattern at scale).

## Names you'll hear

- **Memtable:** the sorted in-memory buffer of recent writes.
- **SSTable:** a sorted, immutable file on disk.
- **Compaction:** merging files in the background.
- **Write-ahead log:** the append-only record that survives a crash.
- **Bloom filter:** a compact structure that can say "definitely not here" quickly.
- **Write amplification:** how many times each byte is rewritten as files are merged.

## Go and look

Find out which storage engine sits underneath a database you use, and whether it updates data in place or appends and merges. Then check whether your workload is mostly reads or mostly writes.
