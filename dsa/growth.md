# Growth

Last reviewed: 2026-11-12

A concept page: what happens to the cost of something when the amount of data grows. It's the intuition behind big-O notation, and the single most useful question in this whole folder is the one it asks: what happens at ten times the size?

## Problem

Most code is written and tested on small data, where everything is fast. Real data is bigger, and grows. Some work grows in step with the data: twice the customers, twice the time. Some grows much faster: twice the customers, four times the time, because every customer is compared with every other. On small data the two look the same. The difference only appears at a size nobody tested, usually in production, usually at the worst moment.

## The story

In 2014 Ruairí Byrne built the customer list for a small invoicing service in Dublin. Its customers were bookkeepers, and each bookkeeper had a few dozen clients. The page showed every client with their unpaid invoices. Ruairí wrote it the clearest way the framework allowed: load the bookkeeper's clients, then, for each client, load that client's invoices. Each step was one short, readable line. With the test account's twenty clients the page appeared in a fifth of a second.

In the spring an accounting firm signed up and imported four thousand clients. Their customer list took a minute and a half to load, and sometimes timed out. Ruairí opened the database log and watched it scroll: four thousand and one queries for one page. Each was quick, about twenty milliseconds, but four thousand of them in a row added up. The code hadn't changed. The number of times it went round the loop had.

He rewrote it as one query that fetched every client's invoices together, and the page came back in under a second. He was relieved, and a little embarrassed, and assumed that was the end of it.

It wasn't. The same firm then imported their history: two hundred thousand old invoices. The import had a check, written by Ruairí the year before, that stopped duplicates from being imported twice. For each new invoice it looked through all the invoices already imported to see whether one matched. With the thousand-invoice imports he'd tested, that was half a million comparisons, done in a blink. With two hundred thousand, it was about twenty billion. The import ran all night and was still going in the morning.

*Before reading on: ten times the clients had made the page ten times slower, and two hundred times the invoices made the import forty thousand times slower. What was different about the two, and what would you have changed?*

Ruairí worked it out with a pencil. The customer list did a fixed amount of work per client, so its cost grew in step with the number of clients: ten times the clients, ten times the queries. The duplicate check compared every invoice with every invoice before it, so its cost grew with the *square* of the number: twice the invoices, four times the comparisons; two hundred times the invoices, forty thousand times the work.

He rebuilt the check around a different question. Instead of asking "does any earlier invoice match this one?", which meant looking at all of them, he asked "have I seen this invoice's key before?" Each invoice's customer, number and amount went into a hash set as it was imported, and checking a new one was a single lookup however many were already there. The import's cost now grew in step with its size. Two hundred thousand invoices took four minutes.

Then he changed how he tested. Before shipping anything that worked over a list, he ran it on a hundred times more fake data than any real customer had, and counted the operations rather than just watching the clock. And he started asking one question in every code review: what happens when there are ten times as many?

Looking back, Ruairí thought neither piece of code had been wrong; both gave the right answer. What he hadn't asked was how the work grew. Code that was fine at twenty and fine at a thousand could still be hopeless at a million, and the only way to know in advance was to count how many times it went round, and what it did each time.

![A chart of how much work four kinds of code do as the data grows from 1 to 100 items. Work that grows in step with the data rises as a straight line. Work that grows as n log n rises slightly faster. Work that grows with the square of the data curves steeply upwards, and work that doubles with each extra item shoots off the top of the chart almost at once.](../images/figures/dsa-growth.svg)

*Four ways work can grow. At small sizes they look alike; at ten times the size they don't.*

## Where it shows up

| Page | What grew | How the cost grew with it |
| --- | --- | --- |
| [Round trips](../latency/round-trips.md) | Ayesha's requests, one per item on the screen | In step with the items, each one paying a full round trip: the same shape as Ruairí's customer list. |
| [Sorting](sorting.md) | Margit's runs of records | Sliding each record into place grew with the square of the run; splitting grew only a little faster than the run. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | The champion's followers | One post became 1.8 million writes, because the work grew with the follower count. |
| [Hashing](hashing.md) | Keys chosen by strangers to collide | A lookup that should take one step took as many steps as there were keys. |
| [Power and predictability](power-and-predictability.md) | One long line that nearly matched | Backtracking tried every way of splitting it, and the ways grew exponentially. |
| [Computability](computability.md) | The cities on a delivery route | The number of possible routes grows faster than any computer can keep up with, which is why approximations are used. |

