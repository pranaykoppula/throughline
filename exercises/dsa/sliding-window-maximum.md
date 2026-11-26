# The busiest five minutes

An exercise in the category **next in line, over a window**. It's LeetCode 239, [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/), rated Hard.

## The situation

A wind farm's control room watches the load on each turbine's gearbox, one reading a second. The engineers don't care about any single reading; a gust can spike one for a moment. What they want on the wall is the highest load over each rolling five-minute window, updated every second, because that's what decides whether a gearbox is being worked too hard. A day of readings is 86,400 numbers, a window is 300 of them, and the chart has to keep up as readings arrive.

## The problem

You're given a list of numbers and a window size *k*. Slide a window of *k* consecutive numbers from the start of the list to the end, one position at a time, and report the largest number in each position of the window.

For the readings `1 3 -1 -3 5 3 6 7` with a window of 3, the windows are `1 3 -1`, `3 -1 -3`, `-1 -3 5` and so on, and the answer is `3 3 5 5 6 7`.

## The question it asks

"What's next in line to matter?" Readings arrive in order and leave in the same order, like a [queue](../../dsa/queues.md), but you also need the largest of whatever is currently in the queue. See the row for the next in line in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

For each position of the window, look at all *k* readings in it and take the largest. It's obviously correct and takes three lines. It also does *k* steps for each of roughly *n* windows: for a day of readings and a five-minute window, about 26 million comparisons, and the work grows with both the data and the window ([growth](../../dsa/growth.md)). Double the window and the chart takes twice as long to draw, though nothing about the answer got harder.

The second idea is better: keep the window's readings in a [heap](../../dsa/heaps.md), so the largest is always on top. Each step adds one reading and takes the top. The catch is removing the reading that just slid out, which is somewhere in the middle of the heap. That can be done, by leaving stale entries in and throwing them away when they reach the top, and it brings the cost down to about *n* log *n*. But there's a way to do it with no logarithm at all.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Suppose a reading of 8 arrives while the window still holds an older reading of 5. Can that 5 ever be the largest in any future window?

</details>

<details markdown="1"><summary>Hint 2</summary>

It can't: the 8 is newer, so it stays in the window at least as long as the 5 does, and it's bigger. So the 5 can be forgotten the moment the 8 arrives. What's left, if you always forget readings like that?

</details>

<details markdown="1"><summary>Hint 3</summary>

What's left is a list of readings in decreasing order, oldest at the front. The front is the window's maximum. You need to add at the back, remove from the back, and remove from the front. Which structure does all three cheaply?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Keep a double-ended queue of *candidates*: positions of readings that could still be the maximum of some window, in the order they arrived, with their values decreasing from front to back.

For each new reading:

1. **Forget the readings it beats.** While the reading at the back of the queue is no larger than the new one, remove it. The new reading is bigger and will stay in the window longer, so those older ones can never be the maximum again.
2. **Add the new reading's position at the back.**
3. **Forget the front if it has left the window.** Its position is now more than *k* behind.
4. **Once the first full window is in, report the front.** Because values decrease from front to back, the front is the largest reading in the window.

Store positions, not values, so you can tell when the front has slid out.

**Why it's fast:** each reading is added to the queue once and removed at most once, so the whole run takes time in proportion to *n*, however large the window. A single step can remove many readings, but those removals are paid for by the steps that added them: the cost is [amortised](../../dsa/amortised-cost.md), constant on average per reading. The queue never holds more than *k* positions.

