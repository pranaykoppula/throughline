# The first free locker

An exercise in the category **find by key**. It's LeetCode 41, [First Missing Positive](https://leetcode.com/problems/first-missing-positive/), rated Hard.

## The situation

A railway station's luggage lockers are numbered 1, 2, 3 and so on, and the controller in each bank of lockers assigns the lowest-numbered free one to the next customer. It keeps a list of the numbers currently in use, in no particular order, with some junk in it: zeros from cleared slots, the occasional corrupted negative number, and numbers far beyond the bank's size from a misconfigured scanner. The controller is a small embedded chip with almost no spare memory. It can rearrange the list it already has, but it can't build anything else of any size.

## The problem

You're given a list of whole numbers in any order. Find the smallest positive whole number that isn't in the list. You must do it in time proportional to the length of the list, using only a fixed amount of extra memory.

For `3 4 −1 1`, 1 is present and 2 is missing, so the answer is 2. For `7 8 9 11 12`, the answer is 1.

## The question it asks

"Is this key present?", asked for 1, then 2, then 3. That's a [hash table](../../dsa/hash-tables.md) question, but with no memory for a hash table. See the find-by-key row in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Put every number in a hash set, then check 1, 2, 3 and so on until one is missing. It's linear in time and obviously right, and it's how you'd do it on a server. But the set needs memory in proportion to the list, which the controller doesn't have.

The other natural idea is to sort the list and walk along it looking for the first gap. That needs no extra memory if you sort in place, but sorting takes time in proportion to *n* log *n* ([sorting](../../dsa/sorting.md)), which breaks the time limit.

## Hints

<details markdown="1"><summary>Hint 1</summary>

If the list has *n* numbers, the answer is somewhere between 1 and *n* + 1. Numbers below 1 or above *n* can't affect it at all.

</details>

<details markdown="1"><summary>Hint 2</summary>

There are exactly *n* slots in the list and *n* numbers that matter, 1 to *n*. What if each number lived in the slot of its own value: 1 in the first slot, 2 in the second, and so on?

</details>

<details markdown="1"><summary>Hint 3</summary>

Moving a number to its own slot can be done with a swap, and the number that comes back may itself need moving. How many times can any one number be moved into its own slot?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Use the list itself as the hash table, with the simplest possible hash: number *v* belongs at position *v* − 1.

1. **Put every useful number in its own slot.** Go through the positions in order. While the number at the current position is between 1 and *n*, and its own slot doesn't already hold the same number, swap it into its own slot. The number that arrives in exchange is then considered in the same way. Numbers outside 1 to *n*, and duplicates whose slot is already taken by an equal number, are left where they land.
2. **Find the first slot that doesn't hold its own number.** If position *i* doesn't hold *i* + 1, then *i* + 1 is missing. If every slot holds its own number, the answer is *n* + 1.

**Why it's linear:** each swap puts at least one number into its own slot for good, and there are at most *n* such numbers, so there are at most *n* swaps in the whole run, however the work is spread across the positions. The inner loop looks expensive and is [amortised](../../dsa/amortised-cost.md) to a constant per position.

**Why the duplicate check matters:** without "its own slot doesn't already hold the same number", a list like `1 1` swaps the two 1s back and forth forever.

**Time:** proportional to *n*. **Memory:** a fixed amount beyond the list, which is rearranged.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        # Use the list itself as the table: number v belongs at position v - 1.
        for i in range(n):
            # Keep swapping until this slot holds something that can't be placed,
            # or already sits where it belongs.
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                home = nums[i] - 1
                nums[i], nums[home] = nums[home], nums[i]
        # The first slot not holding its own number marks the gap.
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        // Use the list itself as the table: number v belongs at position v - 1.
        for (int i = 0; i < n; i++) {
            // Keep swapping until this slot holds something that can't be placed,
            // or already sits where it belongs.
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                swap(nums[i], nums[nums[i] - 1]);
            }
        }
        // The first slot not holding its own number marks the gap.
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    public int firstMissingPositive(int[] nums) {
        int n = nums.length;
        // Use the array itself as the table: number v belongs at position v - 1.
        for (int i = 0; i < n; i++) {
            // Keep swapping until this slot holds something that can't be placed,
            // or already sits where it belongs.
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                int home = nums[i] - 1;
                int moved = nums[home];
                nums[home] = nums[i];
                nums[i] = moved;
            }
        }
        // The first slot not holding its own number marks the gap.
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func firstMissingPositive(nums []int) int {
	n := len(nums)
	// Use the slice itself as the table: number v belongs at position v - 1.
	for i := 0; i < n; i++ {
		// Keep swapping until this slot holds something that can't be placed,
		// or already sits where it belongs.
		for nums[i] >= 1 && nums[i] <= n && nums[nums[i]-1] != nums[i] {
			home := nums[i] - 1
			nums[i], nums[home] = nums[home], nums[i]
		}
	}
	// The first slot not holding its own number marks the gap.
	for i := 0; i < n; i++ {
		if nums[i] != i+1 {
			return i + 1
		}
	}
	return n + 1
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn first_missing_positive(mut nums: Vec<i32>) -> i32 {
        let n = nums.len();
        // Use the vector itself as the table: number v belongs at position v - 1.
        for i in 0..n {
            // Keep swapping until this slot holds something that can't be placed,
            // or already sits where it belongs.
            while nums[i] >= 1 && (nums[i] as usize) <= n && nums[nums[i] as usize - 1] != nums[i] {
                let home = nums[i] as usize - 1;
                nums.swap(i, home);
            }
        }
        // The first slot not holding its own number marks the gap.
        for i in 0..n {
            if nums[i] != i as i32 + 1 {
                return i as i32 + 1;
            }
        }
        n as i32 + 1
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Looping forever on duplicates.** Check the destination slot's value, not just whether the current number is in range.
- **Advancing past a slot after one swap.** The number swapped in may also need to move; keep going until the current slot is settled.
- **Off-by-one between values and positions.** Value *v* goes to position *v* − 1, and position *i* should hold *i* + 1.
- **Forgetting the case where everything is present.** Then the answer is *n* + 1, not *n*.
- **Changing the caller's list unexpectedly.** The method rearranges its input; in real code, say so or work on a copy.

## Related

- The other exercise in this category: [the shortest crash signature](minimum-window-substring.md) (LeetCode 76).
- Concept pages: [hash tables](../../dsa/hash-tables.md), [hashing](../../dsa/hashing.md), [sorting](../../dsa/sorting.md), [amortised cost](../../dsa/amortised-cost.md).
- More practice of the same shape: problems tagged "cyclic sort" or using an array as its own index.
