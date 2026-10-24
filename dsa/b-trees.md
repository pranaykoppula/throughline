# B-trees

Last reviewed: 2026-10-24

A concept page: the structure behind most database indexes, shaped by the cost of reading from disk.

## Problem

An index has to find any key among millions quickly, keep keys in order for range queries, and stay fast as keys are added and removed. On disk, the cost that matters isn't comparisons; it's how many separate reads it takes, because each read from a disk is thousands of times slower than working in memory.

## The story

In 1970 Leonard Fisk maintained the parts index for an aircraft manufacturer. Two million part numbers were kept sorted in a file on disk, and a lookup halved the file again and again until it found the part, about twenty-one steps. On paper that was efficient. In practice every step meant moving the disk's arm to a new place, and twenty-one seeks took most of a second. Adding a part meant rewriting everything after it to keep the order, so new parts were batched up and added once a week, and engineers spent the week asking about parts the index didn't have yet.

Leonard's first improvement was a binary tree. Each part number was a node, smaller numbers to the left, larger to the right, and a new part could be added by hanging it in the right place without rewriting anything. Inserts became instant. It was well reasoned, and it was the standard textbook answer.

It made lookups worse. Each node was stored wherever there was room on the disk, so every step down the tree was another seek, and the tree was over twenty levels deep. Then a new product line arrived, with part numbers issued in sequence: each new number larger than the last. Every one was hung to the right of the one before, and that branch of the tree became a single long chain. Finding the newest parts meant walking hundreds of thousands of nodes, one seek each.

*Before reading on: comparisons were cheap and disk reads were expensive, and the tree did one read per level. How would you have reshaped it?*

Leonard noticed that the disk read a whole block at a time, several thousand bytes, whether you wanted one part number or two hundred. So he stopped putting one key in each node. Each node became a full block holding a couple of hundred keys in order, with pointers between them to the nodes below. A lookup read one block, found where the part fell among its two hundred keys in memory, and followed one pointer down. With two hundred keys per node, three levels covered eight million parts. Three reads instead of twenty-one.

To stop the tree going lopsided, he never let a node get too full. When it did, it split into two half-full nodes and passed the middle key up to its parent. If the parent filled, it split too. The tree grew upwards from the root, a level at a time, and every leaf stayed the same distance from the top, whatever order the parts arrived in. Sequential part numbers just filled and split the rightmost nodes, neatly.

Looking back, Leonard thought the textbook tree had been designed for memory, where every node is equally cheap to reach. On a disk, the shape that mattered was set by the size of a block. Once he designed for that, the right structure was wide, shallow, and always balanced.

## Where it shows up

| Page | The index | What it did |
| --- | --- | --- |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Walter's index on the hospital column | Turned a forty-minute scan into under a minute, and made every new claim slower to write. |
| [1, One machine, one program](../01-one-machine-one-program.md) | The slow floor of the memory hierarchy | The reason B-trees exist: reads from the far tier are expensive, so make as few as possible. |
| [Hash tables](hash-tables.md) | The other way to find by key | Faster for single lookups, but with no order, so no ranges. |
| [Access patterns](../data/access-patterns.md) | Lookups, ranges, and steady inserts | A B-tree serves all three reasonably, which is why it became the default. |

It shows up elsewhere too: nearly every relational database's indexes, most file systems' directories, and many key-value stores.

What these share is one design principle: shape the structure for the cost of the medium it lives on.

## It really happened

Leonard is fictional; his employer's real equivalent was Boeing. Rudolf Bayer and Edward McCreight, at Boeing Scientific Research Laboratories, described B-trees in a 1970 report, published in 1972 as "Organization and Maintenance of Large Ordered Indexes" (*Acta Informatica*). Within a decade Douglas Comer could title a survey "The Ubiquitous B-Tree" (*ACM Computing Surveys*, 1979), noting it had become the standard way to organise files ([Comer](https://users.cs.utah.edu/~pandey/courses/cs6530/fall24/papers/trees/p121-comer.pdf)). Nobody is quite sure what the B stands for; Boeing, balanced and Bayer have all been suggested.

## What it is

A B-tree is a balanced search tree whose nodes each hold many keys, sized to match a disk block or page. Lookups, inserts and deletes take a number of reads proportional to the tree's height, which stays very small because each node branches so widely. Nodes split when full and merge when sparse, keeping every leaf at the same depth. Keys stay in order, so range queries are efficient. The common variant, the B+-tree, keeps all values in the leaves and links the leaves together for fast scans.

## Where it gets misapplied

- **Indexing everything.** Each index is a B-tree that every write has to update ([page 4](../04-data-outlives-programs.md)).
- **Random keys on write-heavy tables.** Random identifiers scatter inserts across the whole tree, touching many pages; sequential ones fill one end.
- **A B-tree for very heavy write loads.** Structures that batch writes, like [LSM trees](lsm-trees.md), can absorb more.
- **The mirror:** avoiding indexes because they cost writes, and scanning millions of rows to find one.

## Connections

- Learning this is also learning [hash tables](hash-tables.md), because they make the opposite trade: faster single lookups, no order.
- Learning this is also learning [LSM trees](lsm-trees.md), because they give up some read speed for much cheaper writes.
- Learning this is also learning [latency numbers](../latency/latency-numbers.md), because the gap between memory and disk is the whole reason for the shape.
- Learning this is also learning [storage tiers](../cost/storage-tiers.md), because a B-tree is a small fast path into a large slow tier.
- Learning this is also learning [access patterns](../data/access-patterns.md), because whether an index helps depends on the queries actually run.

## Resources

1. Markus Winand, [*Use The Index, Luke*](https://use-the-index-luke.com/) (start here: B-tree indexes from the point of view of someone writing queries). <!-- verify -->
2. Douglas Comer, ["The Ubiquitous B-Tree"](https://users.cs.utah.edu/~pandey/courses/cs6530/fall24/papers/trees/p121-comer.pdf) (1979) (go deeper: short and clear).
3. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapter 3 (reference: B-trees against LSM trees).

## Names you'll hear

- **Node, page, block:** the unit of storage a B-tree reads at a time.
- **Fan-out, branching factor:** how many children each node has; high fan-out keeps the tree shallow.
- **Split, merge:** how nodes stay neither too full nor too empty.
- **B+-tree:** the variant most databases use, with values in linked leaves.
- **Clustered index:** an index whose order is the order the table itself is stored in.

## Go and look

Ask the database you use to explain how it runs your slowest common query. Find whether it uses an index, which one, and how many rows it reads to return the answer.
