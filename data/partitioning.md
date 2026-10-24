# Partitioning

Last reviewed: 2026-10-24

A concept page: splitting data across machines when one machine can't hold or serve it all.

## Problem

Copies spread reads, but every copy still holds everything and takes every write. When the data or the writes outgrow one machine, the data has to be split, with each machine owning a slice. Then every request has to find the right slice, slices have to be moved as machines are added, and one popular slice can overwhelm its machine while the rest sit idle.

## The story

In 2013 Maya's old colleague Sam, now running the database at a messaging app, finally had to split it. The main database was taking more writes than any single machine could handle. Sam chose the simplest rule he knew: four machines, and each user's messages lived on machine number *user ID mod 4*. Any server could compute where a user's data was without asking anyone. The load spread evenly. It worked well for a year.

Then the four machines filled up, and Sam needed a fifth. With *mod 5* instead of *mod 4*, almost every user's number pointed to a different machine. Adding one machine meant moving about four-fifths of all the data, while the app was running. He spent a month planning a migration he'd assumed would take a day.

Before he got to it, a second problem arrived. A celebrity joined, and her conversation with millions of fans lived on one machine, the one her ID happened to map to. That machine ran hot all day while the other four were bored. Splitting by user had spread users evenly. It hadn't spread *traffic* evenly.

*Before reading on: the split rule made adding machines move almost everything, and one popular user overloaded one machine. What would you have changed?*

Sam made two changes. First, instead of tying users directly to machines, he split the data into a large fixed number of small partitions, four thousand of them, each user hashed to one partition. A separate table recorded which machine held which partitions. Adding a machine meant moving a few hundred partitions onto it, about a fifth of the data, and updating the table. Nothing else moved. Second, he treated the handful of very large conversations differently. Their messages were split across several partitions by message ID, so no single machine carried them alone. It was more complicated to read, and it was only needed for a few hundred accounts.

Looking back, Sam thought the mistake had been choosing a rule that spread the data without thinking about how it would grow, or how unevenly people would use it.

## Where it shows up

| Page | The split | What it taught |
| --- | --- | --- |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | The step Maya hadn't taken yet | Copies spread reads; splits spread writes, and bring their own problems. |
| [Hashing](../dsa/hashing.md) | Choosing a partition by hashing the key | The placement job: fast and even, but `mod N` moves almost everything when N changes. |
| [Replication](replication.md) | Copies of each partition | Most large systems split the data and copy each slice. |
| [Access patterns](access-patterns.md) | Hot spots | Data spread evenly can still be used unevenly. |

It shows up elsewhere too: sharded databases, distributed caches, message queues split into partitions, and search indexes split across servers.

What these share is two questions every split has to answer: how do you find the right slice, and what happens when the number of slices, or their popularity, changes?

## It really happened

Sam is fictional. Instagram described a similar design in 2012: thousands of logical shards mapped onto far fewer physical database servers, so shards could be moved as the company grew, with IDs generated to include the shard they belonged to ("Sharding & IDs at Instagram", Instagram Engineering). Consistent hashing, from Karger and colleagues in 1997, is another answer to the *mod N* problem: adding a machine moves only a small share of keys ([paper](https://courses.e-ce.uth.gr/CE623/STOC_1997_Consistent_hashing.pdf)). Amazon's Dynamo used it for exactly that reason.

## What it is

Partitioning, or sharding, splits a dataset into pieces stored on different machines, usually by hashing or by ranges of a key. Good schemes make it cheap to find a key's partition, move only a little data when machines change, often by using many small partitions or consistent hashing, and handle hot keys that get far more traffic than others. Queries that span partitions get slower, so the key is chosen to keep common queries within one.

## Where it gets misapplied

- **`mod N` placement.** Even until N changes, then almost everything moves.
- **A key that splits the wrong way.** Sharding by user when most queries are by group means every group query visits every machine.
- **Ignoring hot keys.** Even data, uneven traffic.
- **The mirror:** sharding a database that fits comfortably on one machine. It adds every problem on this page and solves none you have ([page 8](../08-too-many-users-too-much-data.md)).

## Connections

- Learning this is also learning [hashing](../dsa/hashing.md), because the hash decides where each key lives.
- Learning this is also learning [replication](replication.md), because each partition usually has copies.
- Learning this is also learning [access patterns](access-patterns.md), because the right partition key follows the most common queries.
- Learning this is also learning [migrations](migrations.md), because moving partitions while the system runs is a migration.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because hot spots are the long tail of traffic per key.

## Resources

1. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapter 6, "Partitioning" (start here).
2. Karger et al., ["Consistent Hashing and Random Trees"](https://courses.e-ce.uth.gr/CE623/STOC_1997_Consistent_hashing.pdf) (1997) (go deeper).
3. Instagram Engineering, "Sharding & IDs at Instagram" (2012) (reference: a real design, briefly explained).

## Names you'll hear

- **Shard, partition:** one slice of the data.
- **Partition key, shard key:** what decides which slice a record belongs to.
- **Consistent hashing:** placement that moves few keys when machines change.
- **Rebalancing:** moving partitions between machines.
- **Hot spot, hot key:** a slice or key with far more traffic than the rest.
- **Scatter-gather:** sending a query to every partition and combining the answers.

## Go and look

If a database you use is sharded, find its partition key and check whether your most common query can be answered from one partition or has to ask them all.
