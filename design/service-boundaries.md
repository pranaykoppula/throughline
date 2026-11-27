# Service boundaries

Last reviewed: 2026-11-27

A concept page: where to cut a system into parts, and whether the parts should be separate programs. A boundary is worth its price only where it hides a decision that changes on its own, and a boundary across a network has a much higher price than one inside a program.

## Problem

Large systems are divided so that people can work on them without holding all of them in their heads. The division can be inside one program, as modules, or between programs, as services that talk over the network. Services let teams deploy on their own and let parts scale and fail separately, which is why they became fashionable. But every boundary costs something: an interface that must be agreed, a call that can fail, data that can't be joined, a release that has to be coordinated. Drawn in the wrong place, boundaries multiply all of those costs and buy nothing.

## The story

In 2018 Thandiwe Mokoena became head of engineering at an insurance company in Cape Town that sold car and home cover online. Its quoting system was one large program, ten years old, and its eight engineers spent more time waiting for each other's changes than making their own. The board had read about companies that moved fast with many small services, and Thandiwe agreed. Over a year the team split the program into fourteen services: customers, addresses, vehicles, properties, policies, prices, discounts, documents, payments, and so on. Each was a noun in the system, each had its own database, and the team had grown to five squads of four, each owning a few services. It was what the books and the conference talks described, and the first months felt freer.

Then the company decided to sell pet insurance. It was a modest product: a pet, an owner, a price, a policy document. Building it touched nine of the fourteen services. Customers needed a new kind of thing to insure, prices needed new rules, discounts needed new combinations, documents needed a new template, and each change needed a new version of the interface between two services, agreed between two squads and released in the right order. It took four months. And a single quote, which used to be one program reading one database, now made about thirty calls across the network, so it was slower than before, and when the discounts service had a bad afternoon, no one in the country could get a quote for anything.

*Before reading on: every service was small and well made. Why was the system harder to change than the one it replaced?*

Thandiwe saw that the team had cut along the nouns, and the changes ran across them. A new product touched customers, prices, discounts and documents all at once, because those were the things a product was made of. The boundaries had put each change in many places. A colleague showed her a paper from 1972 about a much older system that had made the same mistake with modules: it had divided the program by the steps of its flowchart, and every change to a part number touched all of them. The paper's advice was to put each decision that was likely to change inside one part, and hide it there.

So she redrew the boundaries around what changed together and who changed it. Car, home and pet insurance each became one part, owned by one squad, containing its own rules for pricing, discounts and documents. Most of those parts went back into one program, as modules whose boundaries were checked by tools rather than by the network, so that a quote became a few function calls again. Only a few things stayed as separate services, each for a reason that could be written down: payments, which had its own security rules and auditors; document generation, which used a lot of computing power at the end of each month and needed to scale on its own; and a shared service for customers' identities, which every product used and nobody wanted to copy.

![Two diagrams of the same quoting system. Before: fourteen services named after nouns, with nine of them highlighted because adding pet insurance changed each one, and about thirty calls for a single quote. After: three product modules inside one program, plus three separate services for payments, documents and identity; adding pet insurance changes one module, and a quote makes four calls.](../images/figures/design-service-boundaries.svg)

*Boundaries cut along the nouns put every change in many places. Cut along what changes together, and most changes stay in one.*

Looking back, Thandiwe thought the mistake had been treating the network as the boundary. What the engineers had needed was boundaries in the right places, and most of those could live inside one program. A separate service was a tool for a few specific problems, and each one cost something every day whether it solved one or not.

## Where it shows up

| Page | The boundary | What it taught |
| --- | --- | --- |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | Elena's modules, divided by the steps of a flowchart | Divide by the decisions likely to change, and hide each one; dividing by steps puts every change in every module. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Services split before the team or the load needed them | Segment's services folded back into one; boundaries have running costs. |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | Sofia's teams sharing one codebase | The way people are divided shows up in the code, and the friction of working together shows up at the boundaries. |
| [Round trips](../performance/round-trips.md) | Every call that crosses a network | A function call takes nanoseconds; a call to another service, milliseconds and a chance of failure. Thirty of them make a slow quote. |
| [Sagas](sagas.md) | Tolu's three services, each with its own database | A boundary between databases removes the transaction; work that crosses it needs a way back for every step. |
| [Data modelling](../data/modelling.md) | What the things in a system are | The nouns are a model of the data, not necessarily a good division of the work. |

