# 4. Data outlives programs

Last reviewed: 2026-10-24

## Problem

Programs get rewritten; the data they keep stays for decades. Data stored in the shape one program needed made every later program, and every new question, pay for that first program's choices.

## The story

Walter Brandt maintained the claims system at an insurance company in Hartford. In 1972 it was the company's pride. Every customer's records sat in a tree on disk: the customer at the top, their policies beneath, each policy's claims beneath that, and each claim's payments at the bottom. A program found a customer, then stepped down to their policies, then to the claims. It was fast, because it was shaped exactly like the job the system did most: printing each customer's monthly statement. Walter had helped design it, and he still thought it was right.

In 1974 a new vice-president asked a question at a meeting. Which hospitals were sending the most claims, across all customers? The data was all there. Every claim recorded its hospital. But the tree had no path that started from a hospital. To answer, a program had to walk the whole tree, every customer, every policy, every claim, and count as it went. Walter wrote it. It ran for two nights.

Then the fraud team wanted the same thing every week, by doctor. And the actuaries wanted claims by diagnosis and region. Each new question was another full walk of the tree, or a second copy of the data in a different shape that someone had to keep in step. Walter looked at turning the tree over and putting hospitals at the top. It would have broken a hundred and forty programs that knew how to step from customer to policy to claim. The data had been right all along. The shape had been chosen for one question, and the company kept asking new ones.

*Before reading on: the facts weren't changing, but the questions were. How would you store data so that tomorrow's question doesn't need a rewrite?*

An IBM salesman, of all people, mentioned a paper from IBM's own research lab by a mathematician named Ted Codd. Walter read it on a train. Codd's argument was that programs shouldn't know how data is laid out at all. Store facts as plain tables: customers, policies, claims, each row connected to others by values, such as a policy number written in the claim, rather than by pointers on disk. A program says *what* it wants, and the database works out *how* to get it. Walter's hospital question would be a few lines.

He also noticed that IBM wasn't selling it. IBM sold the tree database, and made a great deal of money doing so. Walter had a fair idea why the research and the products didn't match.

By the end of the decade small companies were selling relational databases, and in 1980 the company let Walter pilot one for the fraud team. He loaded five years of claims into tables and wrote the hospital question in an afternoon. The first time he ran it, it took forty minutes, because the database read every claim to find each hospital's. He added an *index* on the hospital column, a sorted lookup the database kept alongside the table, and the same question came back in under a minute. The fraud team started asking questions he'd never have dared to write against the tree.

He got carried away. Every time someone asked a new question, he added an index for it. Within six months the claims table had fourteen. Then the nightly job that loaded the day's new claims, which had taken an hour, started taking six. Every new claim now meant writing the row and updating fourteen sorted lookups. He'd made every read faster by making every write slower, and the company wrote claims all day. He went through the queries people actually ran, kept the four indexes they used, and dropped the rest. The load went back to ninety minutes. Indexes weren't free; they were a trade, and he'd forgotten to check what he was trading.

The moment he trusted the new system came by accident. A power cut hit in the middle of a payments batch. Walter drove in at midnight sure he'd find half the cheques recorded and half not, and a week of reconciliation ahead of him. Instead, the database had undone every payment that hadn't finished. Each batch had been all or nothing, exactly as the manual promised. He read that part of the manual again the next morning. Walter had always cared most about speed. He decided then that what a store *promised* mattered more.

Looking back, Walter thought his whole career had been about outliving programs. The programs he'd written in 1972 were all gone by 1985. The claims were still there, and so was every shape decision anyone had made about them. The store you choose should follow how the data is read and written. Indexes buy reads with writes. And the promises a store makes about what happens when things go wrong are the part you'll be grateful for at midnight.

## It really happened

Walter is fictional; his tree wasn't. In the 1960s and 70s the leading databases were hierarchical and network systems such as IBM's IMS. Programs moved through them record by record, which Charles Bachman called "the programmer as navigator" in his 1973 Turing Award lecture. Ted Codd's 1970 paper, "A Relational Model of Data for Large Shared Data Banks", argued that programs should be independent of how data is stored. IBM was slow to sell relational databases, and historians usually point to the revenue from IMS ([CACM, "Happy Birthday, RDBMS!"](https://cacm.acm.org/magazines/2010/5/87252-happy-birthday-rdbms/fulltext) <!-- verify -->). Berkeley's Ingres and the small company that became Oracle got relational systems out ahead of IBM's own products. Transactions came earlier than relational databases did; IMS supported them in the early 1970s. The name ACID was coined in 1983 by Theo Härder and Andreas Reuter, building on Jim Gray's work.

