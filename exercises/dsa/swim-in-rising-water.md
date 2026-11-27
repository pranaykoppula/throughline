# The rescue boat's first chance

An exercise in the category **what connects to what**. It's LeetCode 778, [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/), rated Hard.

## The situation

A river has burst its banks and is flooding a valley. The emergency service has a survey of the valley as a grid of squares, each with its ground height in metres, and the water is rising steadily across all of it. A flat-bottomed rescue boat waits at the depot in one corner, and a farm in the opposite corner has people stranded on its roof. The boat can move between neighbouring squares, but only across squares the water already covers. The controllers want to know the lowest water level at which the boat can reach the farm, so they know how soon to launch.

## The problem

You're given an *n* × *n* grid of distinct whole numbers, the heights of each square. At time *t* the water is at level *t* everywhere, and you can move up, down, left or right between squares whose heights are both at most *t*, instantly. Return the earliest time at which you can get from the top-left square to the bottom-right square.

For the grid

```
0 2
1 3
```

the answer is 3: the bottom-right square itself has height 3, so nothing can happen before the water reaches it.

## The question it asks

"Which squares can I reach, and what does it cost to reach them?" That's a question about what connects to what, so the grid is a [graph](../../dsa/graphs.md): squares are nodes, and neighbours are joined by edges. The twist is that a route's cost isn't the sum of its steps but its single highest square. See the row for what connects to what in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Try every water level from 0 upwards, and for each one, walk the grid from the depot to see whether the farm is reachable. The first level that works is the answer. It's correct and easy to trust. But there are *n*² levels and each walk visits up to *n*² squares, so the work grows with *n*⁴ ([growth](../../dsa/growth.md)): for a 50 × 50 survey, about 6 million steps, and real surveys are far bigger.

The fix most people see first is to halve the levels instead of trying each one: if the boat can get through at level *L*, it can at any higher level, so [binary search](../../dsa/divide-and-conquer.md) over the level needs only about log(*n*²) walks. That's a good answer. There's a neater one that needs a single walk.

## Hints

<details markdown="1"><summary>Hint 1</summary>

The cost of a route is the height of its highest square. You want the route whose highest square is as low as possible. How is that like finding the shortest route, and how is it different?

</details>

<details markdown="1"><summary>Hint 2</summary>

Dijkstra's algorithm always extends the cheapest route found so far. What would "cheapest" mean if a route's cost were its highest point rather than its length?

</details>

<details markdown="1"><summary>Hint 3</summary>

Keep the squares on the edge of the area you've reached in a min-heap, keyed by the water level needed to reach them. Always take the lowest one next. When you take the farm, the level you reached it at is the answer.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Grow the area the boat can reach, one square at a time, always taking the square that needs the least water.

1. **Start** with a min-heap holding the depot, keyed by its own height, and mark it as seen.
2. **Pop the lowest square.** Its key is the water level needed to reach it from the depot by the best route. If it's the farm, return that level.
3. **Push each unseen neighbour,** keyed by the higher of the current level and the neighbour's own height, since getting there needs both. Mark it as seen.

**Why the first time you pop the farm is the answer:** squares come out of the heap in order of the level needed to reach them, and that level can never go down along a route. So when the farm comes out, no route needs less water, because any such route would have had to pass through a square still in the heap with a lower key. It's [Dijkstra's algorithm](../../dsa/graphs.md) with "add the step" replaced by "take the higher", and the same [greedy](../../dsa/greedy.md) argument proves it.

**Another way to see it:** sort the squares by height and add them to the map one by one, joining each to its flooded neighbours, until the depot and the farm are in the same group. A union-find structure keeps track of the groups. It does the same work in a different order.

**Time:** proportional to *n*² log *n*. **Memory:** proportional to *n*².

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # Squares we can reach, by the water level needed to reach them; lowest first.
        frontier = [(grid[0][0], 0, 0)]
        seen = {(0, 0)}
        while frontier:
            level, r, c = heapq.heappop(frontier)
            if (r, c) == (n - 1, n - 1):
                return level
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    # Reaching the neighbour needs the higher of the two levels.
                    heapq.heappush(frontier, (max(level, grid[nr][nc]), nr, nc))
        return -1
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        // Squares we can reach, by the water level needed to reach them; lowest first.
        priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>, greater<>> frontier;
        vector<vector<bool>> seen(n, vector<bool>(n, false));
        frontier.push({grid[0][0], 0, 0});
        seen[0][0] = true;
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!frontier.empty()) {
            auto [level, r, c] = frontier.top();
            frontier.pop();
            if (r == n - 1 && c == n - 1) return level;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc]) {
                    seen[nr][nc] = true;
                    // Reaching the neighbour needs the higher of the two levels.
                    frontier.push({max(level, grid[nr][nc]), nr, nc});
                }
            }
        }
        return -1;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.PriorityQueue;

