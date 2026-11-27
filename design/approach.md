# How to approach a design

Last reviewed: 2026-11-27

A guide page, not a concept page: no story of its own, just a way into the rest of this folder. It's the README's four questions, asked of a system that doesn't exist yet. Most designs fail at a question nobody asked, not at one they answered badly.

## The four questions, as a design

| The question | In a design, it becomes | Read |
| --- | --- | --- |
| What do we have? | Who uses it, what they do, how much data there is, how fast it grows, how far it can be trusted | [Estimates](estimates.md), [modelling](../data/modelling.md), [input validation](../security/input-validation.md) |
| What can we do with it? | The operations the system must do, which are reads and which are writes, and how often each | [Access patterns](../data/access-patterns.md), [choosing a data structure](../dsa/choosing.md) |
| How, and within what limits? | The plainest design that meets the numbers, and which limit binds first as they grow | [Growth](../dsa/growth.md), [latency numbers](../performance/latency-numbers.md), [partitioning](../data/partitioning.md), [replication](../data/replication.md), [caching](../performance/caching.md) |
| Why? | What it's for, what failure costs and who pays, and what the bill will be | [Measures and targets](../info/measures-and-targets.md), [the cost of reliability](../economics/reliability.md), [reading a cloud bill](../economics/cloud-bills.md) |

## A way through

Each step has something to write down. A design that's only drawn, never written, can't be checked.

1. **Say what it's for, in a user's words.** Write the two or three things that must always work ("a rider can unlock a bike") and the things that can be worse ("the map can be a minute out of date"). Everything later is judged against these. Rosa's lesson on [page 11](../11-software-that-must-not-go-down.md) was that *working* has to be defined from the customer's side.
2. **Put numbers on it.** Users, actions per user, size per action, reads per write. Then the total, for storage and the bill, and the peak, for anything that must keep up live. Round hard. See [estimates](estimates.md).
3. **Draw the data before the boxes.** What are the things, how is each one found, and what changes together? The structures follow from the questions asked of the data ([modelling](../data/modelling.md), [access patterns](../data/access-patterns.md)).
4. **Start with the plainest design that meets the numbers.** Often one server and one database. Maya on [page 8](../08-too-many-users-too-much-data.md) bought a bigger machine first, and that was right.
5. **Ask what breaks at ten times the size.** Find the one limit that binds first, such as the database's writes, memory, the network or money, and change only that. Each fix has its own page: copies for reads ([replication](../data/replication.md)), splitting for writes and size ([partitioning](../data/partitioning.md)), precomputing for slow reads ([caching](../performance/caching.md)), more servers behind a balancer ([load balancing](load-balancing.md)).
6. **Ask how it fails.** For each part, what happens when it's slow, not just when it's down. What retries, what waits, who is told no and how ([rate limiting and backpressure](rate-limiting.md), [queueing](../performance/queueing.md)). Where there are copies, what you promise while they disagree ([consistency](../data/consistency.md)).
7. **Price it.** Every architecture is also a bill, and the biggest line is often not the one you expected ([page 9](../09-buying-computers-is-too-slow.md)).
8. **Write down what you chose not to do, and the number that would change your mind.** The design will be revisited; the reasons are what the next person needs.

## Where designs usually break

- **Sized to the average.** Live capacity has to meet the peak ([estimates](estimates.md)).
- **Work in proportion to the biggest user.** The champion with 1.8 million followers on [page 8](../08-too-many-users-too-much-data.md) ([growth](../dsa/growth.md)).
- **A line that's allowed to grow.** Overload turns into waiting, and waiting into retries ([queueing](../performance/queueing.md), [rate limiting](rate-limiting.md)).
- **A check that asks the wrong question.** Machines on, customers failing ([load balancing](load-balancing.md), [sampling and observation](../info/observation.md)).
- **A round trip inside a loop.** Each one small, together most of the time ([round trips](../performance/round-trips.md)).
- **Copies treated as one.** For a while after every write they disagree ([consistency](../data/consistency.md)).
- **The bill as an afterthought.** Data transfer, storage kept forever, a managed service priced per request ([reading a cloud bill](../economics/cloud-bills.md)).

## And remember

- **There's usually more than one good design.** The choice is which cost you'd rather pay, and who pays it ([motifs](../motifs.md#costs-move-they-dont-disappear)).
- **The numbers will change.** Write down the ones you assumed, so you can tell when the design has been outgrown.
- **Interviews test this method,** under time pressure and with invented numbers. The habit is worth more than the performance: the same steps, slower, on a real system.
- **When a solution arrives before its problem,** the questions in [pushback](../pushback.md) are a good brake.

## Resources

1. Martin Kleppmann, *Designing Data-Intensive Applications* (start here: reliability, scalability and maintainability, with the data systems behind them).
2. Google, [*Site Reliability Engineering*](https://sre.google/sre-book/table-of-contents/) (go deeper: how a large company runs what it designed).
3. Alex Xu, *System Design Interview* (reference: worked interview cases, useful for practising the steps).
