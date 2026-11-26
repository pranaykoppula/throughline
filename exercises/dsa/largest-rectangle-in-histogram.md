# The biggest banner

An exercise in the category **nesting and undo**. It's LeetCode 84, [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/), rated Hard.

## The situation

A festival wants to hang one rectangular banner along a street of terraced shops, each shop front the same width but a different height. The banner can run across any number of neighbouring shop fronts, but it can't rise above the shortest of them, or it would hang over a roof. The organisers want the biggest banner the street can take. Their designer has the heights of every shop front along a street of several thousand, and wants an answer while the meeting is still going.

## The problem

You're given a list of bar heights, each bar one unit wide, standing side by side. Find the area of the largest rectangle that fits entirely within the bars.

For heights `2 1 5 6 2 3`, the largest rectangle spans the bars of height 5 and 6 at height 5, with an area of 10.

## The question it asks

"Where did the bar that's now blocked begin?" Each bar's rectangle stretches left and right until it meets a shorter bar, and bars that are waiting for their right side to be found pile up like nested brackets, last one in, first one out. That's a stack, the structure behind nesting and undo. See the row for nesting and undo in [choosing a data structure](../../dsa/choosing.md), and the stack that [power and predictability](../../dsa/power-and-predictability.md) describes as the step above a fixed-memory machine.

## The tempting first answer

For every pair of start and end bars, find the shortest bar between them and compute the area. It's three nested loops and grows with the cube of the street's length. Keeping a running minimum as the end moves brings it down to the square ([growth](../../dsa/growth.md)), which is still about 25 million steps for 5,000 shops.

A cleverer idea is [divide and conquer](../../dsa/divide-and-conquer.md): the largest rectangle either uses the shortest bar, spanning everything, or lies entirely to its left or entirely to its right. That's elegant and usually fast, but on bars that only rise, every split is lopsided, and it degrades to the square again, like quicksort on sorted data.

## Hints

<details markdown="1"><summary>Hint 1</summary>

The best rectangle has the height of some bar, and stretches from that bar as far left and right as it can before meeting a shorter bar. So for each bar, you need to know where the first shorter bar is on each side.

</details>

<details markdown="1"><summary>Hint 2</summary>

Walk the bars left to right. While the bars keep getting taller, none of them knows yet where it ends on the right. When a shorter bar arrives, which of the waiting bars has just learned its right edge?

</details>

<details markdown="1"><summary>Hint 3</summary>

Keep the waiting bars in a stack, heights increasing from bottom to top. When a bar is popped, the bar below it in the stack is the first shorter bar to its left. Why?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Walk the bars from left to right, keeping a stack of positions whose heights increase from bottom to top. These are the bars still waiting to find their right edge. Add an imaginary bar of height 0 at the end, so every real bar finds one.

For each bar *i*:

1. **While the bar on top of the stack is at least as tall as bar *i*, pop it.** Bar *i* is the first shorter (or equal) bar to its right, so its rectangle ends just before *i*. Its left edge is just after the bar now on top of the stack, which is the nearest bar to its left that's shorter, because anything taller between them was popped earlier. Compute its area: height × (*i* − left edge), and keep the best.
2. **Push *i*.**

When the walk ends, every bar has been popped once, and its rectangle measured.

**Why the stack holds the answer:** the stack is always the bars that haven't yet met anything shorter, which is exactly the set whose right edge is still unknown. It works like matching brackets: a short bar closes every taller bar opened since the last shorter one.

**Why it's fast:** each bar is pushed once and popped once, so the walk is linear, though one step can pop many bars ([amortised cost](../../dsa/amortised-cost.md)).

