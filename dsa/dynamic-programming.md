# Dynamic programming

Last reviewed: 2026-11-12

A concept page: when a problem breaks into smaller problems that keep recurring, solve each one once, write the answer down, and build the big answer from the table. It's how `diff` compares files, how route planners find the cheapest path, and how a recursive solution that would take longer than the universe's age can finish in a second.

## Problem

Some problems have a natural recursive description: the best answer for the whole is built from the best answers for slightly smaller versions. Written directly, that description is short, clear and correct. It can also be catastrophically slow, because the same smaller problems come up again and again along different paths, and the program solves each one from scratch every time. The work grows exponentially, and nothing about the code looks wrong.

## The story

In 1996 Imelda Cruz worked in the technology team of a law firm in Manila. Lawyers sent each other drafts of contracts, and every round came back with changes, some marked and some not. The partners wanted a tool that would compare two versions and show every line added or removed. Imelda thought about what the best comparison meant: the longest run of lines the two versions had in common, in order. Everything else was a change.

She wrote it the way the definition read. Compare the last line of each version. If they're the same, it's part of the common run; compare everything before them. If they're different, try two possibilities, dropping the last line of the first version or the last line of the second, compare what's left in each case, and keep whichever is better. The program was a dozen lines long and obviously correct. On her test files, twenty lines each, it answered instantly.

The first real contract had two hundred lines. The program ran for a minute, then ten, and Imelda stopped it. She added a counter and ran it on files of thirty lines: millions of comparisons. Forty lines: hundreds of millions. Every extra pair of lines different between the two versions roughly doubled the work, because each mismatch split into two possibilities, and each of those split again.

She printed out the calls for a tiny example and saw why. The same question, "how long is the common run of the first twelve lines of A and the first nine lines of B?", was being asked over and over, reached by dozens of different routes. There were only twelve times nine such questions for those prefixes. The program was answering each of them thousands of times.

*Before reading on: the program kept answering the same few questions millions of times. What would you have changed?*

Imelda gave each question a cell in a table: one row for each prefix of version A, one column for each prefix of version B. She filled it in order, from the smallest prefixes up, so that every cell's answer was built from cells already filled: the one diagonally above if the lines matched, otherwise the better of the one above and the one to the left. Each cell took a moment. For two contracts of two thousand lines, there were four million cells, and the whole table filled in under a second. Then she traced back through the table from the bottom-right corner to read off which lines were common and which had changed.

A year later it ran out of memory. A merger agreement with all its schedules attached ran to sixty thousand lines in each version, and the table would have needed three billion cells. Imelda noticed two things. To fill any row she only ever looked at the row before it, so she could keep two rows instead of the whole table, if she found another way to recover the changes. And the two versions were nearly identical, with a few hundred changed lines in sixty thousand. The best path through the table ran close to its diagonal the whole way. She read about a newer comparison method that explored outwards from the diagonal and stopped as soon as it reached the corner, so its work grew with the number of *differences*, not with the size of the files. The merger agreement compared in two seconds.

Looking back, Imelda thought the recursion had been right about the problem and wrong about the work. The problem really was made of smaller versions of itself. They just weren't separate, like the halves of a sorted list. They overlapped, so the cure was to remember. And once remembering worked, the next step was to notice which parts of the table nobody would ever need.

![A table comparing two short words letter by letter, one along the top and one down the side. Each cell holds the length of the longest common run of letters for those two prefixes. A highlighted path runs from the bottom-right corner back to the top-left, marking the letters the two words share.](../images/figures/dsa-dynamic-programming.svg)

*Imelda's table, for two short words instead of two contracts: every cell is built from the cells above and to its left.*

## Where it shows up

| Page | The overlapping questions | What remembering them bought |
| --- | --- | --- |
| [Graphs](graphs.md) | Ruth's shortest distance to each junction | Each junction's best distance, worked out once and reused by every route through it. |
| [Caching](../latency/caching.md) | The same request, asked many times | Memoisation is caching applied to computation: remember an answer instead of recomputing it. |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | Sofia's merges, line by line | Every merge starts with a comparison like Imelda's, finding what two versions have in common. |
| [Divide and conquer](divide-and-conquer.md) | Pieces that don't overlap | The contrast: when subproblems are separate, solve them separately; when they repeat, remember. |
| [Growth](growth.md) | Imelda's first version | Exponential growth from a dozen innocent lines, cut to the size of a table. |

