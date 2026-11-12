# Append-only logs

Last reviewed: 2026-11-12

A concept page: instead of changing a record in place, write down what happened, in order, and never change what's written. The current state becomes something you work out from the record. Accountants have done this for six hundred years; databases, version control and message systems all rediscovered it.

## Problem

The obvious way to **store** state is to keep the current value and overwrite it when it changes: a balance, a stock level, an address. It's compact and simple to read. But an overwrite destroys the old value, and with it the answer to every question about how the value came to be. When two updates race, one can silently erase the other. When a bug writes a wrong value, there's nothing to rebuild from. And when someone asks *why* the number is what it is, nobody can say.

## The story

In 2015 Teresa Ferreyra was the lead engineer at a mobile wallet startup in Buenos Aires. Customers topped up at kiosks, sent money to each other and paid in shops. The design was what every tutorial showed: each account had a row in the database with its current balance. A payment subtracted from one row and added to another, inside a transaction so both happened or neither did. It was simple, fast and easy to check: the balance was right there.

The first problem came from support. A customer insisted she'd topped up five hundred pesos that never arrived; the balance said otherwise, and nobody could show her why. The application logs had rotated away. The database knew what her balance *was*, not how it had become that.

The second problem was worse. A bug in a promotion gave a cashback bonus to some accounts twice and, in a few cases, wrote a corrupted value over the balance entirely. The team found it three days later. By then each affected balance had changed dozens of times since. There was no way to tell what the balance should have been, because every change had been written over the one before. They restored a backup into a separate database and spent two weeks reconciling by hand, account by account, against the payment provider's records.

*Before reading on: the balances were always the current truth, and the current truth turned out to be the one thing they couldn't rebuild. What would you have stored instead?*

Teresa changed what the system treated as the truth. From then on it never stored a balance as a fact. It stored *movements*: every top-up, payment, fee and bonus became an entry in a ledger, written once and never changed, each recording which account money left, which account it entered, how much, when, and why. Every entry balanced, the way an accountant's double entry does: money out of one account was always money into another, so the whole ledger summed to zero and money couldn't appear from nowhere. An account's balance was simply the sum of its entries.

Mistakes were never erased. When the next promotion bug credited a bonus twice, the fix was a new entry reversing the duplicate, with a note saying why, and both stayed in the ledger for anyone to see. Support could answer any question by reading the account's entries in order. And the bug that had cost two weeks would now have cost an afternoon: find the bad entries, add reversals.

Summing every entry each time someone opened the app would have been slow, so the system kept the current balance too. But it was a *derived* value, a cache, recomputed from the ledger and checked against it every night. If the two ever disagreed, the ledger won. Over the years the ledger grew to billions of entries, so older entries were rolled up into dated opening balances and moved to cheaper storage, the way an accountant closes the books each year.

Looking back, Teresa thought the original design had kept the answer and thrown away the working. That was fine for a calculator and wrong for anything someone might need to question. A log of what happened could always produce the current state, and it could explain itself. The current state alone could do neither.

![Two ways to store a wallet. Left: one balance per account, overwritten by each change, with a corrupted value and no way back. Right: a ledger of entries, each written once, with a duplicate bonus corrected by a reversing entry, and the balance worked out as the sum of the entries.](../images/figures/dsa-append-only-logs.svg)

*The same account, stored as a balance and as a ledger. Only the ledger can explain itself.*

## Where it shows up

| Page | The log | What deriving from it gave |
| --- | --- | --- |
| [LSM trees](lsm-trees.md) | Neha's writes, appended to a log and to sorted files | Fast writes, and a log to rebuild memory from after a crash. |
| [4, Data outlives programs](../04-data-outlives-programs.md) | The database's own record of each change in a batch | Walter's payments undone cleanly after a power cut, because the database had logged them before applying them. |
| [Merkle DAGs](merkle-dags.md) | Git's history of commits | Nothing in the past is changed; a new commit points at the old ones, and history can always be read back. |
| [Replication](../data/replication.md) | The main database's log of changes | A replica that applies the same log in the same order ends in the same state. |
| [Commit messages and design records](../writing/commit-messages.md) | The reasons behind a codebase's changes | Decisions explained by reading what happened, in order. |

