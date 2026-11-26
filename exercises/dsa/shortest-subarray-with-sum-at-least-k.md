# The shortest good run

An exercise in the category **next in line, over a window**. It's LeetCode 862, [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/), rated Hard.

## The situation

A language-learning app records its net growth each day: sign-ups minus cancellations. Most days are positive. Some, after a price rise or an outage, are well negative. The marketing team wants to know the shortest stretch of consecutive days in which the app gained at least 10,000 subscribers, net, because that's the fastest it has ever grown and the number they want to beat. Two years of history is about 730 days; the same question asked of hourly figures is 17,520.

## The problem

You're given a list of whole numbers, some of them negative, and a target *k*. Find the length of the shortest run of consecutive numbers whose total is at least *k*. If no run reaches *k*, the answer is −1.

For `2 −1 2` with a target of 3, the whole list adds up to 3 and no shorter run does, so the answer is 3.

## The question it asks

"Which earlier starting point is next in line to matter?" For each day, the runs ending there begin at earlier days, and only a few of those starting points can ever give the best answer. It's a [queue](../../dsa/queues.md) of candidates, like [the busiest five minutes](sliding-window-maximum.md). See [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Try every starting day and add up forwards until the total reaches *k*. It's correct, and it does work in proportion to the square of the number of days ([growth](../../dsa/growth.md)).

The second idea is the one most people reach for: two pointers. Grow the run on the right until it reaches *k*, then shrink it from the left while it still does. That's linear and works beautifully when every number is positive, because adding a day can only raise the total and dropping one can only lower it. With negative days it breaks. Dropping a bad day from the left *raises* the total, so a run that looked too short can become long enough after shrinking, and the two pointers walk past the answer without seeing it.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Keep a running total from the first day. The total of the run from day *i* to day *j* is then the running total at *j* minus the running total just before *i*. The question becomes: for each *j*, find the latest earlier point whose running total is at most (total at *j*) − *k*.

</details>

<details markdown="1"><summary>Hint 2</summary>

Suppose an earlier point has a running total at least as high as a later point. Can the earlier one ever be the better place to start? It's further away, and it gives a smaller run total.

</details>

<details markdown="1"><summary>Hint 3</summary>

Once a starting point has produced a run of total at least *k*, any later end point would only give a longer run from it. So it can be used once and thrown away.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Work with running totals: `prefix[0] = 0`, and `prefix[j]` is the total of the first *j* days. A run from day *i* up to day *j* − 1 totals `prefix[j] − prefix[i]`.

Keep a double-ended queue of starting points *i*, in order, with their running totals strictly increasing from front to back. For each *j* from 0 to *n*:

1. **Use up starts that already work.** While `prefix[j] − prefix[front] ≥ k`, record the length `j − front` and remove the front. Any later *j* would only make a longer run from that start, so it has nothing more to offer.
2. **Drop starts that can never win.** While the back of the queue has a running total at least `prefix[j]`, remove it. Point *j* is later, so it gives a shorter run, and it has a lower or equal total, so it gives a larger run total. It beats the old start on both counts.
3. **Add *j* at the back.**

The answer is the shortest length recorded, or −1 if none was.

**Why it's fast:** every starting point enters the queue once and leaves at most once, so the whole thing is linear, like the [busiest five minutes](sliding-window-maximum.md). The running totals can exceed the range of a 32-bit integer, so the code uses 64-bit totals.

**Time:** proportional to *n*. **Memory:** proportional to *n*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from collections import deque
from typing import List