It shows up elsewhere too: spell checkers measuring how many edits separate two words, comparing DNA sequences, speech recognition and error-correcting decoders finding the most likely sequence, text layout choosing where to break lines, planning in games and robots, and pricing financial options.

What these share is a problem built from smaller versions of itself that overlap. Find the smaller questions, give each a place to store its answer, and fill them in an order where each answer only needs ones already found. The skill is seeing the overlap; after that, the table is mechanical.

Motif: [costs move; they don't disappear](../motifs.md#costs-move-they-dont-disappear).

## It really happened

Imelda is fictional. Richard Bellman developed dynamic programming at the RAND Corporation in the early 1950s, for problems of planning decisions over time. In his autobiography he said he chose the name partly as camouflage: the Secretary of Defense, he wrote, hated the word "research", and "dynamic programming" was a name not even a Congressman could object to. "Programming" then meant planning, not writing code. Historians have pointed out that Bellman used the term before that Secretary took office, so the story may be partly hindsight ([notes on the origins of the name](https://notes.zachmanson.com/on-the-origins-of-dynamic-programming) <!-- verify -->).

The comparison problem is the one behind `diff`, the Unix tool for comparing files, which James Hunt and Douglas McIlroy described in 1976. In 1986 Eugene Myers published the method Imelda read about, whose work grows with the number of differences, not the size of the files; versions of it are still the default in git.

## What it is

Dynamic programming applies when a problem has optimal substructure (the best answer is built from best answers to subproblems) and overlapping subproblems (the same subproblems recur). It either stores the answer to each subproblem the first time it's computed (memoisation, top-down) or fills a table of subproblems in an order where each entry depends only on entries already filled (tabulation, bottom-up). Time becomes roughly the number of distinct subproblems times the work per subproblem. Memory can often be reduced by keeping only the part of the table still needed. When subproblems don't overlap, plain divide and conquer is simpler.

## Where it gets misapplied

- **Writing the clean recursion and shipping it.** Correct, short, and exponential, like Imelda's first version.
- **Storing a table nobody needs all of.** Three billion cells for a problem that only ever looked at the last row, or at a narrow band around the diagonal.
- **Using it where a greedy choice is enough.** If the best next step never needs revisiting, a table is wasted effort ([greedy algorithms](greedy.md)).
- **The mirror:** remembering everything, everywhere. A memo that never forgets is a cache with no eviction, and it grows until memory runs out.

## Connections

- Learning this is also learning [divide and conquer](divide-and-conquer.md), because both split a problem into smaller ones; dynamic programming is for when the pieces overlap.
- Learning this is also learning [caching](../latency/caching.md), because memoisation is a cache for computation, with the same question of when to forget.
- Learning this is also learning [graphs](graphs.md), because shortest-path algorithms build each node's best distance from its neighbours'.
- Learning this is also learning [growth](growth.md), because the difference between the recursion and the table is the difference between exponential and polynomial.
- Learning this is also learning [greedy algorithms](greedy.md), because the two are the main ways to build an optimal answer step by step, and knowing which one applies is most of the skill.

## Resources

1. [VisuAlgo, recursion](https://visualgo.net/en/recursion) (start here: watch a recursion repeat itself, then watch memoisation cut it down). <!-- verify -->
2. Steven Skiena, *The Algorithm Design Manual*, the chapter on dynamic programming (go deeper: how to spot it in practice).
3. Eugene Myers, "An O(ND) Difference Algorithm and Its Variations", *Algorithmica* (1986) (reference: the diff in your version control).

## Names you'll hear

- **Overlapping subproblems, optimal substructure:** the two properties that make a problem suitable.
- **Memoisation:** storing a function's answers so repeated calls return immediately.
- **Tabulation, bottom-up:** filling a table from the smallest subproblems upwards.
- **Longest common subsequence, edit distance:** the classic comparison problems behind `diff` and spell checking.
- **Bellman equation:** the recursive definition of the best decision at each step.

## Go and look

Run `diff` or `git diff` on two versions of a file with a few changes, then on two files that are completely different. Notice how much longer the second takes: the work grows with the differences.
