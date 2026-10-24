# 3. Programs too big for one head

Last reviewed: 2026-10-24

## Problem

Once programs grew past what one person could hold in their head, every change risked breaking something nobody remembered was connected. Programs couldn't get bigger unless people found a way to work on one part without having to understand all the others.

## The story

Elena Marsh had written assembly language for six years when, in 1968, she joined the team building a new parts-ordering system for a truck manufacturer in Ohio. She knew every instruction the machine had and how long each one took. She could make a routine faster than anyone in the building, and she was a little proud of that.

The project lead announced that the new system would be written in COBOL, a high-level language, not assembly. Elena thought it was a mistake. She'd seen what compilers produced: correct, but slower and bulkier than what she'd write by hand. She said so in the meeting. The lead didn't argue. He asked her to write the order-validation routine both ways, and to time both the code and herself.

Her assembly version ran about a third faster. It also took her three weeks, against four days for the COBOL version, and when the rules for validation changed a month later, she changed the COBOL in an afternoon. She stopped arguing. A layer between her and the machine cost her some control and some speed, and in exchange she could build far more, far faster. For most of the system, that was the better deal.

The system grew. By 1970 it was eighty thousand lines and six people, and nobody could hold all of it. They had divided the work the way everyone did, by following the flowchart: one module read the day's orders, the next validated them, the next looked up each part, the next priced the order, the last printed the picking lists. Each person owned a step. It matched how the work flowed on paper, it was easy to explain to management, and Elena agreed with it.

Then the manufacturer merged with a competitor, and the merged company changed its part numbers from six digits to nine letters and digits. It sounded like a small change. It took three months. Every module had been written knowing exactly what a part number looked like: the reader parsed it, the validator checked it, the lookup searched on it, the pricer split it to find the product line, the printer laid it out in a column six characters wide. All five changed. Bugs turned up in places nobody had thought to look, and twice a fix in one module broke another. Everyone had done their job well. The way they'd divided the job was the problem.

*Before reading on: if you were splitting this system again, what would you put inside each piece?*

A colleague passed Elena a paper by a researcher named David Parnas. Its argument was simple and, to her, slightly annoying because it was so obvious once said. Don't divide a program by the steps it goes through. Divide it by the decisions that are likely to change, and hide each decision inside one module, so that nobody else depends on it. If part numbers might change, one module should be the only code that knows what a part number looks like. Everyone else just asks it to find a part, check a part, or print a part.

They restructured over the next year, slowly, between other work. The new "parts catalogue" module was the only code that knew what part numbers looked like or how parts were stored. When the company changed the format again in 1972, Elena changed one module in two weeks, and nothing else broke.

The real test came later, when orders doubled and the nightly run started overrunning into the morning shift. Elena was sure she knew why. The sorting routine was slow and she'd been wanting to rewrite it in assembly for a year. A younger colleague asked her to measure first. They added counters to every module and ran a night's orders. The sort took four percent of the time. More than half went on looking up parts. The catalogue module searched its list of parts from the top every time it was asked. That was fine with two thousand parts. With forty thousand parts it was very slow.

She replaced the list, inside the module, with a hash table. It was a structure built for exactly what the catalogue was being asked to do over and over: find one item by its key. Because the rest of the system only ever asked the catalogue to find a part, nothing outside it changed. The lookups ran thirty times faster and the night run finished by three. She never rewrote the sort.

Looking back, Elena thought the lesson ran in layers, like the systems themselves. The language had traded control for ease, and that had been worth it. The modules let six people work without holding the whole system in their heads, but only once each module hid a decision instead of a step. And when something was too slow, the answer wasn't to give up the abstraction. It was to measure, find the one piece that mattered, and replace it with something made for the job. Most of her work was putting existing pieces together. The skill was knowing which piece to replace, and only after measuring.

## It really happened

