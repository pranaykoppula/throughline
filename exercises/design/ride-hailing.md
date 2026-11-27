# The nearest car

A design case in the category **location and matching**. It draws on [partitioning](../../data/partitioning.md), [service boundaries](../../design/service-boundaries.md), [timeouts](../../design/timeouts.md), [load balancing](../../design/load-balancing.md) and [state machines](../../dsa/state-machines.md).

## The situation

A ride-hailing company operates in thirty cities. Riders ask for a car; the system offers the request to a nearby driver, who has fifteen seconds to accept; if they don't, it offers it to the next. Drivers' phones report their position every few seconds. In the first version, a rider's request was matched by asking the database for every available driver within three kilometres and choosing the closest. On New Year's Eve in the largest city, the database spent its time answering location updates, matches took a minute, and some drivers were sent two riders at once.

## Requirements and numbers

- Match a rider to a suitable nearby driver within a few seconds.
- Never give one driver two riders at once, and never send two drivers to one rider.
- Driver positions fresh to within a few seconds; a rider sees their driver approach on a map.
- Handle a driver ignoring, declining or losing signal mid-offer.
- About 300,000 drivers online at the busiest moment, each reporting every 4 seconds; up to 5,000 ride requests a second on New Year's Eve, nearly all of them in a few cities.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** A huge stream of positions that are useful for a few seconds and then worthless, and a small stream of requests that matter a great deal.
- **What must always work?** One driver, one rider, at a time.
- **How does it fail?** Phones lose signal, drivers ignore offers, and one city's peak arrives while the others sleep.

## The tempting first design

Store each driver's latest position in a table and update it every four seconds. To match, query available drivers within three kilometres, compute distances, pick the closest, and set their status to busy.

300,000 drivers every four seconds is 75,000 position writes a second into the table that matching reads from. A query for "drivers within three kilometres" on latitude and longitude columns scans a wide band of the city unless the index understands space. And between reading "available" and writing "busy", another request can choose the same driver.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Positions are worthless after a few seconds. Do they need to go into a durable database at all, or only somewhere fast that remembers the latest one?

</details>

<details markdown="1"><summary>Hint 2</summary>

Divide each city into cells, such as hexagons a few hundred metres across. Which cells would you search to find drivers near a rider, and how would you keep a list of the drivers in each?

</details>

<details markdown="1"><summary>Hint 3</summary>

A driver can be offered only one ride at a time. What single operation could move a driver from "available" to "offered this ride" so that two requests can't both do it?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

75,000 position updates a second, each tiny, is easy for an in-memory store spread over a few machines and hard for a database that also keeps every update. Requests peak at 5,000 a second but concentrate in a few cities, so the design should partition by place, and the busiest city must be able to have more capacity than the rest ([estimates](../../design/estimates.md)).

### Design A: cells in memory, a matcher per area

- **Cells.** Each city is covered by a grid of cells a few hundred metres across. A driver's position update says "driver 7731 is in cell X". An in-memory index per area holds, for each cell, the set of available drivers in it ([hash tables](../../dsa/hash-tables.md)). To find drivers near a rider, look up the rider's cell and the rings of cells around it until there are enough candidates; then rank them by estimated driving time, not straight-line distance.
- **Partitioned by area.** Areas, groups of cells, are spread across matcher machines; a busy city has many areas and many machines, a quiet one few ([partitioning](../../data/partitioning.md)). Position updates are routed to the machine that owns the driver's area ([load balancing](../../design/load-balancing.md) by key, not at random).
- **Positions aren't records.** Only the latest position is kept in memory. A sample of positions is written to a log for trip records and analysis, separately and asynchronously ([asynchronous work](../../design/async-work.md)).
- **Each driver is a state machine.** Available → offered → on the way → on trip → available. Moving from available to offered is a single conditional update on the driver's state, owned by one machine, so two requests can't both win ([state machines](../../dsa/state-machines.md)).
- **Offers time out.** An offer expires after fifteen seconds without an answer, and the driver returns to available, perhaps with a note to offer them less for a while ([timeouts](../../design/timeouts.md)).
- **Separate services, for reasons.** Matching, trips and payments are separate: matching changes often and needs to scale per city; payments has its own auditors; trips are the durable record ([service boundaries](../../design/service-boundaries.md)).

**What it costs:** matching state that lives in memory; if a matcher machine dies, drivers in its areas are invisible until their next position update, a few seconds later.

### Design B: batch matching every few seconds

Instead of matching each request as it arrives, collect the requests and available drivers in an area for two seconds, then solve the assignment for the whole batch at once, minimising total pickup time.

**What it gives:** better matches overall. Greedy matching gives the closest driver to the first rider even when a slightly worse choice would let a second rider be served much faster ([greedy algorithms](../../dsa/greedy.md)).

**What it costs:** up to two seconds' extra wait for every rider, and a harder problem to solve in time at the peak. Many services use small batches in dense areas and immediate matching elsewhere.

</details>

## What breaks at ten times the size

- **One giant event.** A stadium emptying puts thousands of requests in a handful of cells; split hot areas into smaller ones on their own machines, and queue riders fairly rather than all at once ([rate limiting](../../design/rate-limiting.md)).
- **Areas at the edges.** A rider near the boundary of two areas needs drivers from both; the matcher must ask its neighbour, which adds a round trip.
- **Estimated arrival times.** Ranking by driving time needs a routing service; at ten times the volume, cache times between cells rather than routing every pair.

## Where people slip

- **Storing every position in the main database.** Most positions are worthless seconds later; keep the latest in memory.
- **Searching by latitude and longitude ranges.** A spatial index, such as cells, makes "near" a lookup.
- **Read, then write a driver's status.** Two requests choose the same driver; make the change one conditional update.
- **Straight-line distance.** The closest driver may be across a river.
- **Offers with no expiry.** A driver who never answers holds the rider for ever.

## Related

- The other case in this category: [the café round the corner](places-near-me.md), "places near me" search.
- Design pages: [service boundaries](../../design/service-boundaries.md), [timeouts](../../design/timeouts.md), [load balancing](../../design/load-balancing.md), [asynchronous work](../../design/async-work.md), [rate limiting](../../design/rate-limiting.md).
- Other pages: [partitioning](../../data/partitioning.md), [state machines](../../dsa/state-machines.md), [hash tables](../../dsa/hash-tables.md), [greedy algorithms](../../dsa/greedy.md), [graphs](../../dsa/graphs.md).
