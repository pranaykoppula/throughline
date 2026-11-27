# System design

Last reviewed: 2026-11-27

A family index. How whole systems are put together from parts: how many servers, how they share the work, what they promise when they're overloaded or broken, and how to reason about all of it before anything is built. The pages on data, performance and economics hold many of the parts; these are about putting them together. They build on one another, so they're in that order. If you arrived with a design to do, start with the guide.

## In reading order

In the order they build on one another. Each line says where the spine first needs the page.

1. [How to approach a design](approach.md): no story of its own, just a way through a design, step by step, with the page for each step. Linked from the README.
2. [Back-of-the-envelope estimates](estimates.md): a few known numbers, multiplied and rounded, tell you whether a design can work before anyone builds it. First needed on [page 8](../08-too-many-users-too-much-data.md).
3. [Load balancing](load-balancing.md): spreading requests across many servers, and the signs a balancer trusts to choose between them. First needed on [page 11](../11-software-that-must-not-go-down.md).
4. [Rate limiting and backpressure](rate-limiting.md): saying no early, clearly and fairly, when more work arrives than a system can do. First needed on [page 11](../11-software-that-must-not-go-down.md).

More pages are planned: making retries safe, stopping failures from spreading, how machines agree, work across services, service boundaries, and time and ordering.