It shows up elsewhere too: database queries that join without an index, nested loops over two lists, string-building in a loop that copies the whole string each time, pages that load one query per row, the number of pairs of people who might need to talk on a team as it grows, and the number of possible tests for a program with many settings.

What these share is a question about shape, not speed: when the input gets ten times bigger, does the work get ten times bigger, a hundred times, or explode? Speed is a constant you can buy. Shape decides whether buying helps at all.

## It really happened

Ruairí is fictional; his two mistakes are among the most common in software. The notation for describing how a function grows, *O(n)*, "order n", was introduced by the number theorists Paul Bachmann in 1894 and Edmund Landau soon after. Donald Knuth brought it into computing and, in 1976, set out the related notations for lower and tight bounds that computer scientists still use.

In 2021 a player who wrote under the name t0st got tired of waiting six minutes for the online mode of *Grand Theft Auto V* to load, and traced where the time went. The game read a 10-megabyte file of about 63,000 store items. The way it parsed the file re-measured the length of the whole remaining text for every item it read, and each item was checked for duplicates by comparing it with every item already stored. Both grew with the square of the number of items. Fixing just those two things cut the loading time by about 70% ([t0st, "How I cut GTA Online loading times by 70%"](https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/) <!-- verify -->). Nelson Elhage collected dozens of real cases like it in a blog called *Accidentally Quadratic*.

## What it is

Growth, or asymptotic complexity, describes how the cost of an algorithm (time, memory, round trips) changes as its input size, *n*, grows, ignoring constant factors. The common shapes are constant (*O(1)*, a hash lookup), logarithmic (*O(log n)*, binary search), linear (*O(n)*, one pass), *O(n log n)* (good sorting), quadratic (*O(n²)*, comparing all pairs) and exponential (*O(2ⁿ)*, trying every combination). Big-O usually describes the worst case; the average and the amortised case can differ. Constants still matter at real sizes, but no constant rescues the wrong shape once the data is large.

## Where it gets misapplied

- **Testing only on small data.** Ruairí's twenty clients and thousand invoices. Every shape looks fast when *n* is small.
- **A loop that does a little work per item, where the work is a round trip.** One query per row is linear in queries, and each query is expensive.
- **Comparing every pair.** Usually there's a way to ask "have I seen this?" in one step instead.
- **The mirror:** optimising the shape of code that only ever sees fifty items. An *O(n²)* loop over a list that can't grow is fine, and clearer than the clever version.

## Connections

- Learning this is also learning [hash tables](hash-tables.md), because turning "compare with everything" into "look it up" is the most common fix for quadratic code.
- Learning this is also learning [sorting](sorting.md), because the gap between sorts that grow as n² and as n log n is the clearest example of shape mattering.
- Learning this is also learning [round trips](../latency/round-trips.md), because one request per item is linear growth in the most expensive unit there is.
- Learning this is also learning [amortised cost](amortised-cost.md), because the growth of an average and the growth of the worst moment can be different things.
- Learning this is also learning [computability](computability.md), because some problems have no known solution that grows slowly, and that's a fact about the problem, not the programmer.

## Resources

1. [VisuAlgo](https://visualgo.net/en) (start here: watch how the number of steps changes as you make the input bigger). <!-- verify -->
2. Steven Skiena, *The Algorithm Design Manual*, chapter 2, on algorithm analysis (go deeper: practical, with war stories).
3. Nelson Elhage, [*Accidentally Quadratic*](https://accidentallyquadratic.tumblr.com/) (reference: real quadratic bugs in real software). <!-- verify -->

## Names you'll hear

- **Big-O, O(n):** how cost grows in the worst case, ignoring constant factors.
- **Constant, logarithmic, linear, n log n, quadratic, exponential:** the common shapes, from best to worst.
- **N+1 queries:** loading a list, then one more query per item in it.
- **Worst case, average case:** the most an operation can cost, and what it usually costs.
- **Big-Theta, big-Omega:** tight and lower bounds, the less famous relatives of big-O.

## Go and look

Find a loop in something you work on that runs over data supplied by users, and look inside it. If there's a query, a network call or another loop over the same data, work out what happens with ten times as much data. Then try it.
