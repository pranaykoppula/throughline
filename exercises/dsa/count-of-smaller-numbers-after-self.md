# The readings that came after

An exercise in the category **split, solve, combine**. It's LeetCode 315, [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/), rated Hard.

## The situation

An energy company keeps a year of daily output readings for each of its wind farms. For each day, an analyst wants to know how many later days produced less, as a rough measure of whether that day was the start of a decline. A farm with ten years of readings has more than three thousand days, the company has hundreds of farms, and the report runs every night.

## The problem

You're given a list of whole numbers. Return a list of the same length where each entry is how many numbers to the right of that position are strictly smaller than the number there.

For `5 2 6 1`, the answer is `2 1 1 0`: after 5 come 2 and 1, which are smaller; after 2 comes 1; after 6 comes 1; and nothing comes after 1.

## The question it asks

"How many smaller numbers cross from my right to my left?" If you sorted the list, every smaller number to an entry's right would have to move past it to the left. Merge sort does its moving in halves, and the halves can count what crosses. That's split, solve, combine: [divide and conquer](../../dsa/divide-and-conquer.md). See the row for split, solve, combine in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

For each day, look at every later day and count the smaller ones. It's two nested loops, and the work grows with the square of the number of days ([growth](../../dsa/growth.md)): for ten years of readings, about six million comparisons per farm, every night, for every farm.

A smarter idea is to walk from the right, keeping the days seen so far in a sorted list, and to find each day's place with [binary search](../../dsa/divide-and-conquer.md). The position is the count. Finding the place is fast, but inserting into the middle of a list shifts everything after it, so it's still quadratic in the worst case.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Split the list in half. For a number in the left half, its count is the smaller numbers to its right in the left half, plus all the smaller numbers in the right half. If you had already solved each half on its own, what's missing?

</details>

<details markdown="1"><summary>Hint 2</summary>

The missing part is: for each number on the left, how many numbers on the right are smaller. If both halves were sorted, could you count that for every number on the left in one pass?

</details>

<details markdown="1"><summary>Hint 3</summary>

Merge the two sorted halves as merge sort does. When you place a number from the left half, every number already placed from the right half is smaller than it, and was to its right. Add that many to its count. You'll need to remember where each number started, because sorting moves it.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Merge sort the positions, ordered by their values, and count during the merges.

1. **Sort positions, not values,** so you can always tell where a number started and add to the right count.
2. **Split** the range in half and sort each half, recursively. Each half's counts are then complete for pairs within that half.
3. **Merge** the halves. Walk through the left half in order. Before placing each left number, place every right number smaller than it. The number of right numbers placed so far is how many smaller numbers from the right half cross it, so add that to its count. Then place it.
4. **The rest of the right half** goes after the left half, and adds nothing, since no left number is waiting.

**Why every pair is counted once:** two positions are in the same half until some split separates them, and that split's merge is the only place their order is compared. So each pair "smaller number to my right" is counted exactly once.

**Why ties aren't counted:** right numbers are placed first only when they're strictly smaller. An equal number waits until after the left number, so it doesn't add to its count.

**Why it's fast:** each level of splitting merges every number once, and there are about log *n* levels, the same as merge sort ([sorting](../../dsa/sorting.md)). The counting rides along for free.

**Time:** proportional to *n* log *n*. **Memory:** proportional to *n*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        counts = [0] * len(nums)
        order = list(range(len(nums)))   # positions, to be sorted by value

        def sort(lo: int, hi: int) -> None:
            # Sort order[lo:hi] by value, counting for each position
            # how many smaller values from its right cross to its left.
            if hi - lo <= 1:
                return
            mid = (lo + hi) // 2
            sort(lo, mid)
            sort(mid, hi)
            merged = []
            j = mid
            for i in range(lo, mid):
                # Every right-half value placed before this one is smaller and was to its right.
                while j < hi and nums[order[j]] < nums[order[i]]:
                    merged.append(order[j])
                    j += 1
                counts[order[i]] += j - mid
                merged.append(order[i])
            merged.extend(order[j:hi])
            order[lo:hi] = merged

        sort(0, len(nums))
        return counts
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
    vector<int> counts, order, merged;

    // Sort order[lo, hi) by value, counting for each position
    // how many smaller values from its right cross to its left.
    void sortRange(const vector<int>& nums, int lo, int hi) {
        if (hi - lo <= 1) return;
        int mid = (lo + hi) / 2;
        sortRange(nums, lo, mid);
        sortRange(nums, mid, hi);
        int j = mid, k = lo;
        for (int i = lo; i < mid; i++) {
            // Every right-half value placed before this one is smaller and was to its right.
            while (j < hi && nums[order[j]] < nums[order[i]]) merged[k++] = order[j++];
            counts[order[i]] += j - mid;
            merged[k++] = order[i];
        }
        while (j < hi) merged[k++] = order[j++];
        copy(merged.begin() + lo, merged.begin() + hi, order.begin() + lo);
    }