class Solution {
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        // Squares we can reach, by the water level needed to reach them; lowest first.
        PriorityQueue<int[]> frontier = new PriorityQueue<>((p, q) -> Integer.compare(p[0], q[0]));
        boolean[][] seen = new boolean[n][n];
        frontier.add(new int[] {grid[0][0], 0, 0});
        seen[0][0] = true;
        int[][] steps = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!frontier.isEmpty()) {
            int[] top = frontier.poll();
            int level = top[0], r = top[1], c = top[2];
            if (r == n - 1 && c == n - 1) return level;
            for (int[] s : steps) {
                int nr = r + s[0], nc = c + s[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc]) {
                    seen[nr][nc] = true;
                    // Reaching the neighbour needs the higher of the two levels.
                    frontier.add(new int[] {Math.max(level, grid[nr][nc]), nr, nc});
                }
            }
        }
        return -1;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
import "container/heap"

// Squares we can reach: {level needed, row, column}, lowest level on top.
type cellHeap [][3]int

func (h cellHeap) Len() int           { return len(h) }
func (h cellHeap) Less(i, j int) bool { return h[i][0] < h[j][0] }
func (h cellHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *cellHeap) Push(x any)        { *h = append(*h, x.([3]int)) }
func (h *cellHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func swimInWater(grid [][]int) int {
	n := len(grid)
	seen := make([][]bool, n)
	for i := range seen {
		seen[i] = make([]bool, n)
	}
	frontier := &cellHeap{{grid[0][0], 0, 0}}
	seen[0][0] = true
	steps := [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for frontier.Len() > 0 {
		top := heap.Pop(frontier).([3]int)
		level, r, c := top[0], top[1], top[2]
		if r == n-1 && c == n-1 {
			return level
		}
		for _, s := range steps {
			nr, nc := r+s[0], c+s[1]
			if nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc] {
				seen[nr][nc] = true
				// Reaching the neighbour needs the higher of the two levels.
				heap.Push(frontier, [3]int{max(level, grid[nr][nc]), nr, nc})
			}
		}
	}
	return -1
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
use std::cmp::Reverse;
use std::collections::BinaryHeap;

impl Solution {
    pub fn swim_in_water(grid: Vec<Vec<i32>>) -> i32 {
        let n = grid.len();
        // Squares we can reach, by the water level needed to reach them; lowest first.
        let mut frontier = BinaryHeap::new();
        let mut seen = vec![vec![false; n]; n];
        frontier.push(Reverse((grid[0][0], 0usize, 0usize)));
        seen[0][0] = true;
        let steps: [(i32, i32); 4] = [(1, 0), (-1, 0), (0, 1), (0, -1)];
        while let Some(Reverse((level, r, c))) = frontier.pop() {
            if r == n - 1 && c == n - 1 {
                return level;
            }
            for (dr, dc) in steps {
                let (nr, nc) = (r as i32 + dr, c as i32 + dc);
                if nr < 0 || nc < 0 || nr >= n as i32 || nc >= n as i32 {
                    continue;
                }
                let (nr, nc) = (nr as usize, nc as usize);
                if !seen[nr][nc] {
                    seen[nr][nc] = true;
                    // Reaching the neighbour needs the higher of the two levels.
                    frontier.push(Reverse((level.max(grid[nr][nc]), nr, nc)));
                }
            }
        }
        -1
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Forgetting the depot's own height.** The boat can't start until its own square is covered, so the first key is `grid[0][0]`, not 0.
- **Adding heights along the route.** The cost of a route is its highest square, not the total; take the maximum.
- **Worrying that marking a square on push is too early.** In ordinary Dijkstra a node's distance can still improve after it's first pushed. Here it can't: squares are popped in order of level, so the first square to discover a neighbour has the lowest level of any that will, and the neighbour's key, the higher of that level and its own height, is already the best it can get.
- **Moving diagonally.** Only up, down, left and right.

## Related

- The other exercise in this category: [the cable you can't lose](critical-connections-in-a-network.md) (LeetCode 1192).
- Concept pages: [graphs](../../dsa/graphs.md), [heaps and priority queues](../../dsa/heaps.md), [greedy algorithms](../../dsa/greedy.md), [divide and conquer](../../dsa/divide-and-conquer.md).
- More practice of the same shape: problems tagged "minimax path" or "bottleneck path", such as the path with the least effort across a height map.
