# Replication

Last reviewed: 2026-10-24

A concept page: keeping copies of data on more than one machine, and deciding what happens when the main one fails.

## Problem

A single database is a single point of failure: when its machine dies, everything stops, and whatever wasn't backed up is gone. Keeping a copy on another machine fixes that, but it raises harder questions. How up to date must the copy be? Who decides when to switch to it? And what happens if the original comes back?

## The story

In 2005 Kwame Asante ran the database for a popular hobby forum. Everything lived on one server, backed up every night. One Tuesday afternoon the server's disk failed. Kwame restored the previous night's backup onto a new machine, and the forum came back four hours later, without anything posted since midnight. Thousands of posts were gone, and the forum's users let him know about it.

So he added a replica: a second database on another machine that followed the first, applying every change shortly after it happened. If the main one died, he could promote the replica and point the forum at it. To keep the main database fast, the replica was updated asynchronously. The main database didn't wait for the replica to confirm each change before telling a user their post was saved. That was a sensible, standard choice.

Eight months later the main server stopped responding. Kwame promoted the replica and the forum was back in two minutes, and he was very pleased. Then users started reporting posts they'd made in the last few seconds before the failure that had simply vanished; the replica had been a little behind. Worse, the original server hadn't died. It had lost its network connection for a while, and when the connection came back, the forum's older application servers were still writing to it. For twenty minutes, two databases each thought they were the main one, both accepted posts, and both handed out the same post numbers for different posts. Untangling them took him most of a week.

*Before reading on: the replica saved the forum from four hours of downtime, then lost some posts and split into two. What would you have changed?*

Kwame made three changes. First, he decided which data couldn't afford to lose the last few seconds, which was account changes and payments for the forum's paid memberships. For those, the main database now waited for the replica to confirm before saying "done", accepting that those requests were a little slower. Ordinary posts stayed asynchronous. Second, promoting the replica now began by cutting off the old main server for certain, by shutting off its network access so it couldn't accept writes even if it woke up. Third, he stopped making the decision alone at three in the morning. A small separate process watched both machines and only triggered a failover when a majority of watchers agreed the main one was really gone.

Looking back, Kwame thought a replica had been the easy part. The hard part was everything around switching to it: what it might be missing, and making sure there was only ever one main database at a time.

## Where it shows up

| Page | The replicas | What they cost |
| --- | --- | --- |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Maya's read copies | A post that seemed to vanish because a copy was a fifth of a second behind. |
| [Consistency](consistency.md) | Any copies | What to promise while they disagree. |
| [LSM trees](../dsa/lsm-trees.md) | The append-only log | Often the very thing shipped to replicas so they can replay changes. |
| [Merkle DAGs](../dsa/merkle-dags.md) | Replicas checking they match | Comparing hash trees to find differences without sending everything. |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Redundancy for reliability | Every extra copy buys availability, and every failover is a moment something can go wrong. |

It shows up elsewhere too: database clusters, distributed file systems, multi-region deployments, and backups, which are a very slow kind of replica.

What these share is the same pair of decisions: how far behind a copy may be, synchronous or asynchronous, and how to make sure only one copy accepts writes at a time.

## It really happened

Kwame is fictional; his twenty minutes with two main databases has a name, split brain, and it happens to large companies too. On 21 October 2018 a 43-second network break between GitHub's East Coast data centre and its network hub led its automated failover tool to move database writes to the West Coast. Some writes had reached the East Coast databases and not been replicated. Untangling the two sides, while keeping user data intact, meant degraded service for just over 24 hours ([GitHub's post-incident analysis](https://github.blog/2018-10-30-oct21-post-incident-analysis/)). GitHub chose data integrity over a fast recovery, and said so plainly.

## What it is

Replication keeps copies of data on several machines, usually one primary that accepts writes and replicas that apply its changes. Synchronous replication waits for replicas before confirming a write, so nothing confirmed is lost, at the cost of latency. Asynchronous replication confirms first, so it's faster, but a failover can lose recent writes. Failover must guarantee a single primary, which is done by fencing off the old one and usually by a quorum of observers agreeing. Systems that let several nodes accept writes need rules for merging conflicts.

## Where it gets misapplied

- **Asynchronous replication for data that can't be lost.** Kwame's vanished posts, fine for a forum post and not for a payment.
- **Failover without fencing.** Promoting a replica while the old primary can still take writes is how split brain happens.
- **Replicas as backups.** A replica faithfully copies mistakes too: delete a table on the primary and the replica deletes it a second later.
- **The mirror:** synchronous replication across continents for everything, making every write wait for the speed of light.

## Connections

- Learning this is also learning [consistency](consistency.md), because replicas are the copies most systems make on purpose.
- Learning this is also learning [state machines](../dsa/state-machines.md), because a replica applying the same changes in the same order ends in the same state.
- Learning this is also learning [round trips](../latency/round-trips.md), because synchronous replication adds a round trip to every write.
- Learning this is also learning [the cost of reliability](../cost/reliability.md), because every replica is capacity paid for in case of failure.
- Learning this is also learning [partitioning](partitioning.md), because replication copies data while partitioning splits it, and most large systems do both.

## Resources

1. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapter 5, "Replication" (start here).
2. [GitHub's October 21 post-incident analysis](https://github.blog/2018-10-30-oct21-post-incident-analysis/) (go deeper: a real failover, written honestly).
3. Your database's documentation on replication modes and failover (reference).

## Names you'll hear

- **Primary, replica:** the copy that accepts writes, and the copies that follow it.
- **Synchronous, asynchronous:** waiting for replicas before confirming, or not.
- **Replication lag:** how far behind a replica is.
- **Failover, promotion:** switching to a replica when the primary fails.
- **Split brain:** two nodes each believing they're the primary.
- **Fencing, quorum:** cutting off the old primary for certain, and requiring a majority to agree.

## Go and look

Find out how a database you depend on is replicated: synchronously or not, how far behind its replicas usually are, and who or what decides to fail over.
