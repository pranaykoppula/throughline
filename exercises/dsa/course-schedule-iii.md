# The training year

An exercise in the category **the best step now**. It's LeetCode 630, [Course Schedule III](https://leetcode.com/problems/course-schedule-iii/), rated Hard.

## The situation

A hospital's new nurses each have a year of optional training courses to fit around their shifts. Each course takes a known number of days of study, and each must be finished by a deadline, after which its certificate no longer counts towards that year's grading. A nurse can only study one course at a time. The education office wants to tell each nurse the most courses they can complete, from a catalogue of several thousand.

## The problem

You're given a list of courses, each as `[duration, last day]`. You start on day 1, take one course at a time, and each must be finished by its last day. Return the largest number of courses you can complete.

For `[100, 200]`, `[200, 1300]`, `[1000, 1250]` and `[2000, 3200]`, the answer is 3: take the first (finished on day 100), then the third (day 1,100), then the second (day 1,300). The fourth would end on day 3,300, too late.

## The question it asks

"Which course should I give up?" Taking courses in order of deadline is the obvious greedy step, and it's right. But it's not enough on its own: sometimes a course that fitted has to be dropped later, to make room for two shorter ones. The question then is which, and the answer is always the longest, which is what a [heap](../../dsa/heaps.md) gives instantly. See the row for the best step now in [choosing a data structure](../../dsa/choosing.md), and [greedy algorithms](../../dsa/greedy.md).

## The tempting first answer

Try every subset of courses, put each in deadline order, and keep the biggest subset that fits. It's correct, and with *n* courses there are 2^*n* subsets ([growth](../../dsa/growth.md)): fine for ten, hopeless for a catalogue.

A better first answer is [dynamic programming](../../dsa/dynamic-programming.md), like packing a knapsack: in deadline order, for each possible finishing day, the most courses that can end by then. It's correct, but the table has a row for every day up to the last deadline, which can be ten thousand days for each of ten thousand courses.

The quick greedy answers, "shortest courses first" or "earliest deadline first, skip anything that doesn't fit", are both wrong. The second skips a course that would fit if a longer one taken earlier were dropped.

## Hints

<details markdown="1"><summary>Hint 1</summary>

If you've chosen a set of courses, does the order you take them in matter? Which order gives the set the best chance of fitting?

</details>

<details markdown="1"><summary>Hint 2</summary>

Earliest deadline first is always the best order for a fixed set. So go through the courses by deadline, adding each one. If adding it makes you late, you have to drop something. Which course, of the ones you've taken, is the best to drop?

</details>

<details markdown="1"><summary>Hint 3</summary>

Drop the longest. The count stays the same as before adding the new course, and you finish as early as possible, leaving the most room for later courses. Keep the durations in a max-heap.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

1. **Sort the courses by last day.**
2. **Go through them in that order,** keeping a max-heap of the durations of the courses you've kept and the day they all finish.
   - Add the course: push its duration, and add it to the finishing day.
   - If the finishing day is now after this course's last day, pop the longest duration from the heap and take it off the finishing day.
3. **The answer** is the number of courses left in the heap.

**Why deadline order:** for any set of courses that can all be completed, taking them in order of deadline completes them. Swapping two courses that are out of deadline order never makes either one late. So the only question is which set to take.

**Why dropping the longest is safe:** after the drop, you have as many courses as before this one was considered, and the finishing day is as early as it can be for that many. Every course still kept has a deadline no later than the current one, and the kept courses finish no later than before. A later course can only benefit from an earlier finishing day. This is the swap argument at the heart of most [greedy](../../dsa/greedy.md) proofs: any better plan can be changed step by step into this one without getting worse.

**Time:** proportional to *n* log *n*, for the sort and the heap. **Memory:** proportional to *n*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
import heapq
from typing import List