Elena is fictional; the arguments she had were real. The FORTRAN team at IBM in the 1950s knew programmers wouldn't trust a compiler unless its code was nearly as fast as hand-written code. John Backus later wrote that they treated language design as the easy part and spent their effort on optimization, because without efficient programs nobody would have adopted it ([Backus, "The History of FORTRAN I, II, and III", 1978](https://users-cs.au.dk/askarov/dovs/p165-backus.pdf)). Parnas's paper is real too, and his example is the one Elena lived through: a system divided by processing steps against one divided by hidden decisions ([Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules", *CACM*, 1972](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf)).

Elena's sort-versus-lookup lesson has a famous line attached, usually quoted by half. Donald Knuth, 1974: "We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%." The second sentence is the part people cut.

Forty years later the same question, "is the language the bottleneck?", got answered both ways. Facebook built HipHop to turn its PHP into C++ and reported roughly halving web server CPU use (2010). Twitter replaced the Ruby front end of search with a Java server and reported search latency falling to about a third ([Twitter, 2011](https://blog.twitter.com/2011/twitter-search-now-3x-faster)) <!-- verify -->. Both measured first, both at a scale most teams never reach, and both posts are companies describing themselves. Twitter's own account says part of the problem was how Ruby processes were run, one request at a time each, not only the language ([page 2](02-one-machine-many-programs.md)). Ladder: both moved down, after measurement.

## What survived

Abstraction is the core skill: layers (languages, libraries, modules, types) that let you use something without knowing how it works. Each layer trades control for ease. The best boundaries hide a decision that might change, not a step in a process. Building is mostly assembling existing abstractions. Optimizing is mostly replacing one of them with something made for the case at hand, once measurement shows its cost dominates. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

## Where it gets misapplied

- **Rewriting a working system in the new thing.** Throwing away code throws away every bug fix in it (Joel Spolsky, ["Things You Should Never Do, Part I"](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/)). <!-- verify -->
- **Framework churn and not-invented-here.** Swapping abstractions because they're new, or building your own because the existing one isn't yours. Both skip the measuring.
- **Optimizing the part you're sure about.** Elena's sort. Without measurement, intuition about where the time goes is usually wrong.
- **The mirror:** never replacing an abstraction at all, and paying its cost forever because nobody measured it. A query library generating thousands of queries per page is the usual example.

## Connections

- Learning this is also learning [hash tables](dsa/hash-tables.md), because Elena's fix was choosing the structure built for her access pattern: find one item by its key.
- Learning this is also learning [hardware](01-one-machine-one-program.md), because "compiled", "interpreted" and "garbage collected" are all prices paid at the layer underneath.
- Learning this is also learning [build systems and package managers](tooling/build-systems.md), because they're abstractions for managing other abstractions, and they break in the same ways.
- Learning this is also learning [type systems](runtimes/type-systems.md), because a type is a boundary the compiler enforces, so people don't have to remember it.
- Learning this is also learning [collaboration](10-many-people-one-codebase.md), because a module boundary is also a boundary between people, and types are documentation for the next person.
- Learning this is also learning [representations](00-representations.md), because every abstraction is a representation, and it has an edge where the layer underneath shows through.

## Resources

1. David Parnas, ["On the Criteria To Be Used in Decomposing Systems into Modules"](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf) (start here: six pages, and Elena's whole story).
2. John Ousterhout, *A Philosophy of Software Design* (go deeper: "deep modules" is Parnas's idea, fifty years on).
3. Fred Brooks, *The Mythical Man-Month* (1975): what happens when programs and teams get big at the same time.
4. Steven Skiena, *The Algorithm Design Manual* (reference: the catalogue of shapes, organised by the problem you have).

## Names you'll hear

- **Information hiding** (Parnas): a module's job is to hide a decision.
- **Turing-complete:** a language that can compute anything any computer can. Nearly all are, which is why the choice between them is about ease, not power.
- **Second-system effect** (Brooks): the follow-up to a successful system tends to be overbuilt.
- **Hyrum's law:** with enough users, every observable behaviour of your module is depended on by someone, hidden or not.
- **Worse is better** (Richard Gabriel): simpler and less correct often spreads faster and wins.
- **Dijkstra:** you'll hear his name for structured programming ("Go To Statement Considered Harmful", 1968), the first big argument that how code is organised matters as much as what it does.

## Go and look

Find a type or data format that's hand-copied across a boundary in something you've built: the same shape defined in the frontend and the backend, say. That's an abstraction boundary maintained by a person instead of a compiler. Ask what decision it should be hiding.

## The model so far

New on this page: sentence 3, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. **Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.**