public:
    vector<int> countSmaller(vector<int>& nums) {
        int n = nums.size();
        counts.assign(n, 0);
        merged.assign(n, 0);
        order.resize(n);
        iota(order.begin(), order.end(), 0);  // positions, to be sorted by value
        sortRange(nums, 0, n);
        return counts;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    private int[] counts, order, merged;

    public List<Integer> countSmaller(int[] nums) {
        int n = nums.length;
        counts = new int[n];
        merged = new int[n];
        order = new int[n];  // positions, to be sorted by value
        for (int i = 0; i < n; i++) order[i] = i;
        sortRange(nums, 0, n);
        List<Integer> result = new ArrayList<>();
        for (int c : counts) result.add(c);
        return result;
    }

    // Sort order[lo, hi) by value, counting for each position
    // how many smaller values from its right cross to its left.
    private void sortRange(int[] nums, int lo, int hi) {
        if (hi - lo <= 1) return;
        int mid = (lo + hi) / 2;
        sortRange(nums, lo, mid);
        sortRange(nums, mid, hi);
        int j = mid, k = lo;
        for (int i = lo; i < mid; i++) {
            // Every right-half value placed before this one is smaller and was to its right.
            while (j < hi && nums[order[j]] < nums[order[i]]) merged[k++] = order[j++];
            counts[order[i]] += j - mid;
            merged[k++] = order[i];
        }
        while (j < hi) merged[k++] = order[j++];
        System.arraycopy(merged, lo, order, lo, hi - lo);
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func countSmaller(nums []int) []int {
	n := len(nums)
	counts := make([]int, n)
	merged := make([]int, n)
	order := make([]int, n) // positions, to be sorted by value
	for i := range order {
		order[i] = i
	}
	// Sort order[lo:hi] by value, counting for each position
	// how many smaller values from its right cross to its left.
	var sortRange func(lo, hi int)
	sortRange = func(lo, hi int) {
		if hi-lo <= 1 {
			return
		}
		mid := (lo + hi) / 2
		sortRange(lo, mid)
		sortRange(mid, hi)
		j, k := mid, lo
		for i := lo; i < mid; i++ {
			// Every right-half value placed before this one is smaller and was to its right.
			for j < hi && nums[order[j]] < nums[order[i]] {
				merged[k] = order[j]
				k++
				j++
			}
			counts[order[i]] += j - mid
			merged[k] = order[i]
			k++
		}
		for ; j < hi; j++ {
			merged[k] = order[j]
			k++
		}
		copy(order[lo:hi], merged[lo:hi])
	}
	sortRange(0, n)
	return counts
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn count_smaller(nums: Vec<i32>) -> Vec<i32> {
        let n = nums.len();
        let mut counts = vec![0; n];
        let mut order: Vec<usize> = (0..n).collect(); // positions, to be sorted by value
        let mut merged = vec![0usize; n];
        Self::sort_range(&nums, 0, n, &mut order, &mut merged, &mut counts);
        counts
    }

    // Sort order[lo..hi] by value, counting for each position
    // how many smaller values from its right cross to its left.
    fn sort_range(nums: &[i32], lo: usize, hi: usize, order: &mut Vec<usize>, merged: &mut Vec<usize>, counts: &mut Vec<i32>) {
        if hi - lo <= 1 {
            return;
        }
        let mid = (lo + hi) / 2;
        Self::sort_range(nums, lo, mid, order, merged, counts);
        Self::sort_range(nums, mid, hi, order, merged, counts);
        let (mut j, mut k) = (mid, lo);
        for i in lo..mid {
            // Every right-half value placed before this one is smaller and was to its right.
            while j < hi && nums[order[j]] < nums[order[i]] {
                merged[k] = order[j];
                k += 1;
                j += 1;
            }
            counts[order[i]] += (j - mid) as i32;
            merged[k] = order[i];
            k += 1;
        }
        while j < hi {
            merged[k] = order[j];
            k += 1;
            j += 1;
        }
        order[lo..hi].copy_from_slice(&merged[lo..hi]);
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Sorting the values and losing their positions.** The counts belong to positions; sort indices by value.
- **Counting ties.** Place a right number first only when it's strictly smaller.
- **Counting at the wrong moment.** Add the count when the left number is placed, not when a right number is; the right numbers placed so far are exactly the smaller ones.
- **Reaching for a balanced tree you have to write yourself.** A binary indexed tree over the values also works and is shorter, but needs the values mapped to ranks first. Merge sort needs nothing extra.

## Related

- The other exercise in this category: [the price that more than halved](reverse-pairs.md) (LeetCode 493).
- Concept pages: [divide and conquer](../../dsa/divide-and-conquer.md), [sorting](../../dsa/sorting.md), [growth](../../dsa/growth.md).
- More practice of the same shape: counting inversions, the number of pairs that are out of order, which is the same merge with a running total.