class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        taken = []   # durations of the courses kept so far, longest on top (stored negated)
        day = 0      # the day the kept courses finish, taken one after another
        # Consider courses in order of deadline: the earliest deadline first.
        for duration, last_day in sorted(courses, key=lambda c: c[1]):
            heapq.heappush(taken, -duration)
            day += duration
            if day > last_day:
                # Too late: drop the longest course kept so far. It frees the most time,
                # and the rest still finish in time because their deadlines are earlier.
                day += heapq.heappop(taken)
        return len(taken)
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int scheduleCourse(vector<vector<int>>& courses) {
        // Consider courses in order of deadline: the earliest deadline first.
        sort(courses.begin(), courses.end(), [](auto& a, auto& b) { return a[1] < b[1]; });
        priority_queue<int> taken;  // durations of the courses kept so far, longest on top
        int day = 0;                // the day the kept courses finish, taken one after another
        for (auto& c : courses) {
            taken.push(c[0]);
            day += c[0];
            if (day > c[1]) {
                // Too late: drop the longest course kept so far. It frees the most time,
                // and the rest still finish in time because their deadlines are earlier.
                day -= taken.top();
                taken.pop();
            }
        }
        return taken.size();
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.Arrays;
import java.util.Collections;
import java.util.PriorityQueue;

class Solution {
    public int scheduleCourse(int[][] courses) {
        // Consider courses in order of deadline: the earliest deadline first.
        Arrays.sort(courses, (a, b) -> Integer.compare(a[1], b[1]));
        // Durations of the courses kept so far, longest on top.
        PriorityQueue<Integer> taken = new PriorityQueue<>(Collections.reverseOrder());
        int day = 0;  // the day the kept courses finish, taken one after another
        for (int[] c : courses) {
            taken.add(c[0]);
            day += c[0];
            if (day > c[1]) {
                // Too late: drop the longest course kept so far. It frees the most time,
                // and the rest still finish in time because their deadlines are earlier.
                day -= taken.poll();
            }
        }
        return taken.size();
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
import (
	"container/heap"
	"sort"
)

// Durations of the courses kept so far, longest on top.
type maxHeap []int

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *maxHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func scheduleCourse(courses [][]int) int {
	// Consider courses in order of deadline: the earliest deadline first.
	sort.Slice(courses, func(i, j int) bool { return courses[i][1] < courses[j][1] })
	taken := &maxHeap{}
	day := 0 // the day the kept courses finish, taken one after another
	for _, c := range courses {
		heap.Push(taken, c[0])
		day += c[0]
		if day > c[1] {
			// Too late: drop the longest course kept so far. It frees the most time,
			// and the rest still finish in time because their deadlines are earlier.
			day -= heap.Pop(taken).(int)
		}
	}
	return taken.Len()
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
use std::collections::BinaryHeap;

impl Solution {
    pub fn schedule_course(mut courses: Vec<Vec<i32>>) -> i32 {
        // Consider courses in order of deadline: the earliest deadline first.
        courses.sort_by_key(|c| c[1]);
        let mut taken = BinaryHeap::new(); // durations of the courses kept so far, longest on top
        let mut day = 0; // the day the kept courses finish, taken one after another
        for c in &courses {
            taken.push(c[0]);
            day += c[0];
            if day > c[1] {
                // Too late: drop the longest course kept so far. It frees the most time,
                // and the rest still finish in time because their deadlines are earlier.
                day -= taken.pop().unwrap();
            }
        }
        taken.len() as i32
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Skipping a course that doesn't fit.** The new course might be short; dropping a longer earlier course could make room for it. Add first, then drop the longest.
- **Sorting by duration.** Short courses with late deadlines can crowd out long courses with early ones; sort by deadline.
- **Dropping the course just added.** It's dropped only if it's the longest; otherwise drop the longest kept.
- **Forgetting that a course longer than its own deadline can never be taken.** The heap handles it: it's added, it's the longest, and it's dropped straight away.

## Related

- The other exercise in this category: [the stickers on the chart](candy.md) (LeetCode 135).
- Concept pages: [greedy algorithms](../../dsa/greedy.md), [heaps and priority queues](../../dsa/heaps.md), [sorting](../../dsa/sorting.md), [dynamic programming](../../dsa/dynamic-programming.md).
- More practice of the same shape: scheduling jobs with deadlines to meet the most of them, and the cheapest way to hire workers for a set of tasks, where a heap holds the choices you might want to undo.
