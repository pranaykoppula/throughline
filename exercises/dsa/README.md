# Algorithm and data structure exercises

Twenty-four LeetCode Hard problems, two for each kind of question. The categories follow [choosing a data structure](../../dsa/choosing.md): recognising which question a problem is asking is most of the skill, so they're grouped that way, not by data structure.

| The question it asks | Exercises | Concept pages |
| --- | --- | --- |
| Find by key | First Missing Positive (41); Minimum Window Substring (76) | [hash tables](../../dsa/hash-tables.md), [hashing](../../dsa/hashing.md) |
| Order and halving | Median of Two Sorted Arrays (4); Split Array Largest Sum (410) | [sorting](../../dsa/sorting.md), [divide and conquer](../../dsa/divide-and-conquer.md) |
| The most urgent next | Find Median from Data Stream (295); The Skyline Problem (218) | [heaps](../../dsa/heaps.md) |
| Next in line, over a window | [The busiest five minutes](sliding-window-maximum.md) (239); Shortest Subarray with Sum at Least K (862) | [queues](../../dsa/queues.md), [amortised cost](../../dsa/amortised-cost.md) |
| Nesting and undo | Largest Rectangle in Histogram (84); Basic Calculator (224) | [power and predictability](../../dsa/power-and-predictability.md) |
| What connects to what | Swim in Rising Water (778); Critical Connections in a Network (1192) | [graphs](../../dsa/graphs.md), [greedy algorithms](../../dsa/greedy.md) |
| Which state, what next | Valid Number (65); Regular Expression Matching (10) | [state machines](../../dsa/state-machines.md), [power and predictability](../../dsa/power-and-predictability.md) |
| Everything with this prefix | Word Search II (212); Prefix and Suffix Search (745) | [tries](../../dsa/tries.md) |
| Split, solve, combine | Count of Smaller Numbers After Self (315); Reverse Pairs (493) | [divide and conquer](../../dsa/divide-and-conquer.md), [sorting](../../dsa/sorting.md) |
| Overlapping questions | Burst Balloons (312); Distinct Subsequences (115) | [dynamic programming](../../dsa/dynamic-programming.md) |
| The best step now | Candy (135); Course Schedule III (630) | [greedy algorithms](../../dsa/greedy.md), [heaps](../../dsa/heaps.md) |
| Build a structure for the pattern | LFU Cache (460); All O`one Data Structure (432) | [choosing a data structure](../../dsa/choosing.md), [hash tables](../../dsa/hash-tables.md) |

Numbers are LeetCode's. All twenty-four were checked as Hard and free to view on 2026-11-26; LeetCode sometimes re-rates problems. Exercises without a link are still to be written.

## How the code works

Each exercise's code lives in `code/<exercise>/`: one solution per language, a small driver per language that reads a test and prints the answer, and `tests.json`. `scripts/make_exercises.py` copies the solutions into the page, and `scripts/test_exercises.py` runs every solution against every test. The signatures match LeetCode's, so a solution can be pasted there as it is.