class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        # prefix[j] - prefix[i] is the total of days i .. j-1.
        prefix = [0]
        for x in nums:
            prefix.append(prefix[-1] + x)
        best = len(nums) + 1
        # Start points worth keeping, with prefix totals increasing from front to back.
        starts = deque()
        for j, total in enumerate(prefix):
            # The oldest start that already reaches k gives its best answer now.
            while starts and total - prefix[starts[0]] >= k:
                best = min(best, j - starts.popleft())
            # A start with a total at least as high as this one is never better.
            while starts and prefix[starts[-1]] >= total:
                starts.pop()
            starts.append(j)
        return best if best <= len(nums) else -1
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int shortestSubarray(vector<int>& nums, int k) {
        int n = nums.size();
        // prefix[j] - prefix[i] is the total of days i .. j-1.
        vector<long long> prefix(n + 1, 0);
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
        int best = n + 1;
        // Start points worth keeping, with prefix totals increasing from front to back.
        deque<int> starts;
        for (int j = 0; j <= n; j++) {
            // The oldest start that already reaches k gives its best answer now.
            while (!starts.empty() && prefix[j] - prefix[starts.front()] >= k) {
                best = min(best, j - starts.front());
                starts.pop_front();
            }
            // A start with a total at least as high as this one is never better.
            while (!starts.empty() && prefix[starts.back()] >= prefix[j]) {
                starts.pop_back();
            }
            starts.push_back(j);
        }
        return best <= n ? best : -1;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int shortestSubarray(int[] nums, int k) {
        int n = nums.length;
        // prefix[j] - prefix[i] is the total of days i .. j-1.
        long[] prefix = new long[n + 1];
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
        int best = n + 1;
        // Start points worth keeping, with prefix totals increasing from front to back.
        Deque<Integer> starts = new ArrayDeque<>();
        for (int j = 0; j <= n; j++) {
            // The oldest start that already reaches k gives its best answer now.
            while (!starts.isEmpty() && prefix[j] - prefix[starts.peekFirst()] >= k) {
                best = Math.min(best, j - starts.pollFirst());
            }
            // A start with a total at least as high as this one is never better.
            while (!starts.isEmpty() && prefix[starts.peekLast()] >= prefix[j]) {
                starts.pollLast();
            }
            starts.addLast(j);
        }
        return best <= n ? best : -1;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func shortestSubarray(nums []int, k int) int {
	n := len(nums)
	// prefix[j] - prefix[i] is the total of days i .. j-1.
	prefix := make([]int, n+1)
	for i, x := range nums {
		prefix[i+1] = prefix[i] + x
	}
	best := n + 1
	// Start points worth keeping, with prefix totals increasing from front to back.
	starts := []int{}
	for j := 0; j <= n; j++ {
		// The oldest start that already reaches k gives its best answer now.
		for len(starts) > 0 && prefix[j]-prefix[starts[0]] >= k {
			if j-starts[0] < best {
				best = j - starts[0]
			}
			starts = starts[1:]
		}
		// A start with a total at least as high as this one is never better.
		for len(starts) > 0 && prefix[starts[len(starts)-1]] >= prefix[j] {
			starts = starts[:len(starts)-1]
		}
		starts = append(starts, j)
	}
	if best <= n {
		return best
	}
	return -1
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
use std::collections::VecDeque;

impl Solution {
    pub fn shortest_subarray(nums: Vec<i32>, k: i32) -> i32 {
        let n = nums.len();
        // prefix[j] - prefix[i] is the total of days i .. j-1.
        let mut prefix = vec![0i64; n + 1];
        for i in 0..n {
            prefix[i + 1] = prefix[i] + nums[i] as i64;
        }
        let k = k as i64;
        let mut best = n + 1;
        // Start points worth keeping, with prefix totals increasing from front to back.
        let mut starts: VecDeque<usize> = VecDeque::new();
        for j in 0..=n {
            // The oldest start that already reaches k gives its best answer now.
            while let Some(&first) = starts.front() {
                if prefix[j] - prefix[first] >= k {
                    best = best.min(j - first);
                    starts.pop_front();
                } else {
                    break;
                }
            }
            // A start with a total at least as high as this one is never better.
            while let Some(&last) = starts.back() {
                if prefix[last] >= prefix[j] {
                    starts.pop_back();
                } else {
                    break;
                }
            }
            starts.push_back(j);
        }
        if best <= n { best as i32 } else { -1 }
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Using two pointers.** It works only when every number is positive; the negative days are the whole difficulty.
- **Overflowing the running total.** With a hundred thousand values of up to a hundred thousand each, totals reach ten billion.
- **Forgetting the starting point before the first day.** `prefix[0] = 0` must be in the queue, or a run that starts on day one is never found.
- **Popping the front only once.** Several starts can all reach *k* at the same *j*; keep going while the front still works, because each later one gives a shorter run.

## Related

- The other exercise in this category: [the busiest five minutes](sliding-window-maximum.md) (LeetCode 239).
- Concept pages: [queues](../../dsa/queues.md), [amortised cost](../../dsa/amortised-cost.md), [growth](../../dsa/growth.md).
- More practice of the same shape: problems tagged "monotonic queue" and "prefix sum" on LeetCode or NeetCode.
