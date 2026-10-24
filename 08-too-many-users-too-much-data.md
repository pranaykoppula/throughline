# 8. Too many users, too much data

Last reviewed: 2026-10-24

Links marked with an HTML `verify` comment haven't been checked against the live page yet.

## Problem

One machine holds only so much data and answers only so many requests. Past that point a bigger machine stops being the answer: the biggest one costs more than it's worth or doesn't exist, and when it fails, everything fails with it.

## What survived

The first answer was the obvious one: buy a bigger machine. It works until it doesn't, and it's still the right first answer more often than people admit. Next came **copies**. Put replicas of the data on other machines and spread the reads across them. That holds until someone writes something, reads it back from a replica that hasn't caught up, and sees their own change missing. Copies disagree for a while, and the disagreement becomes a design problem. When writes outgrow one machine, the data gets **split**: each machine owns a slice (sharding). Now a question that touches every slice is a round trip to every machine, and moving a slice is a migration. When reads are still too slow, the work moves earlier: **precompute** the answer at write time so a read is a lookup. That trades write cost and staleness for read speed. And when an exact answer costs too much, **approximate** it. Nobody needs a view count to the last digit.

What survives is precise: once data lives in more than one place, the copies will disagree, and every design has to say what it promises while they do. When the network splits, a system can stay available and accept answers that might be stale, or stay consistent and refuse some requests. It can't do both (the CAP theorem's honest form). Everything else on this page is a choice of where that disagreement goes and who notices it.

## Why it happened

