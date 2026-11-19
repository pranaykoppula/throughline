# Algorithms and data structures

Last reviewed: 2026-11-19

A family index. The reusable shapes inside programs: the ways of keeping data so that the questions you ask of it are cheap, and the ways of working out an answer from it. It's a toolkit, so it's ordered by what builds on what, not by where the spine first needs each page. If you arrived with a problem rather than a curiosity, start with the guide.

## In reading order

In the order they build on one another. Each line says where the spine first needs the page.

1. [Choosing a data structure](choosing.md): no story of its own, just a way into the rest of this folder. Linked from the README.
2. [Growth](growth.md): what happens to the cost of something when the amount of data grows. First needed on [page 8](../08-too-many-users-too-much-data.md).
3. [Arrays and linked lists](arrays-and-linked-lists.md): the two simplest ways to keep a sequence, and why the one that's worse on paper is often faster in practice. First needed on [page 1](../01-one-machine-one-program.md).
4. [Hashing](hashing.md): turning any key into a short, fixed-size stand-in computed from the key itself, so you can find it, place it or check it without comparing it against everything else. First needed on [page 3](../03-programs-too-big-for-one-head.md).
5. [Hash tables](hash-tables.md): finding things by key in constant time, and what it costs to keep it that way. First needed on [page 3](../03-programs-too-big-for-one-head.md).
6. [Amortised cost](amortised-cost.md): some operations are cheap almost every time and occasionally very expensive, so that the average is excellent and one moment in a thousand is terrible. First needed on [page 3](../03-programs-too-big-for-one-head.md).
7. [Sorting](sorting.md): putting things in order is an investment. First needed on [page 10](../10-many-people-one-codebase.md).
8. [Divide and conquer](divide-and-conquer.md): split a problem into smaller ones of the same kind, solve those, and combine the answers. First needed on [page 3](../03-programs-too-big-for-one-head.md).
9. [Search](search.md): finding what someone is looking for, among more than they could ever read. First needed on [page 3](../03-programs-too-big-for-one-head.md).
10. [Tries](tries.md): a tree that stores words by their letters, so that everything sharing a beginning shares a path. First needed on [page 6](../06-anyone-can-publish.md).
11. [B-trees](b-trees.md): the structure behind most database indexes, shaped by the cost of reading from disk. First needed on [page 4](../04-data-outlives-programs.md).
12. [LSM trees](lsm-trees.md): a storage structure that makes writes cheap by doing them later, in bulk. First needed on [page 4](../04-data-outlives-programs.md).
13. [Append-only logs](append-only-logs.md): instead of changing a record in place, write down what happened, in order, and never change what's written. First needed on [page 4](../04-data-outlives-programs.md).
14. [Bloom filters](bloom-filters.md): a tiny summary of a set that can say "definitely not in here" for certain, and "possibly in here" with a known chance of being wrong. First needed on [page 4](../04-data-outlives-programs.md).
15. [Exact or approximate](exact-or-approximate.md): some questions don't need an exact answer, and a good-enough answer can cost a tiny fraction of the space and time. First needed on [page 8](../08-too-many-users-too-much-data.md).
16. [Merkle DAGs](merkle-dags.md): naming data by the hash of its contents, and building trees of those names, so one short value can vouch for everything beneath it. First needed on [page 10](../10-many-people-one-codebase.md).
17. [Queues](queues.md): the data structure behind waiting in line, and the rules for deciding who goes next. First needed on [page 2](../02-one-machine-many-programs.md).
18. [Heaps and priority queues](heaps.md): a structure that always knows which item is most urgent, and can take it away or add a new one cheaply, without keeping everything in order. First needed on [page 2](../02-one-machine-many-programs.md).
19. [Graphs](graphs.md): things and the connections between them, and the questions you can ask of any network. First needed on [page 2](../02-one-machine-many-programs.md).
20. [Greedy algorithms](greedy.md): build an answer by always taking the step that looks best right now, and never going back. First needed on [page 5](../05-machines-need-to-talk.md).
21. [Dynamic programming](dynamic-programming.md): when a problem breaks into smaller problems that keep recurring, solve each one once, write the answer down, and build the big answer from the table. First needed on [page 10](../10-many-people-one-codebase.md).
22. [State machines](state-machines.md): naming every state something can be in, and every allowed way to move between them. First needed on [page 5](../05-machines-need-to-talk.md).
23. [Power and predictability](power-and-predictability.md): the more a language can express, the less you can know about what a program written in it will do. First needed on [page 3](../03-programs-too-big-for-one-head.md).
24. [Computability](computability.md): some questions about programs can't be answered by any program, and recognising them saves years. First needed on [page 0](../00-representations.md).
