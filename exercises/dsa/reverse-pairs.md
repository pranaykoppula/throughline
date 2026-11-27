# The price that more than halved

An exercise in the category **split, solve, combine**. It's LeetCode 493, [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/), rated Hard.

## The situation

A market regulator watches for sudden collapses in the prices of small shares. One of its measures, for each share, is how many pairs of days had the later price at less than half the earlier one, as a rough count of how often holders lost more than half their money. The regulator keeps a closing price for every trading day of every listed share, and runs the measure across thousands of shares each week.

## The problem

You're given a list of whole numbers. Count the pairs of positions *i* < *j* where the number at *i* is more than twice the number at *j*.

For `1 3 2 3 1`, the answer is 2: the pairs are the 3 at position 1 with the 1 at the end, and the 3 at position 3 with the same 1.

## The question it asks

"For each number, how many later numbers are small enough?" It's the same question as [the readings that came after](count-of-smaller-numbers-after-self.md), with "smaller than" replaced by "less than half of". Pairs that cross from one half of the list to the other can be counted when both halves are sorted, which is split, solve, combine: [divide and conquer](../../dsa/divide-and-conquer.md). See the row for split, solve, combine in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Check every pair. It's two nested loops, so the work grows with the square of the number of days ([growth](../../dsa/growth.md)): for a share with twenty years of trading days, about twelve million comparisons, for every share, every week.

The other tempting answer is to copy the previous exercise: count during the merge, when a right-half number is placed before a left-half one. Here that's wrong. The merge places numbers by plain order, so a right-half number placed early is smaller than the left number, but not necessarily less than half of it.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Split the list in half and count the pairs inside each half recursively. What's left is pairs with one number in each half. Does the order within each half matter for counting those?

</details>

<details markdown="1"><summary>Hint 2</summary>

It doesn't, so you may as well sort each half. If the left half is sorted, then as you move through it, the numbers get bigger, and more of the right half becomes "less than half" of them. What does that let you do with a pointer into the right half?

</details>

<details markdown="1"><summary>Hint 3</summary>

Count first, with one pointer per half, and then merge as a separate step. The counting test and the merging test are different comparisons.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Merge sort the list, and at each merge, count before you merge.

1. **Split** the range in half, and sort and count each half recursively.
2. **Count the crossing pairs.** Both halves are sorted. Walk the left half from smallest to largest, keeping a pointer *j* into the right half. For each left number *x*, move *j* forward while `x > 2 × right[j]`. Every right number before *j* pairs with *x*, so add the count of them. Because *x* only grows, *j* only moves forward, so this is one pass.
3. **Merge** the two halves in the usual way.

**Why counting and merging are separate:** merging asks "which is smaller?", counting asks "is one more than twice the other?". In [the readings that came after](count-of-smaller-numbers-after-self.md) those were the same question, so one pass did both. Here they aren't, so the pass that counts needs its own pointer.

**Why every pair is counted once:** two positions stay in the same half until some split separates them, and that split's count is the only one that considers them together. Sorting within a half doesn't change which side of the split a number is on.

**Why the arithmetic needs care:** twice a large 32-bit number doesn't fit in 32 bits. Do the comparison in 64 bits.

**Time:** proportional to *n* log *n*. **Memory:** proportional to *n*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        def sort(a: List[int]) -> int:
            # Sort a, and return how many pairs i < j in it have a[i] > 2 * a[j].
            if len(a) <= 1:
                return 0
            mid = len(a) // 2
            left, right = a[:mid], a[mid:]
            count = sort(left) + sort(right)
            # Both halves are sorted: count the pairs that cross from left to right.
            j = 0
            for x in left:
                while j < len(right) and x > 2 * right[j]:
                    j += 1
                count += j   # right[0..j) are all small enough for x
            # Then merge, as merge sort does.
            i = j = k = 0
            while i < len(left) or j < len(right):
                if j == len(right) or (i < len(left) and left[i] <= right[j]):
                    a[k] = left[i]
                    i += 1
                else:
                    a[k] = right[j]
                    j += 1
                k += 1
            return count

        return sort(list(nums))
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
    vector<int> merged;

    // Sort a[lo, hi), and return how many pairs i < j in it have a[i] > 2 * a[j].
    long long sortRange(vector<int>& a, int lo, int hi) {
        if (hi - lo <= 1) return 0;
        int mid = (lo + hi) / 2;
        long long count = sortRange(a, lo, mid) + sortRange(a, mid, hi);
        // Both halves are sorted: count the pairs that cross from left to right.
        int j = mid;
        for (int i = lo; i < mid; i++) {
            while (j < hi && (long long)a[i] > 2LL * a[j]) j++;  // 64 bits: 2 * a[j] can overflow
            count += j - mid;
        }
        // Then merge, as merge sort does.
        merge(a.begin() + lo, a.begin() + mid, a.begin() + mid, a.begin() + hi, merged.begin() + lo);
        copy(merged.begin() + lo, merged.begin() + hi, a.begin() + lo);
        return count;
    }

