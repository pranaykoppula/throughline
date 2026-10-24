# 8. Too many users, too much data

Last reviewed: 2026-10-24

Links marked with an HTML `verify` comment haven't been checked against the live page yet.

## Problem

One machine holds only so much data and answers only so many requests. Past that point a bigger machine stops being the answer: the biggest one costs more than it's worth, and when it fails, everything fails with it.

## The story

Maya is the second engineer at Crux, a small app where climbers post the routes they've done and follow each other. It runs on one web server and one database, and for two years that has been fine.

Then a gym chain partners with them, and the app gets busy in the evenings. Every night around seven, pages start taking three seconds to load. Maya looks at the database server. The processor is at 95%, and almost all of the work is reads: people scrolling, not posting.

She has a vague sense that "real" companies spread their data across many machines, and no idea how. She does know what a bigger server costs. She upgrades to one with twice the cores, which takes an afternoon and can be undone if it doesn't help. The evenings go quiet. It's not clever, and it's the right call: it buys eight months for the price of a bill.

Eight months later it's seven o'clock again, and the next size up costs twice as much for a third more speed. Maya counts the queries: about fifty reads for every write. If most of the work is reading, she reasons, the data doesn't all have to be read from one place. She sets up two **copies** of the database that follow the main one and only answer reads. All writes still go to the main database. Load drops by two thirds. She feels like she's finally doing real engineering.

A week later a support email arrives: *"I posted my send of the Nose and it vanished. Then it came back a minute later. Is my account broken?"* Maya can't reproduce it. She tries for an hour and her posts appear every time. Then she adds logging and sees it: the user's post went to the main database, and the very next page load, a fifth of a second later, read from a copy that hadn't caught up yet. On her laptop, everything happens in one place, so the copies never fall behind.

Nobody told her copies disagree. Now she knows: for a while after every write, the copies hold different versions of the truth. She can't make that go away, but she can decide who notices. For a few seconds after someone posts, she sends that person's reads to the main database. Everyone else can wait for the copies. She writes it down for the team in two lines: *you always see your own posts straight away; other people see them within a second or so.* She doesn't know it has a name. She has just written a consistency model.

Then the home feed gets slow. Every time someone opens the app, the database finds everyone they follow, gathers those people's recent posts, sorts them by time, and returns the top fifty. A climber following five hundred people means a lot of gathering, every single time, for a screen they'll glance at for four seconds.

*Before reading on: the feed is read every time someone opens the app, and only changes when someone posts. Where would you move the work?*

Maya gets there on a walk home. If the feed is read a hundred times for each time it changes, build it when it changes. When someone posts, add the post's ID to a ready-made feed list for each of their followers, kept in fast memory. Opening the app becomes a single lookup. The average user has two hundred followers, so a post costs two hundred small writes, which is nothing. She builds it over two weeks. Feed loads drop from 800 milliseconds to 30. It's a well-reasoned decision, and it's right.

In the spring, the world bouldering champion joins Crux. Within a week she has 1.8 million followers. Her first post triggers 1.8 million writes into the feed system. The job queue backs up behind it. For forty minutes, nobody's feed updates. People see replies to her post before the post itself. Her like counter, one row updated thousands of times a second, locks up the database on its own.

It's a bad night, and Maya didn't do anything wrong. She designed for the average user, and the world sent her the edge case. The temptation the next morning is to rip out the precomputed feeds and go back. But they work for 99.99% of accounts. The problem isn't the design. It's that one kind of account doesn't fit it.

Maya calls Sam, who used to work at a much bigger company, and asks the question that matters: *what's different about the accounts that break it?* There are maybe a hundred of them, each with hundreds of thousands of followers. So Maya treats them differently. Their posts don't get copied into anyone's feed. Instead, when you open the app, it takes your ready-made feed and merges in recent posts from the handful of huge accounts you follow. Reads do slightly more work, but it's bounded: nobody follows a thousand celebrities. For the like counter, Sam's advice is to stop counting exactly. Count in ten separate rows and add them up when the post is shown. Nobody can tell 41,203 likes from 41,210.

The hybrid ships in a week. The champion posts again. Nothing happens, which is the point.

Looking back, Maya didn't invent anything. She bought a bigger machine until that stopped making sense. She made **copies** and decided what to promise while they disagree. She **precomputed** what was read far more than it was written. She **approximated** where exactness cost too much. And she shaped the design around the real distribution of her users instead of the average one. A year from now, when writes outgrow the main database too, she'll **split** the data across machines, and that will be another story. Each step was a reasonable guess that worked until it met something she couldn't have seen from where she stood.

## It really happened

