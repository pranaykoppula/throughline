# Caching

Last reviewed: 2026-10-24

A concept page: keeping a copy of something close, because the original is slow to reach.

## Problem

Some data is expensive to get, because it's far away, slow to compute, or both, and it's asked for far more often than it changes. Keeping a copy nearby makes it fast. But a copy can go stale, and a cache that empties at the wrong moment can bring down the thing it was protecting.

## The story

In 2008 Ruth Abara ran the website of a national newspaper. The front page was rebuilt from the database on every visit: the top stories, the latest headlines, the most-read list. On a normal day that was fine. On big news days the database struggled, and the site slowed to a crawl exactly when the most people were reading it.

Her fix was a cache. The finished front page was kept in memory for sixty seconds, and every visitor in that minute got the stored copy. The database went from building the page thousands of times a minute to once. The site felt instant. It was a well-reasoned change, and for months it was perfect.

On election night, at the top of each minute, the site fell over. Ruth watched it happen on the graphs. Every sixty seconds the cached page expired, and in the instant before a new one was ready, twenty thousand visitors all found it missing at once. Every one of them asked the database to rebuild it. The database, which had been resting behind the cache all evening, was hit by twenty thousand identical requests in a second and stopped responding. Then the cache stayed empty, so the next wave did the same.

There was a second problem that night, smaller and more embarrassing. A sub-editor corrected a wrong result in a headline, and readers kept seeing the wrong one for up to a minute. Three people complained on air.

*Before reading on: the cache had protected the database perfectly, until the moment it expired. How would you have refreshed it without letting everyone through at once?*

Ruth changed two things. First, when the cached page expired, only one request was allowed to rebuild it. Everyone else kept getting the old page, slightly stale, until the new one was ready. The database saw one request a minute again, whatever the traffic. Second, the newsroom's publishing system now told the cache when a story changed, so a correction removed the old copy immediately instead of waiting for it to expire. The expiry timer stayed as a backstop.

Looking back, Ruth thought she'd learned that a cache isn't just a speed-up. Once it exists, the system depends on it: the database behind it is sized for the cache being full. And every cache is a copy, which means someone has to decide how stale it's allowed to be and how it finds out the original changed.

## Where it shows up

| Page | The cache | The trade |
| --- | --- | --- |
| [1, One machine, one program](../01-one-machine-one-program.md) | Core memory in front of the drum, then processor caches in front of memory | Fast, small copies of what's being used. Joan's loop order decided whether they helped. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Netflix's servers inside internet providers' networks | Copies of the catalogue placed near viewers, so most viewing never crosses the wider internet. |
| [6, Anyone can publish](../06-anyone-can-publish.md) | The day's appointments kept in each browser | Instant screens, and a double booking when the copy was wrong. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Precomputed feeds in fast memory | Reads become a lookup; writes do the work, and can go stale. |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Popular lessons cached close to students | Each video crosses the expensive boundary once instead of thousands of times. |

It shows up elsewhere too: DNS answers, compiled code, browser caches for images and scripts, and the answers to expensive database queries.

What the pages share is a copy placed nearer to where it's used, in exchange for a question about staleness. Every row in the table is the memory hierarchy from page 1 at a different scale: processor and memory, browser and server, city and data centre.

## It really happened

Ruth is fictional; her election night is a classic failure called a *cache stampede* or *thundering herd*. Facebook described the same problem in "Scaling Memcache at Facebook" (NSDI 2013). When a cached item was missing, its cache gave one client a short-lived *lease* to fetch it from the database and told the others to wait, which the paper reports cut peak database load sharply ([summary](https://pages.cs.wisc.edu/~swift/classes/cs739-fa14/blog/2014/09/scaling_memcache_at_facebook.html)). Commercial computers got processor caches in the late 1960s, starting with IBM's System/360 Model 85, for Joan's reason: memory couldn't keep up with the processor. A line usually credited to Phil Karlton sums it up: there are only two hard things in computer science, cache invalidation and naming things.

## What it is

A cache is a copy of data kept closer to where it's needed than the original, because the original is slower or costlier to reach. It works when data is read far more often than it changes, and when the same data is asked for repeatedly. Every cache needs answers to three questions: how stale may it be, how does it learn the original changed, and what happens when it's empty?

## Where it gets misapplied

- **No plan for the empty cache.** Ruth's election night. If the system can't survive the cache being cold, the cache is now critical infrastructure.
- **Caching to hide a slow query instead of fixing it.** Sometimes right, often just postpones the problem.
- **Caching data that changes constantly.** A cache that's always stale or always being refreshed costs more than it saves.
- **The mirror:** refusing to cache anything for fear of staleness. Most data can be a few seconds old; decide which can't.

## Connections

- Learning this is also learning [consistency](../data/consistency.md), because a cache is a copy you've agreed to let go stale.
- Learning this is also learning [hash tables](../dsa/hash-tables.md), because most caches are a hash table that's allowed to forget.
- Learning this is also learning [access patterns](../data/access-patterns.md), because caching only works when the same things are read again and again.
- Learning this is also learning [latency numbers](latency-numbers.md), because the gap between near and far is the whole reason caches exist.
- Learning this is also learning [queueing](queueing.md), because a stampede is a queue forming all at once at the slowest point in the system.

## Resources

1. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), on derived data and caches (start here).
2. Nishtala et al., "Scaling Memcache at Facebook" (NSDI 2013) (go deeper: caching at very large scale, including stampedes and staleness).
3. Ilya Grigorik, [*High Performance Browser Networking*](https://hpbn.co/), on HTTP caching (reference). <!-- verify -->

## Names you'll hear

- **Hit, miss, hit rate:** found in the cache, not found, and how often it's found.
- **TTL:** time to live, how long a copy is kept before it expires.
- **Invalidation:** removing a copy because the original changed.
- **Cache stampede, thundering herd:** many requests rebuilding the same missing item at once.
- **LRU:** least recently used, a common rule for what to throw out when the cache is full.
- **CDN:** a content delivery network, caches placed around the world near users.

## Go and look

Find one cache in something you work on and answer its three questions: how stale can it be, how does it learn about changes, and what happens to everything behind it when it's empty?