**Time:** proportional to *n*. **Memory:** proportional to *k*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # Indices of readings that could still be a window's maximum,
        # with their values in decreasing order from front to back.
        candidates = deque()
        result = []
        for i, x in enumerate(nums):
            # A new reading outlives every smaller one before it,
            # so those can never be the maximum again.
            while candidates and nums[candidates[-1]] <= x:
                candidates.pop()
            candidates.append(i)
            # The front has slid out of the window.
            if candidates[0] <= i - k:
                candidates.popleft()
            if i >= k - 1:
                result.append(nums[candidates[0]])
        return result
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        // Indices of readings that could still be a window's maximum,
        // with their values in decreasing order from front to back.
        deque<int> candidates;
        vector<int> result;
        for (int i = 0; i < (int)nums.size(); i++) {
            // A new reading outlives every smaller one before it.
            while (!candidates.empty() && nums[candidates.back()] <= nums[i]) {
                candidates.pop_back();
            }
            candidates.push_back(i);
            // The front has slid out of the window.
            if (candidates.front() <= i - k) {
                candidates.pop_front();
            }
            if (i >= k - 1) {
                result.push_back(nums[candidates.front()]);
            }
        }
        return result;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        // Indices of readings that could still be a window's maximum,
        // with their values in decreasing order from front to back.
        Deque<Integer> candidates = new ArrayDeque<>();
        int[] result = new int[nums.length - k + 1];
        for (int i = 0; i < nums.length; i++) {
            // A new reading outlives every smaller one before it.
            while (!candidates.isEmpty() && nums[candidates.peekLast()] <= nums[i]) {
                candidates.pollLast();
            }
            candidates.addLast(i);
            // The front has slid out of the window.
            if (candidates.peekFirst() <= i - k) {
                candidates.pollFirst();
            }
            if (i >= k - 1) {
                result[i - k + 1] = nums[candidates.peekFirst()];
            }
        }
        return result;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func maxSlidingWindow(nums []int, k int) []int {
	// Indices of readings that could still be a window's maximum,
	// with their values in decreasing order from front to back.
	candidates := []int{}
	result := []int{}
	for i, x := range nums {
		// A new reading outlives every smaller one before it.
		for len(candidates) > 0 && nums[candidates[len(candidates)-1]] <= x {
			candidates = candidates[:len(candidates)-1]
		}
		candidates = append(candidates, i)
		// The front has slid out of the window.
		if candidates[0] <= i-k {
			candidates = candidates[1:]
		}
		if i >= k-1 {
			result = append(result, nums[candidates[0]])
		}
	}
	return result
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
use std::collections::VecDeque;

impl Solution {
    pub fn max_sliding_window(nums: Vec<i32>, k: i32) -> Vec<i32> {
        let k = k as usize;
        // Indices of readings that could still be a window's maximum,
        // with their values in decreasing order from front to back.
        let mut candidates: VecDeque<usize> = VecDeque::new();
        let mut result = Vec::with_capacity(nums.len() + 1 - k);
        for i in 0..nums.len() {
            // A new reading outlives every smaller one before it.
            while let Some(&last) = candidates.back() {
                if nums[last] <= nums[i] {
                    candidates.pop_back();
                } else {
                    break;
                }
            }
            candidates.push_back(i);
            // The front has slid out of the window.
            if candidates[0] + k <= i {
                candidates.pop_front();
            }
            if i + 1 >= k {
                result.push(nums[candidates[0]]);
            }
        }
        result
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Storing values instead of positions.** Then there's no way to tell whether the front has left the window, especially when the same value appears more than once.
- **Checking the front before adding the new reading,** or reporting before the first window is full. Both are off-by-one errors that only show up at the start.
- **Using `<` instead of `<=` when forgetting smaller readings.** It still works, because positions tell equal readings apart, but the queue keeps more entries than it needs.
- **Assuming the queue is short.** On readings that only ever fall, nothing is forgotten until it leaves the window, and the queue holds all *k*.

## Related

- The other exercise in this category: Shortest Subarray with Sum at Least K (LeetCode 862), coming in a later batch.
- Concept pages: [queues](../../dsa/queues.md), [heaps](../../dsa/heaps.md), [amortised cost](../../dsa/amortised-cost.md), [growth](../../dsa/growth.md).
- More practice of the same shape: problems tagged "monotonic queue" on LeetCode or NeetCode.