It shows up elsewhere too: double-entry bookkeeping, bank statements, message systems such as Kafka, event sourcing in application design, audit trails in medicine and aviation, blockchains, and laboratory notebooks, where mistakes are crossed out with a single line so they can still be read.

What these share is the decision to keep what happened rather than what's true now. State becomes a view computed from the log, which can be rebuilt, checked, replayed elsewhere, and explained. The costs are space, and the work of rolling up or compacting old entries.

Motif: [copies disagree](../motifs.md#copies-disagree).

## It really happened

Teresa is fictional; her ledger is the oldest idea on this page. Double-entry bookkeeping was in use among Italian merchants by the fourteenth century, and Luca Pacioli set it out in print in 1494, in a section of his *Summa de arithmetica*. Its rules are Teresa's: every transaction is recorded twice, as a debit and a credit, entries are never erased, and errors are corrected by further entries.

Databases rediscovered it as the write-ahead log: before changing data, record the change in a log, so a crash can be recovered by replaying or undoing what was logged. In 2013 Jay Kreps, an engineer at LinkedIn, argued that the log, "an append-only, totally-ordered sequence of records ordered by time", was the unifying idea behind databases, replication and data integration. His team had built Apache Kafka around it ([Kreps, "The Log"](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)).

## What it is

An append-only log is a sequence of records that can only be added to at the end and is never modified. State is derived by reading the log, often cached as a snapshot or materialised view that can be rebuilt. Corrections are new records, not edits. Logs make history, auditing, replication (apply the same log elsewhere), recovery (replay after a crash) and debugging possible, and they turn concurrent overwrites into ordered appends. Their costs are storage, slower reads unless state is cached, and the need to compact or snapshot old records. Event sourcing applies the idea to application design; write-ahead logs, LSM trees and message brokers apply it inside infrastructure.

## Where it gets misapplied

- **Storing only the current value of something people will question.** Balances, stock levels, permissions and prices all get asked "why?".
- **Editing the log.** A log with corrections made in place is just a table with extra steps; fix mistakes with new entries.
- **Never compacting.** A log nobody rolls up becomes a storage bill and a slow start-up.
- **The mirror:** event sourcing everything. A user's preferred colour scheme doesn't need an audit trail, and deriving every screen from events adds real complexity.

## Connections

- Learning this is also learning [LSM trees](lsm-trees.md), because they're a log made fast to read, with compaction as the price.
- Learning this is also learning [replication](../data/replication.md), because a replica is a second reader of the same log.
- Learning this is also learning [Merkle DAGs](merkle-dags.md), because git's history is an append-only log whose entries vouch for everything before them.
- Learning this is also learning [caching](../latency/caching.md), because a balance derived from a ledger is a cache, and the ledger wins when they disagree.
- Learning this is also learning [migrations](../data/migrations.md), because a log of what happened lets you rebuild state in a new shape without guessing what the old shape meant.

## Resources

1. Jay Kreps, ["The Log: What every software engineer should know about real-time data's unifying abstraction"](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) (2013) (start here).
2. Martin Kleppmann, *Designing Data-Intensive Applications*, chapters 3 and 11 (go deeper: logs inside storage engines and as the backbone of data systems).
3. Martin Fowler, ["Event Sourcing"](https://martinfowler.com/eaaDev/EventSourcing.html) (reference: the application-design version, with its costs). <!-- verify -->

## Names you'll hear

- **Append-only, immutable:** written once, never changed.
- **Write-ahead log (WAL):** a database's record of changes, written before the changes are applied.
- **Event sourcing:** storing an application's state as the events that produced it.
- **Snapshot, materialised view, projection:** state derived from a log and kept for fast reading.
- **Compaction, closing the books:** rolling old entries up so the log stays manageable.
- **Double-entry bookkeeping:** recording every transaction as a matching debit and credit.

## Go and look

Find a number in something you run that people sometimes question, such as a balance, a count or a status. Try to answer "how did it get to be this value?" from what the system stores. If you can't, consider what it would take to keep the history.