**Time:** proportional to *n*. **Memory:** proportional to *n*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        best = 0
        # Positions of bars still waiting to learn how far right they reach,
        # with heights increasing from bottom to top.
        stack = []
        for i, h in enumerate(heights + [0]):    # a zero at the end settles every bar
            # A shorter bar ends every taller bar still waiting.
            while stack and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                # It stretched left to just after the bar now below it in the stack.
                left = stack[-1] + 1 if stack else 0
                best = max(best, height * (i - left))
            stack.append(i)
        return best
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size(), best = 0;
        // Positions of bars still waiting to learn how far right they reach,
        // with heights increasing from bottom to top.
        vector<int> stack;
        for (int i = 0; i <= n; i++) {
            int h = i < n ? heights[i] : 0;  // a zero at the end settles every bar
            // A shorter bar ends every taller bar still waiting.
            while (!stack.empty() && heights[stack.back()] >= h) {
                int height = heights[stack.back()];
                stack.pop_back();
                // It stretched left to just after the bar now below it in the stack.
                int left = stack.empty() ? 0 : stack.back() + 1;
                best = max(best, height * (i - left));
            }
            stack.push_back(i);
        }
        return best;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length, best = 0;
        // Positions of bars still waiting to learn how far right they reach,
        // with heights increasing from bottom to top.
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i <= n; i++) {
            int h = i < n ? heights[i] : 0;  // a zero at the end settles every bar
            // A shorter bar ends every taller bar still waiting.
            while (!stack.isEmpty() && heights[stack.peek()] >= h) {
                int height = heights[stack.pop()];
                // It stretched left to just after the bar now below it in the stack.
                int left = stack.isEmpty() ? 0 : stack.peek() + 1;
                best = Math.max(best, height * (i - left));
            }
            stack.push(i);
        }
        return best;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func largestRectangleArea(heights []int) int {
	n, best := len(heights), 0
	// Positions of bars still waiting to learn how far right they reach,
	// with heights increasing from bottom to top.
	stack := []int{}
	for i := 0; i <= n; i++ {
		h := 0 // a zero at the end settles every bar
		if i < n {
			h = heights[i]
		}
		// A shorter bar ends every taller bar still waiting.
		for len(stack) > 0 && heights[stack[len(stack)-1]] >= h {
			height := heights[stack[len(stack)-1]]
			stack = stack[:len(stack)-1]
			// It stretched left to just after the bar now below it in the stack.
			left := 0
			if len(stack) > 0 {
				left = stack[len(stack)-1] + 1
			}
			best = max(best, height*(i-left))
		}
		stack = append(stack, i)
	}
	return best
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn largest_rectangle_area(heights: Vec<i32>) -> i32 {
        let n = heights.len();
        let mut best = 0;
        // Positions of bars still waiting to learn how far right they reach,
        // with heights increasing from bottom to top.
        let mut stack: Vec<usize> = Vec::new();
        for i in 0..=n {
            let h = if i < n { heights[i] } else { 0 }; // a zero at the end settles every bar
            // A shorter bar ends every taller bar still waiting.
            while let Some(&top) = stack.last() {
                if heights[top] < h {
                    break;
                }
                stack.pop();
                // It stretched left to just after the bar now below it in the stack.
                let left = stack.last().map_or(0, |&below| below + 1);
                best = best.max(heights[top] * (i - left) as i32);
            }
            stack.push(i);
        }
        best
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Forgetting the bars left on the stack at the end.** The zero-height bar at the end flushes them; without it, rising streets lose their best answer.
- **Using the popped bar's own position as the left edge.** The rectangle extends left past every taller bar popped before it, to just after the bar below it in the stack.
- **Handling equal heights inconsistently.** Popping on "at least as tall" or on "taller" both work, as long as the left edge comes from the stack and not from the popped position.
- **Overflow in other variants.** Here the largest area fits in 32 bits, but with wider bars or taller heights, use 64-bit areas.

## Related

- The other exercise in this category: [the formula box](basic-calculator.md) (LeetCode 224).
- Concept pages: [power and predictability](../../dsa/power-and-predictability.md), [divide and conquer](../../dsa/divide-and-conquer.md), [amortised cost](../../dsa/amortised-cost.md), [growth](../../dsa/growth.md).
- More practice of the same shape: problems tagged "monotonic stack", such as the largest rectangle of ones in a grid.