The Crux story is made up. Twitter's isn't. In 2012 Twitter's timelines were read about 300,000 times a second against about 6,000 new tweets, and they built home timelines exactly as Maya did: each tweet copied into every follower's timeline in memory. A tweet from an account with 31 million followers could take up to five minutes to reach all of them. The talk describes the same rethink: keep copying for most accounts, and move work to read time for the biggest ones. Nobody at Twitter knew that answer before they needed it. They got there the way Maya did.

Sources: Raffi Krikorian, ["Timelines at Scale"](https://www.infoq.com/presentations/Twitter-Timeline-Scalability/), QCon San Francisco 2012, and a [written summary](https://highscalability.com/the-architecture-twitter-uses-to-deal-with-150m-active-users/). It's a company describing itself; the numbers are theirs.

Amazon made the opposite choice about copies, on purpose. Their Dynamo store accepts every write to a shopping cart even when the copies can't reach each other, because a cart you can't add to is a lost sale. The cost is in the paper in plain words: when copies are merged, an item you deleted can come back. Then came a surprise nobody designed for. Dynamo was hard to run, and most of Amazon's own engineers chose simpler managed services instead, so it came back years later as DynamoDB, run for them ([the paper](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html); [Vogels, 2012](https://www.allthingsdistributed.com/2012/01/amazon-dynamodb.html) <!-- verify -->, a launch post that explains the past in a way that sells the product).

## What survived

Once data lives in more than one place, the copies will disagree, and every design has to say what it promises while they do. When the network between copies breaks, a system can keep answering and risk stale answers, or stay correct and refuse some requests; it can't do both. Copies spread reads; splits spread writes; precomputing moves work from read time to write time; approximating trades exactness for cost. Design for the distribution you have, including its tail, not its average.

## Where it gets misapplied

- **Microservices before the team or the load exists.** Segment split its system into many services, then folded them back into one when the running cost outgrew the benefit ([InfoQ on "To Microservices and Back Again"](https://www.infoq.com/news/2020/04/microservices-back-again/)). Prime Video's monitoring team [reported cutting costs by over 90%](https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90) <!-- verify --> by consolidating; [others pointed out](https://www.catchpoint.com/blog/debunking-misconceptions-amazon-prime-videos-approach-to-microservices-and-serverless) it was one service redesigned for cost, not a verdict on microservices.
- **Sharding a database that fits on one machine.** Copying a company a thousand times your size buys their problems without their reasons ([You Are Not Google](https://blog.bradfieldcs.com/you-are-not-google-84912cf44afb)). <!-- verify --> Maya's bigger server was the right first move.
- **The mirror:** never planning for it. The worst time to learn sharding is during the outage. Know which limit you'll hit first, and roughly when.

## Connections

- Learning this is also learning [data](data.md), because every copy is a second version of the truth and someone has to decide which one wins.
- Learning this is also learning [databases](04-data-outlives-programs.md), because replication and sharding are indexes and transactions stretched across machines.
- Learning this is also learning [latency](latency.md) and [cost](cost.md), because precomputing spends money at write time to save time at read time.
- Learning this is also learning [the web](06-anyone-can-publish.md), because the feed is an interface expectation that rebuilt the backend ([forces](forces.md#user-expectation-ratchets)).
- Learning this is also learning [math](math.md), because the design broke on the tail of a distribution, not its average.

## Resources

1. Raffi Krikorian, ["Timelines at Scale"](https://www.infoq.com/presentations/Twitter-Timeline-Scalability/) (start here: 40 minutes, Maya's story with real numbers).
2. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapters 5 to 9: replication, partitioning, transactions, consistency.
3. [The Dynamo paper](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html) (go deeper: readable, and honest about what it gives up).
4. Eric Brewer, ["CAP Twelve Years Later"](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/): the theorem's author on how it gets misread. <!-- verify -->
5. [Jepsen analyses](https://jepsen.io/analyses) (reference: what real databases do when the network breaks, as opposed to what they claim). <!-- verify -->

## Names you'll hear

- **Read-your-writes:** the promise Maya wrote down without knowing its name.
- **Fan-out on write / fan-out on read:** building feeds when posts arrive, or when feeds are opened.
- **CAP** (Eric Brewer): when the network splits, a system chooses between consistency and availability. Proven formally in 2002 by Gilbert and Lynch.
- **Paxos** (Leslie Lamport) and **Raft:** ways for copies to agree. Raft was designed to be easier to understand, and [it is](https://raft.github.io/). <!-- verify -->
- **Eventual consistency:** if writes stop, the copies will eventually agree. It promises nothing about when.

## Go and look

Find something precomputed for the first screen in an app you use, and something loaded lazily beside it. That split is Maya's hybrid in miniature.

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
