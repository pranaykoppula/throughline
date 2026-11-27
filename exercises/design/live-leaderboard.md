# Who's in the top hundred

A design case in the category **feeds and fan-out**. It draws on [heaps](../../dsa/heaps.md), [partitioning](../../data/partitioning.md), [caching](../../performance/caching.md) and [exact or approximate](../../dsa/exact-or-approximate.md).

## The situation

A mobile puzzle game runs a weekly tournament. Every finished puzzle earns points, and the game shows each player the global top hundred, their own rank, and the ten players just above and below them. Players check their rank constantly; the last hour of the week, when prizes are decided, is frantic. The first version stored each player's score in a database table and, to show a rank, counted how many players had more points. With 30 million players, a single rank took seconds, and the last hour of the tournament took the database down.

## Requirements and numbers

- Scores update as soon as a puzzle is finished.
- The global top hundred, exact and within a second or two.
- Each player's own rank, and their neighbours on the board.
- At the end of the week, prizes are awarded from a final, exact ranking.
- About 30 million players a week, 5,000 score updates a second on average and 50,000 in the final hour; rank checks about ten times as often as updates.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What can we do with it?** Two different questions: "who's at the top?", asked of everyone, and "where am I?", asked by each player about themself.
- **Which answers must be exact?** The top hundred and the final prizes, certainly. Is rank 1,402,113 or 1,402,140 a difference anyone notices?
- **What's the peak?** The final hour.

## The tempting first design

A table of players and scores, with an index on score. Updating a score is one write. The top hundred is the first hundred rows of the index. A player's rank is the count of players with a higher score.

The top hundred is fast. The rank isn't: counting the players above you means walking through every one of them, so a player in the middle of 30 million walks through 15 million entries, and at 50,000 rank checks a second, the database does nothing else ([growth](../../dsa/growth.md)).

## Hints

<details markdown="1"><summary>Hint 1</summary>

A sorted structure can answer "what's the rank of this score?" without walking every entry, if each node remembers how many entries lie beneath it. What would you need to add to a tree to make that work?

</details>

<details markdown="1"><summary>Hint 2</summary>

One machine can hold 30 million scores in memory, but not take all the traffic. If you split players across many machines, which question is still easy to answer, and which becomes hard?

</details>

<details markdown="1"><summary>Hint 3</summary>

Does the player ranked 1,402,113th need their exact rank, or would "about 1,400,000th, top 5%" do, as long as the top of the board and the final result are exact?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

30 million players, each with a score and an ID, is a few gigabytes at most in a sorted in-memory structure: it fits in one machine's memory. Updates peak at 50,000 a second and rank checks at perhaps 500,000 a second, which is more than one machine should serve. Note how lopsided the questions are: everyone asks about the same top hundred, and each player asks about their own position ([estimates](../../design/estimates.md)).

### Design A: one ranked structure in memory, read from copies

- **A sorted set with counts.** Scores are kept in memory in a sorted structure where each node knows how many entries are below it, such as a skip list or balanced tree with counts. Updating a score, reading the top hundred, finding a player's rank, and reading their neighbours each take time in proportion to the logarithm of the number of players. Several in-memory data stores offer exactly this as a sorted-set type.
- **One writer, many readers.** All updates go to one primary copy, which applies them in order. Read-only replicas, updated from its log within a second, serve rank checks ([replication](../../data/replication.md)).
- **Cache the top.** The top hundred is the same for everyone; it's computed once a second and served from a cache ([caching](../../performance/caching.md)).
- **The record lives elsewhere.** Every score change is also written to a durable store. If the in-memory structure is lost, it's rebuilt from there, and the final prize ranking is computed from the durable record, not the cache.

**What it costs:** the primary is a single point that every update passes through; at 50,000 updates a second it's busy but feasible. Replicas show ranks a second old.

### Design B: partition, and approximate the middle

Players are split across many partitions by player ID, each with its own sorted set. Updates scale with the number of partitions ([partitioning](../../data/partitioning.md)).

- **The top hundred:** each partition keeps its own top hundred; a merger combines them into the global top hundred every second, which is exact, because the global top hundred must come from the partitions' top hundreds ([heaps](../../dsa/heaps.md) merge them).
- **A player's rank:** exact rank would need asking every partition how many players beat this score. Instead, every few seconds each partition publishes a histogram of its scores; summed, they give each player an estimated rank, "about 1,400,000th, top 5%", with a known error ([exact or approximate](../../dsa/exact-or-approximate.md)). Players near the top get exact ranks by querying all partitions, which is affordable for a few thousand of them.

**What it gives:** updates and reads scale out without limit.

**What it costs:** most players see an approximate rank. For a game, that's usually fine, and it's worth checking with the people who design the game before building the exact version.

</details>

## What breaks at ten times the size

- **The single primary.** At 500,000 updates a second, Design A's one writer can't keep up; that's the point to move to Design B.
- **Ties.** With integer points, thousands of players can share a score; decide the tie-breaker (who got there first) before the prizes depend on it.
- **The final hour.** The last minutes of a tournament concentrate updates and rank checks; cache neighbours' boards briefly, and freeze the final ranking from the durable record.

## Where people slip

- **Counting to find a rank.** It walks every player above you; keep counts in the sorted structure.
- **Treating "who's at the top" and "where am I" as one question.** The first is shared and cacheable; the second is personal and can be approximate.
- **Prizes from the cache.** Award them from the durable record, after the last late update has arrived.
- **Forgetting ties.** "Equal 3rd" needs a rule, and the rule needs to be published.

## Related

- The other case in this category: [the final whistle](social-feed.md), a social feed with very large accounts.
- Design pages: [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [heaps](../../dsa/heaps.md), [B-trees](../../dsa/b-trees.md), [growth](../../dsa/growth.md), [partitioning](../../data/partitioning.md), [replication](../../data/replication.md), [caching](../../performance/caching.md), [exact or approximate](../../dsa/exact-or-approximate.md).