Thirty years later the tree came back. Document databases store each record as one nested document, which is a tree. Around 2010, Diaspora, an open-source social network, stored its data in MongoDB. It later moved to MySQL when it needed questions that cut across documents, the same way Walter's hospital question cut across customers ([Sarah Mei's talk on the move, 2011](https://www.slideshare.net/sarahmei/taking-diaspora-from-mongodb-to-mysql-rubyconf-2011)). Her later essay, "Why You Should Never Use MongoDB", drew a strong reply arguing that the real problem was how the data was modelled, not the database ([Oren Eini](https://ayende.net/blog/164483/re-why-you-should-never-use-mongodb)). Both are partly right. Eini builds a document database, RavenDB; read his reply with that in mind. Ladder: up. Codd moved the *how* out of programs and into the database.

## What survived

Data outlives programs, so its shape is the longest-lived decision you make. Choose a store by how the data will be read and written, and expect new questions. Keep the logical shape (what the facts are) separate from the physical shape (how they're laid out), so the second can change without breaking programs. Indexes trade write cost for read speed. Transactions define what the store promises when things fail halfway.

## Where it gets misapplied

- **A document store for "web scale", then rebuilding joins in application code.** If your data is full of relationships, a store that doesn't model them makes you write the database yourself, badly.
- **Never looking at what the query library generates.** A layer that writes your queries for you can write a thousand where one would do. Measure it at least once.
- **Indexes on everything.** Walter's fourteen. Every index is paid for on every write.
- **The mirror:** forcing everything into tables. Logs, event streams, and data that really is one nested document per item can fit other stores better. The question is always how it's read and written.

## Connections

- Learning this is also learning [access patterns](data/access-patterns.md), because the tree was shaped for one question and the company kept asking new ones: how data is read and written decides the store, not fashion.
- Learning this is also learning [abstraction](03-programs-too-big-for-one-head.md), because Codd's data independence is Parnas's information hiding applied to data: hide the layout so it can change.
- Learning this is also learning [B-trees](dsa/b-trees.md), because they're what Walter's index was, and they're still behind most indexes: sorted, shallow, and cheap to read from disk.
- Learning this is also learning [LSM trees](dsa/lsm-trees.md), because they make the opposite trade, cheaper writes for costlier reads, for stores that write all day.
- Learning this is also learning [hardware](01-one-machine-one-program.md), because every index exists to avoid reading from the slow floor of the memory hierarchy.
- Learning this is also learning [multi-tenancy](auth/multi-tenancy.md), because who may read which row is the boundary between one customer's data and another's.
- Learning this is also learning [storage tiers](cost/storage-tiers.md), because storage, indexes and the writes they cost all show up on a bill.
- Learning this is also learning [consistency](data/consistency.md), because the actuaries' second copy of the data, in a different shape, was a copy someone had to keep in step, and copies drift apart.

## Resources

1. Markus Winand, [*Use The Index, Luke*](https://use-the-index-luke.com/) (start here: free, and about the one thing that matters most in practice). <!-- verify -->
2. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapters 2 and 3: data models, and how stores actually lay data out (go deeper).
3. E. F. Codd, "A Relational Model of Data for Large Shared Data Banks", *CACM*, 1970 (the original; the first section is readable and is the whole argument).
4. Charles Bachman, "The Programmer as Navigator", Turing Award lecture, 1973 (the world Codd was arguing against, from its best defender).

## Names you'll hear

- **Codd's relational model; SQL:** tables, and the language for asking them questions.
- **Normal forms** (Boyce–Codd and others): rules for storing each fact once so copies can't disagree.
- **ACID:** atomicity, consistency, isolation, durability, the promises of a transaction.
- **B-tree:** the structure behind most indexes since the 1970s.
- **CAP:** you'll hear it here, but it belongs to [page 8](08-too-many-users-too-much-data.md), when data is copied across machines.

## Go and look

Find a table or collection you've worked with and ask whether its keys were chosen for how the data is written or how it's read. They're rarely the same answer.

## The model so far

New on this page: sentence 4, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

4. **Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises.**
