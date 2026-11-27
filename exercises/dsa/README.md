# Algorithm and data structure exercises

Twenty-four LeetCode Hard problems, two for each kind of question. The categories follow [choosing a data structure](../../dsa/choosing.md): recognising which question a problem is asking is most of the skill, so they're grouped that way, not by data structure.

| The question it asks | Exercises | Concept pages |
| --- | --- | --- |
| Find by key | [The first free locker](first-missing-positive.md) (41); [The shortest crash signature](minimum-window-substring.md) (76) | [hash tables](../../dsa/hash-tables.md), [hashing](../../dsa/hashing.md) |
| Order and halving | [Two depots, one median](median-of-two-sorted-arrays.md) (4); [Splitting the translation](split-array-largest-sum.md) (410) | [sorting](../../dsa/sorting.md), [divide and conquer](../../dsa/divide-and-conquer.md) |
| The most urgent next | [The waiting-room screen](find-median-from-data-stream.md) (295); [The city's outline](the-skyline-problem.md) (218) | [heaps](../../dsa/heaps.md) |
| Next in line, over a window | [The busiest five minutes](sliding-window-maximum.md) (239); [The shortest good run](shortest-subarray-with-sum-at-least-k.md) (862) | [queues](../../dsa/queues.md), [amortised cost](../../dsa/amortised-cost.md) |
| Nesting and undo | [The biggest banner](largest-rectangle-in-histogram.md) (84); [The formula box](basic-calculator.md) (224) | [power and predictability](../../dsa/power-and-predictability.md) |
| What connects to what | [The rescue boat's first chance](swim-in-rising-water.md) (778); [The cable you can't lose](critical-connections-in-a-network.md) (1192) | [graphs](../../dsa/graphs.md), [greedy algorithms](../../dsa/greedy.md) |
| Which state, what next | [The price column](valid-number.md) (65); [The rule that took the afternoon](regular-expression-matching.md) (10) | [state machines](../../dsa/state-machines.md), [power and predictability](../../dsa/power-and-predictability.md) |
| Everything with this prefix | [The letter grid](word-search-ii.md) (212); [The shop's search box](prefix-and-suffix-search.md) (745) | [tries](../../dsa/tries.md) |
| Split, solve, combine | [The readings that came after](count-of-smaller-numbers-after-self.md) (315); [The price that more than halved](reverse-pairs.md) (493) | [divide and conquer](../../dsa/divide-and-conquer.md), [sorting](../../dsa/sorting.md) |
| Overlapping questions | [The last balloon](burst-balloons.md) (312); [The marker in the sequence](distinct-subsequences.md) (115) | [dynamic programming](../../dsa/dynamic-programming.md) |
| The best step now | [The stickers on the chart](candy.md) (135); [The training year](course-schedule-iii.md) (630) | [greedy algorithms](../../dsa/greedy.md), [heaps](../../dsa/heaps.md) |
| Build a structure for the pattern | [The least-asked question](lfu-cache.md) (460); [The leaderboard's ends](all-oone-data-structure.md) (432) | [choosing a data structure](../../dsa/choosing.md), [hash tables](../../dsa/hash-tables.md) |

Numbers are LeetCode's. All twenty-four were checked as Hard and free to view on 2026-11-26; LeetCode sometimes re-rates problems.

## How the code works

Each exercise's code lives in `code/<exercise>/`: one solution per language, a small driver per language that reads a test and prints the answer, and `tests.json`. `scripts/make_exercises.py` copies the solutions into the page, and `scripts/test_exercises.py` runs every solution against every test. The signatures match LeetCode's, so a solution can be pasted there as it is.
