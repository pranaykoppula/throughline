# Migrations

Last reviewed: 2026-10-24

A concept page: changing the shape or home of data that a running system depends on, without stopping it.

## Problem

Data's shape outlives the programs that use it, but it still has to change sometimes: a column split in two, a table moved to a new database, a format replaced. With a small system you can stop it, change everything, and start again. With a large one that runs all day, stopping isn't an option, and changing everything at once is how outages happen.

## The story

In 2010 Bilal Chaudhry worked on the accounts database at an online marketplace. Every seller had one address, stored as a single text field. Now sellers wanted separate shipping and billing addresses, and the tax team needed postcodes as their own field. The change was clear: replace one column with several, on a table of forty million sellers.

Bilal did it the way he'd always done it. He wrote a script that changed the table and copied every address into the new columns, then booked a maintenance window for two in the morning on a Sunday. On a copy of the database, the script took twenty minutes.

On the real database, with real traffic still trickling in, it locked the table. While the change ran, nothing could read or write a seller's record, which meant nobody could log in, list an item, or check out. The script was still running at four. At five, with the European morning starting, Bilal cancelled it, and cancelling took another forty minutes while the database undid what it had done. The site was effectively down for three hours, and the table hadn't changed.

*Before reading on: the change was simple, and doing it all at once had taken the site down. How would you have made it without stopping anything?*

Bilal broke the change into steps that each did something small and safe, and each could be undone. First, add the new, empty columns, which took a moment and locked nothing. Second, change the code so every write updated both the old address field and the new columns. Third, copy old addresses into the new columns in small batches, a few thousand rows at a time, pausing whenever the database got busy. That took four days and nobody noticed. Fourth, check that old and new agreed for every seller. Fifth, switch the code to read from the new columns. Sixth, after a fortnight with nothing going wrong, stop writing the old field, and finally remove it.

It took three weeks instead of one night. At every step, the site was up, and if anything looked wrong he could step back.

Looking back, Bilal thought the maintenance window had been a way of pretending the system could stop. It couldn't, not really. Treating the migration as a series of small moves, with both shapes alive for a while, was slower and far safer.

## Where it shows up

| Page | The migration | How it went |
| --- | --- | --- |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | Ines's payments, from the mainframe to new services | The big switchover failed in rehearsal; one kind of payment at a time, with both systems running and compared nightly, worked. |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Turning Walter's tree over, hospitals at the top | Rejected, because it would have broken a hundred and forty programs at once. |
| [Consistency](consistency.md) | Old and new running side by side | Two copies on purpose, which means deciding what to trust while they disagree. |
| [Data gravity](data-gravity.md) | Moving petabytes between providers | The hardest kind, because the data's size makes every step slow and costly. |

It shows up elsewhere too: database upgrades, splitting a service in two, changing an ID format, and moving from one cloud region to another.

The pages share one pattern at different sizes: let the old and new shapes coexist, move a little at a time, compare, switch, and only then remove the old. Big-bang migrations fail for the same reason Sofia's merge day did on page 10: too much change, discovered all at once.

## It really happened

Bilal is fictional; his six steps are standard practice. Stripe described the same pattern in 2017, using it to move hundreds of millions of subscription records: write to both old and new, move reads to the new, move writes to the new, then remove the old ([Stripe, "Online migrations at scale"](https://stripe.com/blog/online-migrations) <!-- verify -->). GitHub built gh-ost in 2016 because existing tools for changing large MySQL tables online were slowing its busiest tables to a near halt; it copies a table in the background and switches over at the end ([GitHub](https://github.blog/2016-08-01-gh-ost-github-s-online-migration-tool-for-mysql/)). The big-bang alternative is on [page 13](../13-everything-still-exists-at-once.md): TSB's 2018 weekend migration.

## What it is

A migration changes data's shape or location while systems depend on it. Done safely, it's a sequence of small, reversible steps: expand, by adding the new shape alongside the old; write to both; backfill old data in batches; verify; switch reads; contract, by stopping writes to the old and removing it. Each step can be paused or undone, and the system stays up throughout.

## Where it gets misapplied

- **The big-bang weekend.** Bilal's maintenance window, TSB's switchover. Everything changes at once, and nothing can be undone quickly.
- **Skipping verification.** Switching reads before checking old and new agree means trusting a copy nobody has compared.
- **Never finishing.** Leaving both shapes in place forever, so every future change has to handle two.
- **The mirror:** a six-step plan for a table with a thousand rows that nobody uses at night. Sometimes a short window really is fine.

## Connections

- Learning this is also learning [consistency](consistency.md), because during a migration there are two copies, and you must decide which to trust.
- Learning this is also learning [state machines](../dsa/state-machines.md), because untangling which states old data was really in is often the first job.
- Learning this is also learning [serialization formats](serialization.md), because changing a stored format is a migration, and good formats make it easier.
- Learning this is also learning [data gravity](data-gravity.md), because moving large data is slow enough that every migration plan has to account for it.
- Learning this is also learning [CI pipelines](../tooling/ci.md), because shipping each small step safely depends on deploying often, as Sofia learned.

## Resources

1. Stripe, ["Online migrations at scale"](https://stripe.com/blog/online-migrations) (2017) (start here: the four steps with a real example). <!-- verify -->
2. Martin Fowler, ["Strangler Fig Application"](https://martinfowler.com/bliki/StranglerFigApplication.html) (go deeper: the same idea for whole systems). <!-- verify -->
3. Your database's documentation on online schema changes (reference: what locks, and for how long).

## Names you'll hear

- **Schema migration:** changing a database's structure.
- **Expand and contract:** add the new shape alongside the old, then remove the old.
- **Dual writing:** writing to both old and new during the move.
- **Backfill:** filling the new shape with existing data, usually in batches.
- **Big bang:** changing everything at once.

## Go and look

Find the last schema change made to a database you work on and check how it was done: in one step or several, and whether it locked anything while it ran.
