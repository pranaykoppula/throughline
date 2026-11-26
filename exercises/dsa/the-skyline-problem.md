# The city's outline

An exercise in the category **the most urgent next**. It's LeetCode 218, [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/), rated Hard.

## The situation

A city's planning office checks every proposal for a new tower against the protected view from the harbour. Its software keeps each building along the waterfront as a rectangle, a left edge, a right edge and a height, and draws the outline the buildings make against the sky. An officer then adds the proposed tower and sees whether it breaks the line. The waterfront has thousands of buildings, many overlapping when seen from the water, and the outline needs to be redrawn instantly every time a proposal changes.

## The problem

You're given buildings as `[left, right, height]` rectangles standing on flat ground, sorted by their left edge. Return the outline they make together, as a list of key points `[x, height]`: each point is where the outline's height changes to a new value, and the last point always returns to height 0. Consecutive points must have different heights.

For buildings `[2,9,10] [3,7,15] [5,12,12] [15,20,10] [19,24,8]`, the outline is `[2,10] [3,15] [7,12] [12,0] [15,10] [20,8] [24,0]`.

## The question it asks

"Which building is tallest here, now?", asked at every place the outline might change. That's a question about the most urgent item in a changing set, which is what a [heap](../../dsa/heaps.md) answers. See the row for the most urgent next in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

The outline can only change at a building's edge. So for each edge, look through every building, find the tallest one covering that point, and record a key point if the height changed. It's correct and easy to reason about. It also checks every building at every edge, so the work grows with the square of the number of buildings ([growth](../../dsa/growth.md)): for 10,000 buildings, about 200 million checks for every redraw.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Sweep from left to right. At any point, only the buildings that have started and not yet ended matter, and of those, only the tallest. What do you need to do when a building starts, and when it ends?

</details>

<details markdown="1"><summary>Hint 2</summary>

A max-heap of the buildings standing gives the tallest in one step. Adding a starting building is easy. Removing an ending building from the middle of a heap isn't. Do you actually need to remove it straight away?

</details>

<details markdown="1"><summary>Hint 3</summary>

An ended building only matters if it's on top of the heap, because only the top is ever read. So keep each building's right edge with it in the heap, and throw away the top while it has already ended.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

1. **Collect every edge,** left and right, sorted, without duplicates. The outline can only change at these points.
2. **Sweep the edges from left to right,** keeping a max-heap of `(height, right edge)` for the buildings that have started.
   - Push every building whose left edge is at or before the current point. The input is sorted by left edge, so a single pointer walks through them.
   - While the tallest building in the heap has a right edge at or before the current point, pop it: it has ended. Ended buildings lower down are left alone until they reach the top.
   - The outline's height here is the top of the heap, or 0 if it's empty.
   - If that height differs from the last key point's, add a key point.

Leaving ended buildings in the heap until they surface is called lazy deletion. It's the same trick as the dead timers in [heaps](../../dsa/heaps.md), and it works because nobody ever asks about anything but the top.

**Why the edges are tricky:** a building's right edge is not part of it (`left ≤ x < right`), so at a building's right edge it must already be gone. Two buildings meeting at the same height must produce one key point, not two, which the "only if the height changed" check handles.

**Why it's fast:** each building is pushed once and popped at most once, and each push and pop takes time in proportion to log *n*.