It shows up elsewhere too: how a company is divided into departments, and the forms that pass between them; a hospital organised by medical specialty or by patient pathway; the division of a book into chapters; and the joke that you can tell how many teams built a system by counting its parts.

What the rows share is that a boundary is a bet about which changes will come. A good one puts each likely change inside one part; a bad one makes every change a negotiation. A boundary across a network makes the bet more expensive to lose.

## It really happened

Thandiwe is fictional, and so is her insurer. The 1972 paper is real: David Parnas's "On the Criteria To Be Used in Decomposing Systems into Modules", whose two decompositions of the same program are the source of Elena's story on [page 3](../03-programs-too-big-for-one-head.md). The observation that systems take the shape of the organisations that build them is Melvin Conway's, from 1968 (see [forces](../forces.md)).

Shopify, one of the largest Ruby on Rails applications, chose in 2019 not to split into services. It kept its code in one program and divided it into components with boundaries enforced by tooling, which it called a modular monolith, to get clearer ownership "without increasing the number of deployment units" ([Shopify Engineering, "Deconstructing the Monolith"](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)). Segment's move in the other direction, from many services back to one, is described on [page 8](../08-too-many-users-too-much-data.md).

## What it is

A **boundary** divides a system into parts with an interface between them. Inside one program the parts are **modules**; between programs they're **services**, communicating over a network. Good boundaries follow Parnas's rule, each hiding a decision likely to change, and in practice often follow business capabilities (what the organisation does) rather than data nouns, since changes come from the business. Domain-driven design calls such a part a **bounded context**: an area within which words and rules have one meaning. A service boundary adds independent deployment, scaling and failure isolation, and costs network calls, partial failures, lost transactions and joins, versioned interfaces, and operational work for each service. A **modular monolith** keeps the boundaries and drops the network. The useful question for any proposed service is which of its benefits is needed, and whether a module would provide it.

## Where it gets misapplied

- **Boundaries along nouns.** Customers, products and orders each become a service, and every feature changes all of them.
- **Services before the need.** Splitting a system that a small team can still hold in its head buys the costs and none of the benefits.
- **A distributed monolith.** Services that must be released together, and fail together, are one program with a network in the middle.
- **Sharing a database between services.** The boundary exists in the code and not in the data, so every schema change is everyone's change.
- **The mirror:** one program long after it has outgrown its team, where every change waits for every other and a fault anywhere stops everything.

## Connections

- Learning this is also learning [abstraction and modules](../03-programs-too-big-for-one-head.md), because a service is a module with a network around it, and the same rule for where to cut applies.
- Learning this is also learning [round trips](../performance/round-trips.md), because a boundary across a network turns every function call into a slow, fallible message.
- Learning this is also learning [sagas](sagas.md), because work that crosses a boundary between databases loses its transaction.
- Learning this is also learning [data modelling](../data/modelling.md), because the things in a system are a model of the data, not automatically a division of the work.
- Learning this is also learning [timeouts and circuit breakers](timeouts.md), because every service boundary is a dependency that can be slow, and its callers need limits.
- Learning this is also learning [how to approach a design](approach.md), because where the boundaries go is decided by which limit binds, not by fashion.

## Resources

1. David Parnas, ["On the Criteria To Be Used in Decomposing Systems into Modules"](https://dl.acm.org/doi/10.1145/361598.361623) (1972) (start here: short, and still the clearest statement of where to cut).
2. Shopify Engineering, ["Deconstructing the Monolith"](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity) (2019) (a large system choosing modules over services, and why).
3. Sam Newman, *Building Microservices*, second edition (2021) (go deeper: when services are worth it, and how to split).
4. Eric Evans, *Domain-Driven Design* (2003) (reference: bounded contexts).

## Names you'll hear

- **Monolith, modular monolith:** one program; one program with enforced internal boundaries.
- **Microservices:** many small, separately deployed services.
- **Distributed monolith:** services that can only be changed and released together.
- **Bounded context:** a part of the system in which terms have one meaning.
- **Conway's law:** systems take the shape of the organisations that build them.
- **Coupling, cohesion:** how much parts depend on each other, and how much a part's contents belong together.

## Go and look

Find the last feature you shipped and count the parts it changed: modules, services, repositories or teams. If it was more than two, ask whether the boundaries follow the way your system changes, or the way its data is shaped.

Practise this: [the nearest car](../exercises/design/ride-hailing.md), where matching, trips and payments are separate for stated reasons, and [the lecture that buffered](../exercises/design/video-streaming.md), where uploads, transcoding and playback need different things.
