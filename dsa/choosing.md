# Choosing a data structure

Last reviewed: 2026-11-12

A guide page, not a concept page: no story of its own, just a way into the rest of this folder. Every data structure is an answer to a question someone kept asking of their data. Start from the question, and the structure usually follows.

## Start from the question

Ask what you'll do to the data most often, in the words you'd use for it. Each of these is a way to **find** something, and each has a structure built for it.

| If you keep asking… | Reach for | Because | Read |
| --- | --- | --- | --- |
| "Give me the item with this key" | A hash table | One step, however many items there are | [Hash tables](hash-tables.md), [hashing](hashing.md) |
| "Give me everything between these two values", or "the next one in order" | A sorted array, or a tree such as a B-tree | Order lets you jump to the start of a range and walk from there | [Sorting](sorting.md), [B-trees](b-trees.md) |
| "What's the most urgent thing now?" | A heap, as a priority queue | It always keeps the smallest (or largest) on top, cheaply | [Heaps and priority queues](heaps.md) |
| "What's next, in the order things arrived?" | A queue | First in, first out, with room to decide what happens when it's full | [Queues](queues.md) |
| "Undo the last thing", or "where was I before this?" | A stack | Last in, first out, which is how nesting and backtracking work | [Power and predictability](power-and-predictability.md) |
| "What's connected to what?" | A graph | Things and the links between them, and questions like "can I get from here to there?" | [Graphs](graphs.md) |
| "Which state is this in, and what can it do next?" | A state machine | A fixed set of states and allowed moves, so impossible ones can't happen | [State machines](state-machines.md) |
| "Have I possibly seen this before?", in a huge set | A Bloom filter | A tiny summary that's certain about "no" | [Bloom filters](bloom-filters.md) |
| "Has anything changed, and where?" | A Merkle tree or DAG | Names built from contents, so one value at the top vouches for everything below | [Merkle DAGs](merkle-dags.md) |
| "Walk them all, in order, fast" | An array | Items side by side in memory, which is what memory is fastest at | [Arrays and linked lists](arrays-and-linked-lists.md) |
| "Keep up with a flood of writes" | A log-structured merge tree | Writes go in order to the end; sorting and merging happen later | [LSM trees](lsm-trees.md) |

## Then ask four more questions

The question above picks a family. These pick between its members, and they're where most real mistakes happen.

1. **How big will it get?** Something that's fine for a thousand items can be hopeless for a million, and the difference is the *shape* of the cost, not its speed ([growth](growth.md)).
2. **How often is it written, compared with read?** Structures that make reads cheap usually make writes dearer, and the reverse ([access patterns](../data/access-patterns.md), [LSM trees](lsm-trees.md)).
3. **Where does it live?** In memory, on one disk, or across a network, the cost of a step changes by factors of thousands, and the best structure changes with it ([B-trees](b-trees.md), [latency numbers](../latency/latency-numbers.md)).
4. **What's the worst moment, and who's waiting for it?** An excellent average can hide an occasional disaster, and an attacker can choose the input that causes it ([amortised cost](amortised-cost.md), [hashing](hashing.md)).

## And for computing an answer

Structures hold data; these are the main ways of working out an answer from it.

| If the problem… | Try | Read |
| --- | --- | --- |
| Splits into smaller, separate problems of the same kind | Divide and conquer | [Divide and conquer](divide-and-conquer.md) |
| Splits into smaller problems that keep recurring | Dynamic programming: solve each once and remember it | [Dynamic programming](dynamic-programming.md) |
| Lets the best step now never block a better one later | A greedy algorithm | [Greedy algorithms](greedy.md) |
| Has no fast exact method at all | A greedy start, then improvements, or an approximation | [Greedy algorithms](greedy.md), [computability](computability.md) |

## And remember

- **Your language already has most of these,** tuned and tested for decades. The skill is choosing between them, not writing them.
- **Real systems combine them.** A database is a B-tree or an LSM tree, with hash tables, Bloom filters, heaps and queues inside it.
- **The question changes.** The structure that fitted the first question can be wrong for the next one, as Walter found when someone asked about hospitals ([page 4](../04-data-outlives-programs.md)).

## Resources

1. Steven Skiena, *The Algorithm Design Manual* (start here: the second half is a catalogue of problems and which structures and algorithms fit them).
2. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th edition, with free lectures and code from the book's site (go deeper).
3. [VisuAlgo](https://visualgo.net/en) (reference: animations of most of the structures above). <!-- verify -->
