# Access patterns

Last reviewed: 2026-10-24

A concept page: how data is read and written decides how it should be stored.

## Problem

The same data can be stored many ways, and the right one depends entirely on how it will be used: read or written, often or rarely, one item at a time or many together, in what order. Storing data without asking those questions means paying for the wrong answer on every access.

## The story

In 1952 Arthur Benn ran the warehouse of a mail-order company in Kansas City. Orders arrived by post, each a list of items from the catalogue, and pickers walked the aisles with carts collecting them. The warehouse was arranged the way the catalogue was: by product number, from one end of the building to the other. It was tidy, logical, and easy to restock.

Arthur walked with the pickers for a week and kept a notebook. A typical order sent a picker from one end of the building to the other and back, often for small items. Most orders contained the same few hundred popular products, spread across the whole warehouse by the accident of their product numbers. The pickers walked about twelve miles a day, mostly past shelves nobody ordered from.

*Before reading on: the warehouse was arranged by product number, and the pickers walked miles. How would you have arranged it?*

Over a long weekend Arthur moved the three hundred most-ordered products to the shelves nearest the packing benches. The rest stayed in number order further back. Walking distance fell by more than half. Orders went out the same day instead of the next. He was congratulated at a board meeting.

In November the pickers started walking miles again. Christmas had arrived, and the products people ordered in November weren't the ones they'd ordered in June: toys, decorations, gift boxes, all at the back of the warehouse. Arthur's arrangement had been right for the summer and was wrong for the season that mattered most. He also noticed something new in his notebook. Certain items were almost always ordered together, like a lamp and its bulbs, and he'd placed them far apart.

He stopped thinking of the layout as something to get right once. Every quarter, he looked at what had actually been ordered and moved the fast-moving products forward. Items ordered together went side by side. The warehouse never stayed tidy again, and the pickers' walk stayed short.

Looking back, Arthur thought the mistake had been arranging the warehouse for how the stock was *catalogued* instead of how it was *ordered*. The second mistake had been assuming the orders wouldn't change.

## Where it shows up

| Page | The data | How it was really accessed |
| --- | --- | --- |
| [1, One machine, one program](../01-one-machine-one-program.md) | Joan's grid, stored row by row | Walked column by column, which touched a new page on every step. Swapping the loops fixed it. |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | Elena's parts catalogue, a list | Asked one question over and over: find this part by number. A hash table answers exactly that. |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Walter's claims, a tree shaped for monthly statements | Then asked new questions, by hospital, by doctor. The shape was right for one pattern, and the patterns changed. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Maya's feeds | Read fifty times for every write, so building them at write time was the right call. |

It shows up elsewhere too: column-oriented databases for analytics, which read a few columns across millions of rows; time-series stores for data that's mostly appended and read by time; and every index, which is a second arrangement of the same data for a different question.

What the pages share is Arthur's two lessons. Arrange data for how it's used, not how it's described: reads or writes, one item or many, which items together, in what order. And expect the pattern to change: Walter's new questions, Maya's celebrity, Arthur's Christmas.

## It really happened

Arthur is fictional; warehouses still re-slot fast-moving stock by order data, for the same reason. In software, the clearest example is the column store. Traditional databases store each row together, which suits reading or updating one customer at a time. Analytical queries read one or two columns across millions of rows, so in the 2000s systems such as C-Store (Stonebraker et al., 2005) stored each column together instead, and analytical queries became many times faster. Most data warehouses work that way now. Joan's row-versus-column lesson, at the scale of a whole database.

## What it is

An access pattern is how data is actually used: how often it's read compared with written, whether by single key, by range, or by scanning, which items are used together, and in what order. Storage should follow it. Stores, layouts, indexes and caches are all choices about which pattern to make cheap, and each makes some other pattern more expensive. Patterns change, so the choice needs revisiting.

## Where it gets misapplied

- **Storing data the way it's described.** Arthur's catalogue order. A tidy schema that matches the business's vocabulary but not its queries.
- **Designing for the pattern you imagine.** Measure what's actually read and written before choosing ([profiling](../tooling/profiling.md)).
- **Optimising for one pattern forever.** Walter's tree and Arthur's summer layout.
- **The mirror:** designing for every possible pattern. A store with fifteen indexes is fast to read any way and slow to write at all ([page 4](../04-data-outlives-programs.md)).

## Connections

- Learning this is also learning [B-trees](../dsa/b-trees.md) and [LSM trees](../dsa/lsm-trees.md), because each is built for a different balance of reads and writes.
- Learning this is also learning [caching](../latency/caching.md), because a cache is Arthur's front shelves: the popular items, near.
- Learning this is also learning [hash tables](../dsa/hash-tables.md), because they make one pattern, finding by key, as cheap as possible.
- Learning this is also learning [data modelling](modelling.md), because the shape of the data should come from the questions asked of it.
- Learning this is also learning [profiling](../tooling/profiling.md), because you find the real pattern by measuring, not guessing.

## Resources

1. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapter 3, on how stores lay data out (start here).
2. Markus Winand, [*Use The Index, Luke*](https://use-the-index-luke.com/) (go deeper: indexes as access patterns made explicit). <!-- verify -->
3. Alex DeBrie, *The DynamoDB Book* (reference: designing a store entirely around known access patterns, and what it costs when they change).

## Names you'll hear

- **Read-heavy, write-heavy:** which side of the ratio dominates.
- **Point lookup, range scan, full scan:** one item by key, a sorted range, or everything.
- **Locality:** using items stored near each other at around the same time.
- **Row store, column store:** keeping each record together, or each field together.
- **Hot spot:** one key or partition getting far more traffic than the rest, Maya's champion.

## Go and look

Pick a table or collection you work with and write down the three questions most often asked of it. Then look at how it's stored and indexed, and ask whether that arrangement was chosen for those questions.
