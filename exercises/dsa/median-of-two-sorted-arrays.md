# Two depots, one median

An exercise in the category **order and halving**. It's LeetCode 4, [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/), rated Hard.

## The situation

A delivery company runs two depots, and each depot's system keeps its delivery times for the day in a sorted list, fastest first. The operations dashboard wants the median delivery time across both depots, refreshed every few seconds. Each list is held by a different service, and reading a value from either one is a request over the network. The lists run to hundreds of thousands of deliveries on a busy day, so whatever the dashboard does, it needs to read as few values as possible.

## The problem

You're given two lists of numbers, each sorted from smallest to largest. Find the median of all the numbers in both lists together: the middle value if there's an odd number of values, or the average of the two middle values if there's an even number. The time taken must grow with the logarithm of the total size, not the size itself.

For `1 3` and `2`, the combined list is `1 2 3`, so the median is 2. For `1 2` and `3 4`, it's the average of 2 and 3, which is 2.5.

## The question it asks

"Where does the middle fall?", a question about [order](../../dsa/sorting.md). With the logarithm in the time limit, it's really asking for [halving](../../dsa/divide-and-conquer.md): rule out half of what's left at each step. See the order-and-halving row in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Merge the two lists, as merge sort does, and read off the middle. It's simple, and you can stop as soon as you reach the middle, so it reads about half of all the values. That's linear in the total size: hundreds of thousands of network reads every few seconds.

The next idea is to binary-search for the median's value, counting how many values in each list fall below a guess. That works, but each guess costs a binary search in each list, and the steps depend on the range of the values, not just how many there are. There's a cleaner way that halves the shorter list directly.

## Hints

<details markdown="1"><summary>Hint 1</summary>

The median splits the combined list into a left half and a right half of equal size (or with one extra on the left). Suppose the left half takes *i* values from the first list. How many must it take from the second?

</details>

<details markdown="1"><summary>Hint 2</summary>

A choice of *i* is right exactly when everything on the left is no bigger than everything on the right. Because each list is sorted, that only needs two comparisons, across the boundary between the lists.

</details>

<details markdown="1"><summary>Hint 3</summary>

If the first list's last value on the left is bigger than the second list's first value on the right, you took too many from the first list. If it's the other way round, too few. Which way should *i* move, and by how much?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Call the shorter list *a* (length *m*) and the longer one *b* (length *n*). The left half of the combined list has `half = (m + n + 1) / 2` values (rounding down). If it takes *i* values from *a*, it takes `j = half − i` from *b*.

Binary-search *i* between 0 and *m*. For each guess, look at four values at the boundary:

- `aLeft`, the last of *a*'s values on the left (or minus infinity if *i* is 0), and `aRight`, the first of *a*'s on the right (or plus infinity if *i* is *m*);
- `bLeft` and `bRight`, the same for *b* at *j*.

Then:

1. **If `aLeft > bRight`,** too many values came from *a*: search smaller *i*.
2. **If `bLeft > aRight`,** too few came from *a*: search larger *i*.
3. **Otherwise the split is right.** Every value on the left is no bigger than every value on the right. If the total is odd, the median is the larger of `aLeft` and `bLeft`. If it's even, it's the average of that and the smaller of `aRight` and `bRight`.

Searching the shorter list matters for two reasons: it takes fewer steps, and it guarantees *j* never falls outside *b*.

**Why it's fast:** each guess halves the range of *i* that's left, so the number of guesses grows with the logarithm of the shorter list, and each guess reads four values. The approach is [divide and conquer](../../dsa/divide-and-conquer.md) in its purest form, like Kwesi's bisection: rule out half of the possibilities with every question ([information gain](../../info/information-gain.md)).

