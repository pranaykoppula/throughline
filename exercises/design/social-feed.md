# The final whistle

A design case in the category **feeds and fan-out**. It draws on [caching](../../performance/caching.md), [partitioning](../../data/partitioning.md), [growth](../../dsa/growth.md) and [back-of-the-envelope estimates](../../design/estimates.md).

## The situation

A sports app lets fans follow players, clubs, journalists and each other, and shows each fan a feed of recent posts from everyone they follow, newest first. Most accounts have a few hundred followers. The biggest clubs and star players have up to 20 million. The busiest moment of every week is the final whistle of a big match, when the star player posts and millions of fans open the app within the same few minutes. The first version built each feed when it was opened, by fetching recent posts from everyone the fan followed; on a big match day, it took twenty seconds to load.

## Requirements and numbers

- A feed of recent posts from followed accounts, newest first, loading in well under a second.
- A new post appears in followers' feeds within a few seconds.
- Deleted posts disappear, and blocked accounts' posts never appear.
- About 30 million users, 8 million active each day, each opening the feed about 10 times a day. Fans follow about 200 accounts on average. About 2 million posts a day.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What can we do with it?** Feeds are read far more often than posts are written. The ratio decides where the work should go.
- **What breaks at ten times?** Work in proportion to the biggest account, not the average one ([growth](../../dsa/growth.md)).
- **What's the peak?** The final whistle, not the daily average.

## The tempting first design

**Build on read:** when a fan opens the feed, fetch the recent posts of all 200 accounts they follow, merge them by time and show the newest. It's simple and always fresh. At the final whistle, with perhaps 20,000 feed opens a second, that's 4 million lookups a second.

**Build on write:** the obvious fix is to do the work when someone posts, by adding the post to every follower's stored feed. Opening the feed becomes one read. But when the star with 20 million followers posts at the final whistle, that's 20 million writes, at exactly the moment the system is busiest, and the fans opening the app first won't see the post at all.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Count reads and writes. How many times is a feed read for every post written? Where does that suggest the work should go, for most accounts?

</details>

<details markdown="1"><summary>Hint 2</summary>

The build-on-write plan is expensive only for a few accounts. What if those accounts were handled differently from everyone else?

</details>

<details markdown="1"><summary>Hint 3</summary>

Does every one of a star's 20 million followers need the post written into their feed? How many of them will open the app this week?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

Reads: 8 million active fans × 10 opens is 80 million feed opens a day, about 1,000 a second on average, and perhaps 20 times that at the final whistle. Writes: 2 million posts a day is about 23 a second, and with about 200 followers each, writing every post to every follower is about 400 million feed inserts a day, about 4,600 a second. So feeds are read far more than posts are written, which favours doing the work at write time, except for the few accounts where one post means millions of inserts ([estimates](../../design/estimates.md)).

### Design A: push for most, pull for the few

- **Stored feeds of post IDs.** Each active fan has a stored feed: the IDs of the most recent several hundred posts from accounts they follow, newest first, in an in-memory store partitioned by fan ([partitioning](../../data/partitioning.md), [caching](../../performance/caching.md)). Storing IDs, not whole posts, means an edit or deletion changes one record.
- **Push for ordinary accounts.** When an account with fewer than, say, 100,000 followers posts, a background job adds the post's ID to each active follower's stored feed ([asynchronous work](../../design/async-work.md)).
- **Pull for the biggest accounts.** Posts from accounts above the threshold aren't pushed. When a fan opens the feed, the app reads their stored feed and also the recent posts of the few big accounts they follow, which are cached because millions read them, and merges them by time ([heaps](../../dsa/heaps.md) merge sorted lists efficiently).
- **Only active fans.** Fans who haven't opened the app in a month have no stored feed; theirs is built on read the next time they come back.
- **Fill in at read time.** The IDs are turned into posts at read time, from a store of posts partitioned by author. Deleted posts and blocked accounts are filtered out then.

**What it costs:** two paths to maintain, and a threshold to tune. The cached posts of a star are read by millions of fans in the same minute, so that cache needs copies on many servers.

### Design B: pull everything, cache hard

Every account's recent posts are kept as a short, cached, sorted list. A feed is built on read by merging the lists of the accounts a fan follows, and the finished feed is cached for a minute.

**What it gives:** no fan-out at all, so the star's post costs nothing extra to publish, and one code path.

**What it costs:** much more work per read, and a feed cached for a minute is a minute stale. It's a good design when fans follow few accounts, or when reads are rare compared with writes; here, with 200 follows and ten opens a day, Design A does less work.

This is the same choice Maya faced on [page 8](../../08-too-many-users-too-much-data.md), whose app slowed down when its champion climber, with 1.8 million followers, posted.

</details>

## What breaks at ten times the size

- **Memory.** Stored feeds for 8 million active fans at a few hundred eight-byte IDs each are tens of gigabytes; at ten times, hundreds, spread across a cluster.
- **The threshold moves.** With more fans, more accounts cross into "too big to push", and more of each read becomes a merge.
- **Ranking.** Once the feed is ordered by what's interesting rather than by time, every read needs scoring, which is a different, heavier design.

## Where people slip

- **Treating every account the same.** The average account is cheap; the biggest one sets the cost.
- **Storing whole posts in feeds.** Edits, deletions and blocks then have to touch millions of copies.
- **Pushing to fans who never come back.** Most of the work for a big account is wasted on inactive followers.
- **Designing for the average day.** The final whistle is the design point ([estimates](../../design/estimates.md)).

## Related

- The other case in this category: a live leaderboard for a global game (coming in a later batch).
- Design pages: [back-of-the-envelope estimates](../../design/estimates.md), [asynchronous work and message queues](../../design/async-work.md).
- Other pages: [8, Too many users, too much data](../../08-too-many-users-too-much-data.md), [caching](../../performance/caching.md), [partitioning](../../data/partitioning.md), [growth](../../dsa/growth.md), [heaps](../../dsa/heaps.md), [access patterns](../../data/access-patterns.md).