public:
    int reversePairs(vector<int>& nums) {
        vector<int> a = nums;
        merged.assign(a.size(), 0);
        return (int)sortRange(a, 0, a.size());
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    private int[] merged;

    public int reversePairs(int[] nums) {
        int[] a = nums.clone();
        merged = new int[a.length];
        return (int) sortRange(a, 0, a.length);
    }

    // Sort a[lo, hi), and return how many pairs i < j in it have a[i] > 2 * a[j].
    private long sortRange(int[] a, int lo, int hi) {
        if (hi - lo <= 1) return 0;
        int mid = (lo + hi) / 2;
        long count = sortRange(a, lo, mid) + sortRange(a, mid, hi);
        // Both halves are sorted: count the pairs that cross from left to right.
        int j = mid;
        for (int i = lo; i < mid; i++) {
            while (j < hi && (long) a[i] > 2L * a[j]) j++;  // 64 bits: 2 * a[j] can overflow
            count += j - mid;
        }
        // Then merge, as merge sort does.
        int i = lo, r = mid, k = lo;
        while (i < mid || r < hi) {
            if (r == hi || (i < mid && a[i] <= a[r])) merged[k++] = a[i++];
            else merged[k++] = a[r++];
        }
        System.arraycopy(merged, lo, a, lo, hi - lo);
        return count;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func reversePairs(nums []int) int {
	a := append([]int(nil), nums...)
	merged := make([]int, len(a))
	// Sort a[lo:hi], and return how many pairs i < j in it have a[i] > 2 * a[j].
	var sortRange func(lo, hi int) int
	sortRange = func(lo, hi int) int {
		if hi-lo <= 1 {
			return 0
		}
		mid := (lo + hi) / 2
		count := sortRange(lo, mid) + sortRange(mid, hi)
		// Both halves are sorted: count the pairs that cross from left to right.
		j := mid
		for i := lo; i < mid; i++ {
			for j < hi && a[i] > 2*a[j] { // Go's int is 64 bits, so 2 * a[j] can't overflow
				j++
			}
			count += j - mid
		}
		// Then merge, as merge sort does.
		i, r, k := lo, mid, lo
		for i < mid || r < hi {
			if r == hi || (i < mid && a[i] <= a[r]) {
				merged[k] = a[i]
				i++
			} else {
				merged[k] = a[r]
				r++
			}
			k++
		}
		copy(a[lo:hi], merged[lo:hi])
		return count
	}
	return sortRange(0, len(a))
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn reverse_pairs(nums: Vec<i32>) -> i32 {
        let mut a: Vec<i64> = nums.iter().map(|&x| x as i64).collect(); // 64 bits: 2 * x can overflow i32
        let mut merged = vec![0i64; a.len()];
        let n = a.len();
        Self::sort_range(&mut a, &mut merged, 0, n) as i32
    }

    // Sort a[lo..hi], and return how many pairs i < j in it have a[i] > 2 * a[j].
    fn sort_range(a: &mut Vec<i64>, merged: &mut Vec<i64>, lo: usize, hi: usize) -> i64 {
        if hi - lo <= 1 {
            return 0;
        }
        let mid = (lo + hi) / 2;
        let mut count = Self::sort_range(a, merged, lo, mid) + Self::sort_range(a, merged, mid, hi);
        // Both halves are sorted: count the pairs that cross from left to right.
        let mut j = mid;
        for i in lo..mid {
            while j < hi && a[i] > 2 * a[j] {
                j += 1;
            }
            count += (j - mid) as i64;
        }
        // Then merge, as merge sort does.
        let (mut i, mut r, mut k) = (lo, mid, lo);
        while i < mid || r < hi {
            if r == hi || (i < mid && a[i] <= a[r]) {
                merged[k] = a[i];
                i += 1;
            } else {
                merged[k] = a[r];
                r += 1;
            }
            k += 1;
        }
        a[lo..hi].copy_from_slice(&merged[lo..hi]);
        count
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Counting inside the merge.** The merge's comparison isn't the pair test; count in a separate pass first.
- **Overflow in `2 × nums[j]`.** With numbers near 2³¹, double them in 64-bit arithmetic.
- **Resetting the pointer for every left number.** The left half is sorted, so the pointer only ever moves forward; resetting it makes the pass quadratic.
- **Using "at least twice".** The pair needs strictly more than twice; `2 1` isn't a pair.

## Related

- The other exercise in this category: [the readings that came after](count-of-smaller-numbers-after-self.md) (LeetCode 315).
- Concept pages: [divide and conquer](../../dsa/divide-and-conquer.md), [sorting](../../dsa/sorting.md), [growth](../../dsa/growth.md).
- More practice of the same shape: counting the ranges of a list whose sums fall between two bounds, with a merge sort over running totals.
