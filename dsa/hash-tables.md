# Hash tables

Last reviewed: 2026-10-24

A concept page: finding things by key in constant time, and what it costs to keep it that way.

## Problem

Most programs constantly ask one question: given this key, where's the value? Searching a list gets slower as the list grows. A hash table answers in roughly the same time however much it holds, as long as it never gets too full, and growing it is where the trouble hides.

## The story

In 2006 Kenji Mori wrote the server for an online game. Every player connected to it had a session, and every message that arrived, a move or a chat line or an attack, started with a lookup: which player sent this? The sessions lived in a hash table. A player's ID was hashed to a slot, and the session was found there in one step, whether a hundred players were online or a hundred thousand. [Hashing](hashing.md) did the hard part.

Kenji had used the language's standard hash table, which handled the one thing he hadn't thought about: it grew. When it got more than three-quarters full, it allocated a table twice the size and moved every entry across, because keeping a table roomy is what keeps lookups fast. Doubling meant growth was rare, and on average it cost almost nothing per insert. It was a well-understood design, and Kenji didn't give it a second thought.

At the launch of the game's first expansion, two hundred thousand players logged in within an hour. At about four million sessions, counting reconnections, the table filled past three-quarters and doubled. Moving four million entries took the server nearly two seconds, and for those two seconds it answered nothing. Every connected player froze. Thousands of game clients decided the server had died and reconnected at once, which added more sessions, which brought the next doubling sooner.

On average, the hash table had been fast. On one occasion, it had stopped the world.

*Before reading on: the table needed to grow, and growing all at once froze the server. How would you have grown it?*

Kenji's fix was to grow the table gradually. When it got full, the server allocated the new, larger table but didn't move anything yet. From then on, every lookup or insert also moved a few entries from the old table to the new one. Lookups checked both tables until the move was finished. Growth that used to happen in one two-second lump now happened in thousands of microsecond-sized steps, spread over a minute. Nobody noticed it at all. He also started the table at a sensible size for launch day, so it rarely needed to grow during the busiest hour.

Looking back, Kenji thought the lesson was about "on average". A doubling hash table really is fast on average. But a game server, like most servers, is judged by its worst moment, and the average had been hiding a two-second pause inside it.

## Where it shows up

| Page | The table | What it was for |
| --- | --- | --- |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | Elena's parts catalogue | Find one part by its number, thirty times faster than searching a list. |
| [Caching](../latency/caching.md) | Nearly every cache | A hash table that's allowed to forget. |
| [Hashing](hashing.md) | Dorothy's freight-car slots | The first hash tables, and the lesson that real keys aren't spread evenly. |

It shows up elsewhere too: database hash indexes, the dictionaries and maps built into most programming languages, symbol tables in compilers, and deduplication.

What these share is one access pattern, finding one item by its key, made as cheap as possible. What they all have to plan for is the same: collisions, keys that aren't spread evenly, and growth.

## It really happened

Kenji is fictional; his fix is how Redis, a widely used in-memory database, grows its hash tables. When a table needs to grow, Redis allocates a second table and moves entries across a few at a time with each operation, and in the background when it's idle, so no single command pauses for long ([an explanation of Redis's dictionary](https://www.openmymind.net/Back-To-Basics-Hasthables-Part-2/)). The cost is complexity: almost every operation has to know a move might be in progress. The idea of hash tables goes back to Hans Peter Luhn's memo at IBM in 1953 ([hashing](hashing.md)).

## What it is

A hash table stores values in an array of slots, choosing each value's slot by hashing its key. Lookups, inserts and deletes take roughly constant time on average, as long as the table stays below a certain fullness, its load factor, and the hash spreads keys evenly. Collisions are handled by chaining or by probing for the next free slot. Tables grow by moving entries to a bigger array, all at once or gradually. They don't keep keys in order, so they're the wrong choice for range queries.

## Where it gets misapplied

- **Ignoring growth.** Average-case cost hides the occasional pause; for a server, that pause can be the outage.
- **Range queries.** "All parts numbered between 4000 and 5000" means checking every slot. A sorted structure, like a [B-tree](b-trees.md), does it directly.
- **Predictable hashes on untrusted keys.** Strangers can choose keys that all collide ([hashing](hashing.md)).
- **The mirror:** reaching for something cleverer when a hash table would do. For lookup by key, it's almost always the right first answer.

## Connections

- Learning this is also learning [hashing](hashing.md), because the table is only as good as the hash that places its keys.
- Learning this is also learning [B-trees](b-trees.md), because they make the other trade: slightly slower lookups, but keys kept in order.
- Learning this is also learning [caching](../latency/caching.md), because a cache is a hash table that's allowed to forget.
- Learning this is also learning [access patterns](../data/access-patterns.md), because a hash table is what you get when the pattern is "find by key" and nothing else.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because "constant time on average" can hide a terrible worst case.

## Resources

1. Thomas Cormen et al., *Introduction to Algorithms*, the chapter on hash tables (start here).
2. ["Back to Basics: Hashtables"](https://www.openmymind.net/Back-To-Basics-Hasthables-Part-2/) (go deeper: growth and incremental rehashing, with Redis as the example).
3. Donald Knuth, *The Art of Computer Programming*, volume 3, section 6.4 (reference).

## Names you'll hear

- **Load factor:** how full the table is; past a threshold, it grows.
- **Rehashing, resizing:** moving entries into a bigger table.
- **Amortised cost:** the average cost per operation over many, which can hide rare expensive ones.
- **Chaining, open addressing:** two ways to store colliding keys.
- **Dictionary, map, hash map:** what most languages call a hash table.

## Go and look

Find the biggest hash table, dictionary or map in something you've built and ask what happens when it grows. Then find out how big it gets on your busiest day.
