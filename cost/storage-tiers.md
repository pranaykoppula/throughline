# Storage tiers

Last reviewed: 2026-10-24

A concept page: fast storage is expensive, cheap storage is slow, and data cools over time.

## Problem

Storage comes in tiers: small and fast and costly, or large and slow and cheap, with several steps between. Keeping everything in the fast tier wastes money on data nobody reads. Pushing data to the cheap tier saves money until someone needs it quickly.

## The story

In 2016 Sam Okoro ran storage for a photo-sharing service. Every photo ever uploaded, about two petabytes, sat on fast storage, ready to load instantly. Sam pulled a month of access logs and found what he'd suspected. Photos were looked at a great deal in their first few days, a little in their first month, and almost never after that. Ninety percent of what they paid to store fast was never read.

The cloud provider offered an archive tier at a fraction of the price. Retrieving from it took hours and cost a fee per gigabyte, but nobody was retrieving these photos. Sam moved every photo older than six months into the archive. The storage bill fell by more than half. It was clearly the right decision, and the finance team sent him a thank-you note.

Eight months later the product team launched a "memories" feature: every morning, show each user a photo from this day in a past year. It was delightful and very popular. It also asked for millions of old photos a day, from the archive. The first morning, most memories showed a grey box, because the photos took hours to come back. By the end of the first week, the retrieval fees had wiped out half a year of storage savings.

*Before reading on: the archive was right for photos nobody looked at, until a feature started looking at them. How would you have arranged the tiers instead?*

Sam stopped tiering by age alone and started tiering by how photos were actually used. Small thumbnails of every photo, a tiny fraction of the bytes, went back on fast storage, because they were what features like memories showed first. Full-size old photos moved to a middle tier, slower and cheaper than the fast one but readable in milliseconds, not hours. The archive kept only originals that were almost never requested. And memories began fetching tomorrow's photos tonight, so they were warm before anyone woke up.

Looking back, Sam thought his first decision had been right for the access pattern he measured and wrong for the one the product invented later. Data doesn't just cool. Sometimes something warms it up again.

## Where it shows up

| Page | The tiers | The trade |
| --- | --- | --- |
| [1, One machine, one program](../01-one-machine-one-program.md) | Core memory and the drum | Joan's program was fast or slow depending on which tier its data was in. |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Data on disk, and the indexes that avoid reading most of it | Each index is a small, fast path to data on the slow tier. |
| [Reading a cloud bill](cloud-bills.md) | What you store, and how fast you need it | A large part of most bills, and easy to get wrong in both directions. |
| [Latency numbers](../latency/latency-numbers.md) | Every row of the table | The fast rows are the expensive ones. |

It shows up elsewhere too: processor caches, memory, solid-state disks, spinning disks and tape; hot, warm and cold storage classes in every cloud; and backups.

What the pages share is page 1's memory hierarchy, priced. Every tier trades speed for cost, and the right tier for a piece of data depends on how often, and how fast, it will be needed.

## It really happened

Sam is fictional; his pattern is well documented. Facebook found that requests for photos and other files fell sharply with age, roughly a hundredfold within two months, and built a separate "warm" storage system, f4, for older data. It used fewer copies stored more cleverly, cutting the space needed while keeping files readable in milliseconds ([f4, OSDI 2014](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/muralidhar); [summary](https://blog.acolyer.org/2014/12/16/f4-facebooks-warm-blob-storage-system/)). Cloud archive tiers launched in the 2010s priced storage very low and retrieval separately, which suits backups and is dangerous for anything a product might start reading.

## What it is

Storage tiers are levels of storage that trade speed for cost: memory, fast disks, slow disks, archives. Data is usually read most when it's new and cools with age, so moving older data to cheaper tiers saves money. The traps are retrieval costs and delays in the cold tiers, and features that suddenly warm old data up. Tier by measured access, keep small summaries hot, and price retrieval before choosing a tier.

## Where it gets misapplied

- **Everything on the fastest tier.** Paying premium prices for data nobody has read in years.
- **Tiering by age alone.** Sam's first plan, until memories.
- **Ignoring retrieval costs.** Archive tiers are cheap to fill and expensive to read.
- **The mirror:** archiving so aggressively that ordinary requests wait hours. Storage is cheap compared with a feature that doesn't work.

## Connections

- Learning this is also learning [latency numbers](../latency/latency-numbers.md), because each tier is a row in the table with a price attached.
- Learning this is also learning [access patterns](../data/access-patterns.md), because the right tier depends on how often data is read.
- Learning this is also learning [caching](../latency/caching.md), because keeping thumbnails hot is caching the part that's used most.
- Learning this is also learning [reading a cloud bill](cloud-bills.md), because storage and retrieval are separate lines, and both matter.
- Learning this is also learning [data gravity](../data/data-gravity.md), because the more data sits in one place, the more it costs to move.

## Resources

1. Your cloud provider's storage class documentation (start here: read the retrieval prices, not just the storage prices).
2. Muralidhar et al., ["f4: Facebook's Warm BLOB Storage System"](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/muralidhar) (OSDI 2014) (go deeper).
3. Randal Bryant and David O'Hallaron, *Computer Systems: A Programmer's Perspective*, chapter 6 (reference: the memory hierarchy the tiers come from).

## Names you'll hear

- **Hot, warm, cold:** how often data is read, and so which tier suits it.
- **Archive tier:** very cheap storage with slow, paid retrieval.
- **Lifecycle policy:** rules that move data between tiers automatically, usually by age.
- **Erasure coding:** storing data with less overhead than full copies, while still surviving failures.
- **Data temperature:** how often data is accessed, which usually falls with age.

## Go and look

Find the largest store of data in something you run and check how much of it was read in the last month. Then find the price of storing that data on a cheaper tier, and the price of reading it back.
