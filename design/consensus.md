# Consensus and leader election

Last reviewed: 2026-11-27

A concept page: how several machines agree on one thing, such as which of them is in charge, when any of them can stop, restart or fall silent at any moment. The hard part is that a machine can't tell from the inside that it has been asleep.

## Problem

Many systems need exactly one of something: one database accepting writes, one scheduler running the nightly jobs, one owner of each lock. With one machine that's easy, and with one machine it's a single point of failure. With several, they have to **decide** among themselves which one is in charge and when it changes hands, over a network that delays and drops messages, using clocks that drift, on machines that can pause for seconds without knowing it. Get it wrong and there are two leaders, each sure it's the only one.

## The story

In 2017 Ilinca Dumitru ran the billing systems for a mobile network in Bucharest. Every night a scheduler started the invoice run: work out each customer's bill, store it, send it, and collect the direct debits. A single scheduler machine was a single point of failure, so she ran two. They shared the main database, and in it a row recorded which scheduler was in charge and until when. The leader renewed its *lease* every ten seconds, extending it by thirty. If it stopped renewing, the lease ran out and the standby took over. It was simple, it used a database they already trusted, and in testing the standby took over within thirty seconds every time she pulled a plug.

Fourteen months later, on the first night of the month, the leader paused. Its memory had grown large, and the language's garbage collector stopped the whole program for forty-five seconds to tidy it. While it was frozen, its lease ran out, and the standby, correctly, took over and started the invoice run from the beginning. Then the old leader woke up. It had checked its lease just before freezing, the lease had been valid, and from its own point of view no time had passed. It carried on with the run. About 31,000 customers received two invoices that night, and some had their direct debits taken twice.

*Before reading on: each scheduler did exactly what its lease told it to. What couldn't a lease tell a machine that had been frozen?*

Ilinca saw that the old leader hadn't been careless. It had no way to know. A paused program doesn't notice the pause; its next instruction runs as if straight after the last, and any check it made before the pause looks as fresh as ever. No amount of checking by the leader could close that gap, because the leader was the one that couldn't see it. The protection had to be somewhere that wasn't asleep.

She kept two schedulers and a lease, and changed who decided and who checked. Leadership now came from a small cluster of three machines running a consensus protocol, which granted the lease only with the agreement of a majority, so no network split could produce two clusters that both thought they could grant it. Each new grant came with a number one higher than the last: the leader before the pause had held lease 7, and the standby got lease 8. Every write of the invoice run carried its lease number, and the database refused any write carrying a number lower than the highest it had already seen. When the old leader woke and tried to carry on with lease 7, the database turned it away, and it stepped down. Nobody could stop a machine believing it was in charge. The database just stopped believing it.

![A timeline with two schedulers and the database. Scheduler A holds lease 7 and writes. It freezes for forty-five seconds; its lease runs out; scheduler B is granted lease 8 and writes. A wakes, still believing it leads, and tries to write with lease 7. The database, which has already seen 8, rejects the write.](../images/figures/design-consensus.svg)

*A machine can't tell that it's been asleep. The storage can tell that a lease number is old.*

Looking back, Ilinca thought her lease had answered the wrong question. It told each scheduler whether it believed it was the leader, and both had believed it honestly. What mattered was whether the rest of the system would accept its work, and that had to be decided somewhere outside either scheduler.

## Where it shows up

| Page | The agreement | What it taught |
| --- | --- | --- |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Maya's main database and its copies | Copies need one place where writes go, and someone has to decide which. |
| [Replication](../data/replication.md) | Kwame's replica, promoted while the old main database still took writes | Failing over without fencing the old leader is how split brain happens. |
| [Consistency](../data/consistency.md) | Copies that disagree for a while | Consensus is the expensive end of the range: every change agreed by a majority before anyone sees it. |
| [Append-only logs](../dsa/append-only-logs.md) | A log of changes, applied in order | What consensus protocols really agree on is the next entry in a shared log. |
| [State machines](../dsa/state-machines.md) | Chloe's order states | Machines that apply the same log to the same state machine end in the same state, which is how a replicated service is built. |
| [Idempotency](idempotency.md) | Valeria's repeated charges | Fencing stops an old leader's writes; idempotency stops a retried one's. Billing needs both. |

It shows up elsewhere too: committees that need a quorum before a vote counts, juries that need a majority, a papal conclave that keeps voting until one name has two thirds, and a relay race's baton, which makes "who's running now" a physical object rather than a belief.

What the rows share is that being in charge isn't something a machine can know about itself. It's something the others agree to, and the agreement has to be checked where the work lands, by a number that only ever goes up.