**Time:** proportional to *n* log *n*. **Memory:** proportional to *n*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
import heapq
from typing import List


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # Every place the outline can change: a building's left or right edge.
        edges = sorted({x for left, right, _ in buildings for x in (left, right)})
        skyline = []
        standing = []   # (-height, right edge) of buildings that have started; tallest on top
        i, n = 0, len(buildings)
        for x in edges:
            # Buildings that start here join the heap (the input is sorted by left edge).
            while i < n and buildings[i][0] <= x:
                left, right, height = buildings[i]
                heapq.heappush(standing, (-height, right))
                i += 1
            # The tallest might have ended already; drop it only when it's on top.
            while standing and standing[0][1] <= x:
                heapq.heappop(standing)
            height = -standing[0][0] if standing else 0
            if not skyline or skyline[-1][1] != height:
                skyline.append([x, height])
        return skyline
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    vector<vector<int>> getSkyline(vector<vector<int>>& buildings) {
        // Every place the outline can change: a building's left or right edge.
        vector<int> edges;
        for (auto& b : buildings) {
            edges.push_back(b[0]);
            edges.push_back(b[1]);
        }
        sort(edges.begin(), edges.end());
        edges.erase(unique(edges.begin(), edges.end()), edges.end());

        vector<vector<int>> skyline;
        priority_queue<pair<int, int>> standing;  // (height, right edge); tallest on top
        size_t i = 0;
        for (int x : edges) {
            // Buildings that start here join the heap (the input is sorted by left edge).
            while (i < buildings.size() && buildings[i][0] <= x) {
                standing.push({buildings[i][2], buildings[i][1]});
                i++;
            }
            // The tallest might have ended already; drop it only when it's on top.
            while (!standing.empty() && standing.top().second <= x) {
                standing.pop();
            }
            int height = standing.empty() ? 0 : standing.top().first;
            if (skyline.empty() || skyline.back()[1] != height) {
                skyline.push_back({x, height});
            }
        }
        return skyline;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.TreeSet;

class Solution {
    public List<List<Integer>> getSkyline(int[][] buildings) {
        // Every place the outline can change: a building's left or right edge.
        TreeSet<Integer> edges = new TreeSet<>();
        for (int[] b : buildings) {
            edges.add(b[0]);
            edges.add(b[1]);
        }
        List<List<Integer>> skyline = new ArrayList<>();
        // {height, right edge} of buildings that have started; tallest on top.
        PriorityQueue<int[]> standing = new PriorityQueue<>((p, q) -> Integer.compare(q[0], p[0]));
        int i = 0;
        for (int x : edges) {
            // Buildings that start here join the heap (the input is sorted by left edge).
            while (i < buildings.length && buildings[i][0] <= x) {
                standing.add(new int[] {buildings[i][2], buildings[i][1]});
                i++;
            }
            // The tallest might have ended already; drop it only when it's on top.
            while (!standing.isEmpty() && standing.peek()[1] <= x) {
                standing.poll();
            }
            int height = standing.isEmpty() ? 0 : standing.peek()[0];
            if (skyline.isEmpty() || skyline.get(skyline.size() - 1).get(1) != height) {
                skyline.add(List.of(x, height));
            }
        }
        return skyline;
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

// Buildings that have started: {height, right edge}, tallest on top.
type standingHeap [][2]int

func (h standingHeap) Len() int           { return len(h) }
func (h standingHeap) Less(i, j int) bool { return h[i][0] > h[j][0] }
func (h standingHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *standingHeap) Push(x any)        { *h = append(*h, x.([2]int)) }
func (h *standingHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func getSkyline(buildings [][]int) [][]int {
	// Every place the outline can change: a building's left or right edge.
	seen := map[int]bool{}
	edges := []int{}
	for _, b := range buildings {
		for _, x := range []int{b[0], b[1]} {
			if !seen[x] {
				seen[x] = true
				edges = append(edges, x)
			}
		}
	}
	sort.Ints(edges)

	skyline := [][]int{}
	standing := &standingHeap{}
	i := 0
	for _, x := range edges {
		// Buildings that start here join the heap (the input is sorted by left edge).
		for i < len(buildings) && buildings[i][0] <= x {
			heap.Push(standing, [2]int{buildings[i][2], buildings[i][1]})
			i++
		}
		// The tallest might have ended already; drop it only when it's on top.
		for standing.Len() > 0 && (*standing)[0][1] <= x {
			heap.Pop(standing)
		}
		height := 0
		if standing.Len() > 0 {
			height = (*standing)[0][0]
		}
		if len(skyline) == 0 || skyline[len(skyline)-1][1] != height {
			skyline = append(skyline, []int{x, height})
		}
	}
	return skyline
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
use std::collections::BinaryHeap;

impl Solution {
    pub fn get_skyline(buildings: Vec<Vec<i32>>) -> Vec<Vec<i32>> {
        // Every place the outline can change: a building's left or right edge.
        let mut edges: Vec<i32> = buildings.iter().flat_map(|b| [b[0], b[1]]).collect();
        edges.sort_unstable();
        edges.dedup();

        let mut skyline: Vec<Vec<i32>> = Vec::new();
        // (height, right edge) of buildings that have started; tallest on top.
        let mut standing: BinaryHeap<(i32, i32)> = BinaryHeap::new();
        let mut i = 0;
        for x in edges {
            // Buildings that start here join the heap (the input is sorted by left edge).
            while i < buildings.len() && buildings[i][0] <= x {
                standing.push((buildings[i][2], buildings[i][1]));
                i += 1;
            }
            // The tallest might have ended already; drop it only when it's on top.
            while let Some(&(_, right)) = standing.peek() {
                if right <= x {
                    standing.pop();
                } else {
                    break;
                }
            }
            let height = standing.peek().map_or(0, |&(h, _)| h);
            if skyline.last().map_or(true, |p| p[1] != height) {
                skyline.push(vec![x, height]);
            }
        }
        skyline
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Treating the right edge as inside the building.** At `x = right`, the building has ended; pop when `right ≤ x`.
- **Emitting a point at every edge.** Only emit when the height changes, or adjacent buildings of equal height produce duplicate points.
- **Removing ended buildings eagerly.** Searching the heap for them is slow and unnecessary; drop them when they reach the top.
- **Processing starts and ends in the wrong order at the same x.** Add the buildings starting at *x* first, then drop the ones that ended, then read the height.

## Related

- The other exercise in this category: [the waiting-room screen](find-median-from-data-stream.md) (LeetCode 295).
- Concept pages: [heaps and priority queues](../../dsa/heaps.md), [sorting](../../dsa/sorting.md), [growth](../../dsa/growth.md).
- More practice of the same shape: "sweep line" problems, such as finding the most rooms needed for a list of meetings.
