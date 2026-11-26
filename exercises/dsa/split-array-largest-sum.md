# Splitting the translation

An exercise in the category **order and halving**. It's LeetCode 410, [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/), rated Hard.

## The situation

A publisher has bought the rights to a long novel and wants it translated quickly. It has hired *k* translators, and to keep each translator's voice consistent across a stretch of the story, each will take a run of consecutive chapters: the first translator from chapter 1 up to some chapter, the next from there on, and so on. The chapters vary a lot in length. The book is finished when the slowest translator finishes, so the publisher wants to split the chapters so that the largest workload, in words, is as small as possible.

## The problem

You're given a list of non-negative whole numbers and a number *k*. Split the list into *k* runs of consecutive numbers, each with at least one number. Find the smallest possible value of the largest run total.

For chapter lengths `7 2 5 10 8` and two translators, the best split is `7 2 5` and `10 8`, whose totals are 14 and 18, so the answer is 18.

## The question it asks

"What's the smallest limit that works?" The trick is to stop asking "how should I split?" and ask "could I split so that nobody gets more than *L* words?", a yes-or-no question whose answer changes only once as *L* grows. That's a question you can answer by [halving](../../dsa/divide-and-conquer.md). See the order-and-halving row in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Try every way to place the *k* − 1 cuts between chapters, and keep the split whose largest run is smallest. The number of ways explodes as the book and the team grow ([growth](../../dsa/growth.md)).

The better first answer is [dynamic programming](../../dsa/dynamic-programming.md): the best way to split the first *i* chapters among *p* translators is built from the best ways to split fewer chapters among *p* − 1. It's correct and a good answer in an interview, but it takes time in proportion to *n*² × *k*, which is slow for long books and big teams.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Suppose someone proposes a limit: nobody translates more than *L* words. How would you check, quickly, whether *k* translators are enough to stay within it?

</details>

<details markdown="1"><summary>Hint 2</summary>

Give chapters to the first translator, in order, until the next one would take them over *L*. Then start the second translator. If this greedy fill needs at most *k* translators, the limit *L* is achievable. Why is filling each translator as full as possible never a mistake here?

</details>

<details markdown="1"><summary>Hint 3</summary>

If a limit *L* works, any bigger limit works too. So the achievable limits form a range with a smallest member. What's the smallest limit that could possibly work, and the largest you'd ever need?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Search over the answer, not the split.

1. **Bound the answer.** The largest run total is at least the longest single chapter (someone must translate it) and at most the whole book (one translator does everything).
2. **Write the check.** For a limit *L*, walk the chapters in order, adding each to the current translator's load. When a chapter would push the load over *L*, start a new translator with that chapter. Count the translators used. *L* works if the count is at most *k*.
3. **Binary-search the limit.** Take the middle of the range. If it works, the answer is that limit or smaller; otherwise it's bigger. Halve until the range is one value.

**Why greedy filling is safe:** giving the current translator one more chapter, when it fits, can never make things worse for the translators after them: it only leaves them less to do. So the greedy check needs the fewest translators possible for that limit. This is a [greedy algorithm](../../dsa/greedy.md) where the greedy choice provably can't block a better one.

**Why it's fast:** the check is one pass through the chapters, and the binary search needs about log(total words) checks, around 30 for a book of a billion words. The halving is over the range of possible answers, not over a list, which is the move that makes this problem easy once you see it.

