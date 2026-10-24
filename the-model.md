# The model

Last reviewed: 2026-10-24

This is what the wiki is for. Each numbered part is earned on the page of the same number; follow the number to see where a sentence came from, and to argue with it. If you edit a sentence, edit it on its page, here, and in every later page's copy, in one change.

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job. ([0](00-representations.md))

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is. ([1](01-one-machine-one-program.md))

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes. ([2](02-one-machine-many-programs.md))

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve. ([3](03-programs-too-big-for-one-head.md))

4. Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises. ([4](04-data-outlives-programs.md))

5. Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so systems retry and tolerate repeats. Once data moves cheaply, distribution is free, and value shifts from copies to services, relationships, and trust. ([5](05-machines-need-to-talk.md))

6. Client and server split the work: the server owns the truth, the client owns presentation and a copy of state. Most interface bugs are two sources of truth disagreeing. The browser won because shipping one server beats shipping a million installs; native shells survive where platforms control distribution. ([6](06-anyone-can-publish.md))

7. Once strangers can reach a system, every boundary is a question of who is asking and what they may do. Trust nothing that crossed a boundary; give every party the least it needs. Harms from data fall on people other than those who collect it, so law steps in where incentives don't. ([7](07-strangers-on-the-network.md))

8. When one machine isn't enough, data is copied and split, and copies disagree for a while. Every distributed design chooses what to promise about consistency versus availability. Precompute what is read often; accept approximate answers where exactness costs too much. ([8](08-too-many-users-too-much-data.md))

9. Machines are rented by the unit, so cost is a live design variable: every architecture is also a bill. Subscription ties the vendor's revenue to the customer's continued use, and capex becoming opex changes who can start a company. An advantage competitors can't copy quickly is worth more than a better product, and most such advantages, switching costs, network effects, scale, are things engineers build or erode. ([9](09-buying-computers-is-too-slow.md))

10. Systems are built by many people over time, so the codebase is itself a system, with its own data (history), protocols (branches, reviews), and trust boundaries. Practices live in tools; choosing a tool is choosing a practice. ([10](10-many-people-one-codebase.md))

11. Everything fails; the questions are how you'll know and what you promised. Define what "working" means before measuring it. Instrument for questions you haven't asked yet. ([11](11-software-that-must-not-go-down.md))

12. Some transformations are learned from data rather than written, and are only as good as the data and the context they're given. Inference is a new kind of round trip, paid in tokens and uncertain in output, and it reintroduces every trust problem at a new boundary. ([12](12-machines-that-learn-from-data.md))

13. None of this replaced what came before; every era still runs somewhere, and some of it is there because it was first or lucky, not because it was right. Adoption is slow because switching costs are paid now by the adopter and the benefits arrive later, mostly to someone else. Nothing stays put: dependencies, data, prices, requirements, and the reasons behind them all drift, and what was rightly hand-built becomes a commodity someone else maintains. Keeping a system true to its purpose while everything around it moves is as much the job as building it. Engineering judgment is mostly knowing which limit binds now and which will lift next, and the commonest failure is adopting a solution to a problem you don't have. ([13](13-everything-still-exists-at-once.md))
