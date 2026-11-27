# System design

Last reviewed: 2026-11-27

A family index. How whole systems are put together from parts: how many servers, how they share the work, what they promise when they're overloaded or broken, and how to reason about all of it before anything is built. The pages on data, performance and economics hold many of the parts; these are about putting them together. They build on one another, so they're in that order. If you arrived with a design to do, start with the guide.

## In reading order

In the order they build on one another. Each line says where the spine first needs the page.

1. [How to approach a design](approach.md): no story of its own, just a way through a design, step by step, with the page for each step. Linked from the README.
2. [Back-of-the-envelope estimates](estimates.md): a few known numbers, multiplied and rounded, tell you whether a design can work before anyone builds it. First needed on [page 8](../08-too-many-users-too-much-data.md).
3. [Load balancing](load-balancing.md): spreading requests across many servers, and the signs a balancer trusts to choose between them. First needed on [page 11](../11-software-that-must-not-go-down.md).
4. [Rate limiting and backpressure](rate-limiting.md): saying no early, clearly and fairly, when more work arrives than a system can do. First needed on [page 11](../11-software-that-must-not-go-down.md).
5. [Idempotency](idempotency.md): making an operation safe to repeat, because across a network you often can't tell whether it worked. First needed on [page 5](../05-machines-need-to-talk.md).
6. [Timeouts and circuit breakers](timeouts.md): how long to wait, what to do instead, and when to stop asking a part that's failing. First needed on [page 11](../11-software-that-must-not-go-down.md).
7. [Consensus and leader election](consensus.md): how several machines agree on one thing, such as which of them is in charge. First needed on [page 8](../08-too-many-users-too-much-data.md).
8. [Sagas](sagas.md): one piece of work across several services, without a transaction, with a planned way back for each step. First needed on [page 4](../04-data-outlives-programs.md).
9. [Asynchronous work and message queues](async-work.md): handing work off to be done later, and deciding what happens to work nobody is watching. First needed on [page 2](../02-one-machine-many-programs.md).
10. [Batch or stream](batch-or-stream.md): process data later, all at once, or as it arrives, and the two clocks in every record. First needed on [page 2](../02-one-machine-many-programs.md).
11. [Time and ordering](time-and-ordering.md): why "which happened first?" can't be answered by comparing clocks across machines. First needed on [page 5](../05-machines-need-to-talk.md).
12. [Service boundaries](service-boundaries.md): where to cut a system into parts, and whether the parts should be separate programs. First needed on [page 3](../03-programs-too-big-for-one-head.md).