**Time:** proportional to *n* × log(total). **Memory:** a fixed amount.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def days_needed(limit: int) -> int:
            # Fill each day greedily; start a new day when the next job won't fit.
            days, load = 1, 0
            for x in nums:
                if load + x > limit:
                    days += 1
                    load = 0
                load += x
            return days

        # The answer is at least the biggest single job and at most everything in one day.
        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= k:
                hi = mid          # this limit works; try a smaller one
            else:
                lo = mid + 1      # too tight; the answer is bigger
        return lo
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        // Fill each day greedily; start a new day when the next job won't fit.
        auto daysNeeded = [&](long long limit) {
            int days = 1;
            long long load = 0;
            for (int x : nums) {
                if (load + x > limit) {
                    days++;
                    load = 0;
                }
                load += x;
            }
            return days;
        };
        // The answer is at least the biggest single job and at most everything in one day.
        long long lo = *max_element(nums.begin(), nums.end());
        long long hi = accumulate(nums.begin(), nums.end(), 0LL);
        while (lo < hi) {
            long long mid = lo + (hi - lo) / 2;
            if (daysNeeded(mid) <= k) {
                hi = mid;      // this limit works; try a smaller one
            } else {
                lo = mid + 1;  // too tight; the answer is bigger
            }
        }
        return (int)lo;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    public int splitArray(int[] nums, int k) {
        // The answer is at least the biggest single job and at most everything in one day.
        long lo = 0, hi = 0;
        for (int x : nums) {
            lo = Math.max(lo, x);
            hi += x;
        }
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (daysNeeded(nums, mid) <= k) {
                hi = mid;      // this limit works; try a smaller one
            } else {
                lo = mid + 1;  // too tight; the answer is bigger
            }
        }
        return (int) lo;
    }

    // Fill each day greedily; start a new day when the next job won't fit.
    private int daysNeeded(int[] nums, long limit) {
        int days = 1;
        long load = 0;
        for (int x : nums) {
            if (load + x > limit) {
                days++;
                load = 0;
            }
            load += x;
        }
        return days;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func splitArray(nums []int, k int) int {
	// Fill each day greedily; start a new day when the next job won't fit.
	daysNeeded := func(limit int) int {
		days, load := 1, 0
		for _, x := range nums {
			if load+x > limit {
				days++
				load = 0
			}
			load += x
		}
		return days
	}
	// The answer is at least the biggest single job and at most everything in one day.
	lo, hi := 0, 0
	for _, x := range nums {
		lo = max(lo, x)
		hi += x
	}
	for lo < hi {
		mid := lo + (hi-lo)/2
		if daysNeeded(mid) <= k {
			hi = mid // this limit works; try a smaller one
		} else {
			lo = mid + 1 // too tight; the answer is bigger
		}
	}
	return lo
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn split_array(nums: Vec<i32>, k: i32) -> i32 {
        // Fill each day greedily; start a new day when the next job won't fit.
        let days_needed = |limit: i64| -> i32 {
            let (mut days, mut load) = (1, 0i64);
            for &x in &nums {
                if load + x as i64 > limit {
                    days += 1;
                    load = 0;
                }
                load += x as i64;
            }
            days
        };
        // The answer is at least the biggest single job and at most everything in one day.
        let mut lo = *nums.iter().max().unwrap() as i64;
        let mut hi: i64 = nums.iter().map(|&x| x as i64).sum();
        while lo < hi {
            let mid = lo + (hi - lo) / 2;
            if days_needed(mid) <= k {
                hi = mid; // this limit works; try a smaller one
            } else {
                lo = mid + 1; // too tight; the answer is bigger
            }
        }
        lo as i32
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Searching the wrong range.** The lower bound must be the largest single number, not 0 or 1, or the check fails in confusing ways.
- **Getting the binary search boundary wrong.** When a limit works, keep it in the range (`hi = mid`); when it doesn't, move past it (`lo = mid + 1`).
- **Overflow.** Totals can exceed a 32-bit integer in some languages' arithmetic, especially when computing the middle; use 64-bit totals or `lo + (hi − lo) / 2`.
- **Worrying about using fewer than *k* runs.** If the greedy fill needs fewer translators than *k*, you can always split a run further without raising the largest total, so "at most *k*" is the right test.

## Related

- The other exercise in this category: [two depots, one median](median-of-two-sorted-arrays.md) (LeetCode 4).
- Concept pages: [divide and conquer](../../dsa/divide-and-conquer.md), [greedy algorithms](../../dsa/greedy.md), [dynamic programming](../../dsa/dynamic-programming.md), [growth](../../dsa/growth.md).
- More practice of the same shape: problems tagged "binary search on the answer", such as shipping packages within a number of days.