Motif: [copies disagree](../motifs.md#copies-disagree).

## It really happened

Ilinca is fictional, and so is her phone network. Her failure has been described in exactly these terms. In 2016 Martin Kleppmann showed how a client holding a lock can be paused by garbage collection, have its lease expire while it's frozen, and wake to write after another client has taken over. His fix was a fencing token: a number that increases with every lock granted, checked by the storage service, which rejects writes carrying an older one ([Kleppmann, "How to do distributed locking"](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)).

Consensus protocols are old and famously hard. Leslie Lamport described Paxos in a paper written around 1989 as the story of an ancient Greek parliament; it was published in 1998. In 1985 Michael Fischer, Nancy Lynch and Michael Paterson had proved that no protocol can guarantee agreement in every case when messages can be delayed without limit and one machine may crash, which is why real protocols rely on timeouts to make progress. Google's Chubby lock service (2006) put Paxos behind a simple lock-and-lease interface for the rest of the company. In 2014 Diego Ongaro and John Ousterhout published Raft, designed to be easier to understand than Paxos, with leader election, log replication and safety as separate parts ([USENIX ATC 2014](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro)). Raft runs inside etcd, which stores the state of Kubernetes clusters, and in many databases.

## What it is

A **consensus protocol** lets a group of machines agree on a value, usually the next entry in a shared log, as long as a majority of them can talk to each other. Because any two majorities overlap, two separate groups can't both decide. **Leader election** is consensus about who leads: in Raft, a follower that hears nothing from the leader for a random timeout asks the others to vote for it, and each new leader serves in a numbered *term*. A **lease** gives leadership for a limited time, so a crashed leader's role passes on automatically. A **fencing token** is the lease's number, checked by whatever the leader writes to, so that a leader that has lost its lease without knowing can't do harm. In practice, few teams implement consensus themselves; they use a coordination service such as etcd, ZooKeeper or Consul, or a database built on one.

## Where it gets misapplied

- **A lease without fencing.** It works until the leader pauses: a garbage collection, a virtual machine being moved, a disk that stalls.
- **Trusting clocks.** Leases measured by different machines' clocks drift apart; only the storage's ordering of numbers is reliable.
- **Two machines deciding between themselves.** With two, a broken link looks the same as a dead partner, and each takes over. Majorities need three or more.
- **Writing a consensus protocol from a paper.** The published algorithms are subtle, and the corner cases are where implementations fail; use a tested one.
- **The mirror:** reaching for consensus where one leader isn't needed. Work that's safe to do twice, or that can be split so each machine owns its own part, needs no election at all.

## Connections

- Learning this is also learning [replication](../data/replication.md), because promoting a copy is an election, and doing it without fencing is how split brain happens.
- Learning this is also learning [append-only logs](../dsa/append-only-logs.md), because consensus protocols agree on the order of a log, and everything else is derived from it.
- Learning this is also learning [state machines](../dsa/state-machines.md), because machines applying the same log to the same state machine stay in step.
- Learning this is also learning [consistency](../data/consistency.md), because agreement by a majority is the strongest promise copies can make, and the slowest.
- Learning this is also learning [idempotency](idempotency.md), because work that's safe to repeat needs no single leader to protect it.
- Learning this is also learning [timeouts and circuit breakers](timeouts.md), because every election starts when someone decides another machine has been silent too long.

## Resources

1. Martin Kleppmann, ["How to do distributed locking"](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) (2016) (start here: the paused leader and the fencing token).
2. Diego Ongaro and John Ousterhout, ["In Search of an Understandable Consensus Algorithm"](https://raft.github.io/raft.pdf) (2014), and the visualisations on the [Raft site](https://raft.github.io/) (go deeper).
3. Martin Kleppmann, *Designing Data-Intensive Applications*, chapters 8 and 9 (reference: what can go wrong with clocks and pauses, and how consensus copes).

## Names you'll hear

- **Consensus, quorum, majority:** agreeing on a value; the number of machines whose agreement counts.
- **Paxos, Raft, Zab:** consensus protocols; Zab is ZooKeeper's.
- **Leader, follower, term, epoch:** who leads, and the numbered period they lead in.
- **Lease:** leadership or a lock for a limited time.
- **Fencing token:** an increasing number that lets storage reject a stale leader.
- **Split brain:** two machines each believing they lead.
- **etcd, ZooKeeper, Consul:** coordination services built on consensus.
- **FLP impossibility:** the proof that no protocol can guarantee agreement in every case if messages can be delayed indefinitely.

## Go and look

Find something you run that's meant to have exactly one of something: one primary database, one scheduler, one consumer. Find out how it decides, and what stops the old one from acting if it pauses for a minute and wakes up.

Practise this: [ten o'clock on Friday](../exercises/design/flash-ticket-sale.md), where each section's seats have exactly one owner, and [every hour, on the hour](../exercises/design/job-scheduler.md), schedule partitions with fenced leases.