- Cheap commodity machines got cheaper faster than big ones, so many small ones beat one large one on cost long before they beat it on simplicity ([1](01-one-machine-one-program.md)).
- Users came to expect a feed that is instant and personal. That pulled precomputation out of batch jobs and into the request path ([forces: user expectation](forces.md#user-expectation-ratchets)).

## Where it lives today

Replicated databases with read replicas are standard in every managed database service. The Dynamo paper's design (below) was carried into open-source stores such as Cassandra and Riak. Every CDN is precomputation by geography.

## Where it gets misapplied

- **Microservices before the team or the load exists.** Segment split its system into many services, then folded them back into one when the running cost outgrew the benefit ([InfoQ on the talk "To Microservices and Back Again"](https://www.infoq.com/news/2020/04/microservices-back-again/)). Prime Video's monitoring team [reported cutting costs by over 90%](https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90) by consolidating a distributed pipeline. <!-- verify --> It was widely read as "microservices are dead"; [others pointed out](https://www.catchpoint.com/blog/debunking-misconceptions-amazon-prime-videos-approach-to-microservices-and-serverless) it was one service redesigned for cost. Both are true.
- **Sharding a database that fits on one machine.** Copying the architecture of a company a thousand times your size buys their problems without their reasons ([You Are Not Google](https://blog.bradfieldcs.com/you-are-not-google-84912cf44afb)). <!-- verify -->
- **The mirror:** never planning for it. When the one machine is genuinely full, the worst time to learn sharding is during the outage. Know which limit you'll hit first, and roughly when.

## Questions engineers have answered

**How do you build a home timeline for hundreds of millions of people?**

*The decision.* Twitter's timelines were read far more often than tweets were written: about 300,000 timeline reads a second against about 6,000 tweets, by the figures in a 2012 talk. So they did the work at write time. When you tweet, your tweet's ID is inserted into the in-memory timeline of every one of your followers, and reading a timeline becomes a single lookup. With reads fifty times more common than writes, that's the right call.

*What it caused.* The cost of a tweet became proportional to the number of followers. Most accounts have a few hundred. A few have tens of millions, and the talk describes a tweet from an account with 31 million followers taking up to five minutes to reach all of them. The average load was fine. The tail broke it.

*The rethink.* They didn't throw the design away. For most accounts, fan-out at write time stayed. For accounts with huge followings, the talk describes moving work to read time: their tweets are merged in when you load your timeline. The limit that moved was the shape of the follower distribution, not the total load. Ladder: down, a hand-built timeline service at a scale where nothing on sale would do.

Sources: Raffi Krikorian, ["Timelines at Scale"](https://www.infoq.com/presentations/Twitter-Timeline-Scalability/), QCon San Francisco 2012; a [written summary](https://highscalability.com/the-architecture-twitter-uses-to-deal-with-150m-active-users/) at High Scalability. A talk is the company describing itself; the numbers are theirs.

**What should a shopping cart do when the network splits?**

*The decision.* Amazon judged that a cart you can't add to is a lost sale. Their Dynamo store was built to accept every write, even when replicas couldn't reach each other, and to reconcile the versions later. It chose availability over consistency, on purpose and in writing.

*What it caused.* Two of them, and only one was in the design. The expected one: when versions conflict, the application has to merge them, and for a cart the merge keeps everything. An added item is never lost, but a deleted item can come back. The paper says so plainly. The unexpected one: Dynamo was hard to run. By Amazon's own later account, it was used for core services, but most of its engineers chose simpler managed stores instead because they didn't want to operate it.

*The rethink.* The design was kept and the operating was handed over. DynamoDB, launched in 2012, offered Dynamo's scaling as a managed service and added choices Dynamo hadn't offered, such as strongly consistent reads. Ladder: Dynamo moved down for control; DynamoDB moved back up for ease, because the cost that bound turned out to be people's time, not the machines.

Sources: DeCandia et al., ["Dynamo: Amazon's Highly Available Key-value Store"](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html) (SOSP 2007); Werner Vogels, ["Amazon DynamoDB"](https://www.allthingsdistributed.com/2012/01/amazon-dynamodb.html) (2012). <!-- verify --> The second is a launch post; it explains the past in a way that sells the product.

## Connections

- Learning this is also learning [data](data.md), because every copy is a second version of the truth and someone has to decide which one wins.
- Learning this is also learning [databases](04-data-outlives-programs.md), because replication and sharding are just indexes and transactions stretched across machines.
- Learning this is also learning [latency](latency.md) and [cost](cost.md), because fast and cheap are the same fight: precomputing spends money at write time to save time at read time.
- Learning this is also learning [the web](06-anyone-can-publish.md), because the feed is an interface expectation that rebuilt the backend.
- Learning this is also learning [math](math.md), because the timeline broke on the tail of a distribution, not its average.

## Resources

1. Raffi Krikorian, ["Timelines at Scale"](https://www.infoq.com/presentations/Twitter-Timeline-Scalability/) (start here: 40 minutes, one system, real numbers).
2. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapters 5 to 9: replication, partitioning, transactions, and consistency. The best single book on this page.
3. [The Dynamo paper](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html) (go deeper: readable, and honest about what it gives up).
4. Eric Brewer, ["CAP Twelve Years Later: How the 'Rules' Have Changed"](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/): the theorem's author on how it's misread. <!-- verify -->
5. [Jepsen analyses](https://jepsen.io/analyses) (reference: what real databases do when the network splits, as opposed to what they claim). <!-- verify -->

## Names you'll hear

- **CAP:** Eric Brewer's conjecture, later proven: when the network splits, a system has to choose between consistency and availability (formally proven in 2002 by Gilbert and Lynch).
- **Paxos** (Leslie Lamport) and **Raft:** ways for copies to agree. Raft was designed to be easier to understand than Paxos, and [it is](https://raft.github.io/). <!-- verify -->
- **Lamport clocks:** ordering events without trusting anyone's wall clock.
- **Eventual consistency:** if writes stop, the copies will eventually agree. It promises nothing about when.

## Go and look

Find something precomputed for the first screen in a system you use, and something loaded lazily beside it. That split is fan-out-on-write in miniature.

## The model so far

New on this page: sentence 8, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

4. Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises.

5. Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so systems retry and tolerate repeats. Once data moves cheaply, distribution is free, and value shifts from copies to services, relationships, and trust.

6. Client and server split the work: the server owns the truth, the client owns presentation and a copy of state. Most interface bugs are two sources of truth disagreeing. The browser won because shipping one server beats shipping a million installs; native shells survive where platforms control distribution.

7. Once strangers can reach a system, every boundary is a question of who is asking and what they may do. Trust nothing that crossed a boundary; give every party the least it needs. Harms from data fall on people other than those who collect it, so law steps in where incentives don't.

8. **When one machine isn't enough, data is copied and split, and copies disagree for a while. Every distributed design chooses what to promise about consistency versus availability. Precompute what is read often; accept approximate answers where exactness costs too much.**