**Time:** proportional to log(min(*m*, *n*)). **Memory:** a fixed amount.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Search the shorter list, so the halving takes the fewest steps.
        a, b = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)
        m, n = len(a), len(b)
        half = (m + n + 1) // 2
        lo, hi = 0, m
        while lo <= hi:
            # Take i from a and the rest of the left half from b.
            i = (lo + hi) // 2
            j = half - i
            a_left = a[i - 1] if i > 0 else float("-inf")
            a_right = a[i] if i < m else float("inf")
            b_left = b[j - 1] if j > 0 else float("-inf")
            b_right = b[j] if j < n else float("inf")
            if a_left > b_right:
                hi = i - 1        # took too many from a
            elif b_left > a_right:
                lo = i + 1        # took too few from a
            else:
                # Every left value is no bigger than every right value.
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
        raise ValueError("inputs must be sorted")
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        // Search the shorter list, so the halving takes the fewest steps.
        if (nums1.size() > nums2.size()) return findMedianSortedArrays(nums2, nums1);
        const vector<int>& a = nums1;
        const vector<int>& b = nums2;
        int m = a.size(), n = b.size();
        int half = (m + n + 1) / 2;
        int lo = 0, hi = m;
        while (lo <= hi) {
            // Take i from a and the rest of the left half from b.
            int i = (lo + hi) / 2;
            int j = half - i;
            long long aLeft = i > 0 ? a[i - 1] : LLONG_MIN;
            long long aRight = i < m ? a[i] : LLONG_MAX;
            long long bLeft = j > 0 ? b[j - 1] : LLONG_MIN;
            long long bRight = j < n ? b[j] : LLONG_MAX;
            if (aLeft > bRight) {
                hi = i - 1;  // took too many from a
            } else if (bLeft > aRight) {
                lo = i + 1;  // took too few from a
            } else {
                // Every left value is no bigger than every right value.
                if ((m + n) % 2) return (double)max(aLeft, bLeft);
                return (max(aLeft, bLeft) + min(aRight, bRight)) / 2.0;
            }
        }
        return 0.0;  // not reached for sorted inputs
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        // Search the shorter array, so the halving takes the fewest steps.
        if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
        int[] a = nums1, b = nums2;
        int m = a.length, n = b.length;
        int half = (m + n + 1) / 2;
        int lo = 0, hi = m;
        while (lo <= hi) {
            // Take i from a and the rest of the left half from b.
            int i = (lo + hi) / 2;
            int j = half - i;
            long aLeft = i > 0 ? a[i - 1] : Long.MIN_VALUE;
            long aRight = i < m ? a[i] : Long.MAX_VALUE;
            long bLeft = j > 0 ? b[j - 1] : Long.MIN_VALUE;
            long bRight = j < n ? b[j] : Long.MAX_VALUE;
            if (aLeft > bRight) {
                hi = i - 1;  // took too many from a
            } else if (bLeft > aRight) {
                lo = i + 1;  // took too few from a
            } else {
                // Every left value is no bigger than every right value.
                if ((m + n) % 2 == 1) return Math.max(aLeft, bLeft);
                return (Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2.0;
            }
        }
        return 0.0;  // not reached for sorted inputs
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
import "math"

func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
	// Search the shorter slice, so the halving takes the fewest steps.
	if len(nums1) > len(nums2) {
		return findMedianSortedArrays(nums2, nums1)
	}
	a, b := nums1, nums2
	m, n := len(a), len(b)
	half := (m + n + 1) / 2
	lo, hi := 0, m
	for lo <= hi {
		// Take i from a and the rest of the left half from b.
		i := (lo + hi) / 2
		j := half - i
		aLeft, aRight, bLeft, bRight := math.MinInt, math.MaxInt, math.MinInt, math.MaxInt
		if i > 0 {
			aLeft = a[i-1]
		}
		if i < m {
			aRight = a[i]
		}
		if j > 0 {
			bLeft = b[j-1]
		}
		if j < n {
			bRight = b[j]
		}
		if aLeft > bRight {
			hi = i - 1 // took too many from a
		} else if bLeft > aRight {
			lo = i + 1 // took too few from a
		} else {
			// Every left value is no bigger than every right value.
			if (m+n)%2 == 1 {
				return float64(max(aLeft, bLeft))
			}
			return float64(max(aLeft, bLeft)+min(aRight, bRight)) / 2
		}
	}
	return 0 // not reached for sorted inputs
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn find_median_sorted_arrays(nums1: Vec<i32>, nums2: Vec<i32>) -> f64 {
        // Search the shorter vector, so the halving takes the fewest steps.
        let (a, b) = if nums1.len() <= nums2.len() { (&nums1, &nums2) } else { (&nums2, &nums1) };
        let (m, n) = (a.len(), b.len());
        let half = (m + n + 1) / 2;
        let (mut lo, mut hi) = (0usize, m);
        loop {
            // Take i from a and the rest of the left half from b.
            let i = (lo + hi) / 2;
            let j = half - i;
            let a_left = if i > 0 { a[i - 1] as i64 } else { i64::MIN };
            let a_right = if i < m { a[i] as i64 } else { i64::MAX };
            let b_left = if j > 0 { b[j - 1] as i64 } else { i64::MIN };
            let b_right = if j < n { b[j] as i64 } else { i64::MAX };
            if a_left > b_right {
                hi = i - 1; // took too many from a
            } else if b_left > a_right {
                lo = i + 1; // took too few from a
            } else {
                // Every left value is no bigger than every right value.
                if (m + n) % 2 == 1 {
                    return a_left.max(b_left) as f64;
                }
                return (a_left.max(b_left) + a_right.min(b_right)) as f64 / 2.0;
            }
        }
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Searching the longer list.** Then *j* can go negative or past the end of the shorter list.
- **Mishandling empty lists and edges.** Use minus and plus infinity for values beyond either end of a list, rather than special cases.
- **Rounding the halves wrongly.** With `half = (m + n + 1) / 2`, the left half has the extra value when the total is odd, so the median is the largest on the left.
- **Integer division in the average.** The average of two middle values can be a half; divide as a decimal.
- **Merging "to be safe".** It's correct, and it's exactly the linear cost the problem asks you to avoid.

## Related

- The other exercise in this category: [splitting the translation](split-array-largest-sum.md) (LeetCode 410).
- Concept pages: [sorting](../../dsa/sorting.md), [divide and conquer](../../dsa/divide-and-conquer.md), [information gain](../../info/information-gain.md), [growth](../../dsa/growth.md).
- More practice of the same shape: problems tagged "binary search" on LeetCode or NeetCode, especially those searching for a split point.
