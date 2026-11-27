# The last balloon

An exercise in the category **overlapping questions**. It's LeetCode 312, [Burst Balloons](https://leetcode.com/problems/burst-balloons/), rated Hard.

## The situation

A company that demolishes old industrial buildings brings each one down a section at a time. Removing a section shakes its two standing neighbours, and the contract pays a bonus on each removal that grows with the size of the section and of the two neighbours still standing on either side, because those are the hardest removals to do safely. The planners want the order of removals that earns the most. A building can have a few hundred sections, and the planners need the answer before they quote.

The puzzle is usually told with balloons, and the code uses that version.

## The problem

You're given a row of balloons, each with a number. Bursting balloon *i* earns `left × nums[i] × right`, where *left* and *right* are the numbers of its nearest neighbours still unburst, or 1 if there's no neighbour on that side. After it bursts, its neighbours become next to each other. Burst every balloon. Return the most you can earn.

For `3 1 5 8`, the best order earns 167: burst 1 (3 × 1 × 5 = 15), then 5 (3 × 5 × 8 = 120), then 3 (1 × 3 × 8 = 24), then 8 (1 × 8 × 1 = 8).

## The question it asks

"What's the best I can do with this stretch?", asked about the same stretches over and over, from different orders. That's overlapping questions, which is what [dynamic programming](../../dsa/dynamic-programming.md) answers. See the row for overlapping questions in [choosing a data structure](../../dsa/choosing.md). The difficulty is finding a question whose answers really can be reused.

## The tempting first answer

Try every order: *n* choices for the first balloon, *n* − 1 for the second, and so on. That's *n*! orders, and for twenty balloons it's more than two billion billion ([growth](../../dsa/growth.md)).

The tempting fix is to pick which balloon to burst **first**, then solve what's left on each side. But after the first burst, the two sides aren't separate: the balloons at the edge of each side are now neighbours of each other, so what you earn on one side depends on the order on the other. The subproblems overlap in the wrong way, and the table never fills.

A [greedy](../../dsa/greedy.md) rule, such as always bursting the smallest balloon, is quick and often close, and it's wrong.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Choosing the first balloon to burst leaves two sides that interfere with each other. Is there a choice that leaves two sides which can't interfere?

</details>

<details markdown="1"><summary>Hint 2</summary>

Choose the balloon to burst **last** in a stretch. Until then it stands between the two sides like a wall, so the left side's bursts never see the right side's balloons.

</details>

<details markdown="1"><summary>Hint 3</summary>

Put a balloon worth 1 at each end that's never burst. Let `best[lo][hi]` be the most you can earn by bursting everything strictly between *lo* and *hi*, while both are still standing. If *k* is the last balloon burst between them, what does it earn, and what's left to solve?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

1. **Add the edges.** Put a 1 at each end of the row. These two are never burst.
2. **Define the question.** `best[lo][hi]` is the most you can earn by bursting every balloon strictly between positions *lo* and *hi*, with *lo* and *hi* themselves still standing.
3. **Choose the last balloon.** If *k* is burst last among them, then when it bursts its neighbours are *lo* and *hi*, so it earns `v[lo] × v[k] × v[hi]`. Before that, the balloons between *lo* and *k* were burst with *k* standing as a wall, and so were those between *k* and *hi*. So

   `best[lo][hi] = max over k of best[lo][k] + v[lo] × v[k] × v[hi] + best[k][hi]`.

4. **Fill by width.** Short stretches first, so every entry you need is already there. The answer is `best[0][n + 1]`.

**Why "last" works and "first" doesn't:** a good subproblem has to be independent of everything outside it. Choosing the first balloon creates new neighbours that cross between the sides. Choosing the last one fixes the neighbours of both sides for the whole time they're being burst. This turning-round, asking what happens last instead of first, is a move worth keeping: it turns up whenever the obvious split leaves its parts entangled.

**Time:** proportional to *n*³: about *n*² stretches, each trying up to *n* last balloons. For 300 balloons that's about 4.5 million steps. **Memory:** proportional to *n*².

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        # Pretend there's a balloon worth 1 at each end that can't be burst.
        v = [1] + nums + [1]
        n = len(v)
        # best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
        # while lo and hi themselves are still standing.
        best = [[0] * n for _ in range(n)]
        for width in range(2, n):
            for lo in range(n - width):
                hi = lo + width
                # Choose the balloon k to burst LAST in this stretch: by then its
                # neighbours are lo and hi, and the two sides were settled independently.
                best[lo][hi] = max(
                    best[lo][k] + v[lo] * v[k] * v[hi] + best[k][hi] for k in range(lo + 1, hi)
                )
        return best[0][n - 1]
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int maxCoins(vector<int>& nums) {
        // Pretend there's a balloon worth 1 at each end that can't be burst.
        vector<int> v = {1};
        v.insert(v.end(), nums.begin(), nums.end());
        v.push_back(1);
        int n = v.size();
        // best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
        // while lo and hi themselves are still standing.
        vector<vector<int>> best(n, vector<int>(n, 0));
        for (int width = 2; width < n; width++) {
            for (int lo = 0; lo + width < n; lo++) {
                int hi = lo + width;
                // Choose the balloon k to burst LAST in this stretch: by then its
                // neighbours are lo and hi, and the two sides were settled independently.
                for (int k = lo + 1; k < hi; k++) {
                    best[lo][hi] = max(best[lo][hi], best[lo][k] + v[lo] * v[k] * v[hi] + best[k][hi]);
                }
            }
        }
        return best[0][n - 1];
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    public int maxCoins(int[] nums) {
        // Pretend there's a balloon worth 1 at each end that can't be burst.
        int n = nums.length + 2;
        int[] v = new int[n];
        v[0] = v[n - 1] = 1;
        System.arraycopy(nums, 0, v, 1, nums.length);
        // best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
        // while lo and hi themselves are still standing.
        int[][] best = new int[n][n];
        for (int width = 2; width < n; width++) {
            for (int lo = 0; lo + width < n; lo++) {
                int hi = lo + width;
                // Choose the balloon k to burst LAST in this stretch: by then its
                // neighbours are lo and hi, and the two sides were settled independently.
                for (int k = lo + 1; k < hi; k++) {
                    best[lo][hi] = Math.max(best[lo][hi], best[lo][k] + v[lo] * v[k] * v[hi] + best[k][hi]);
                }
            }
        }
        return best[0][n - 1];
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func maxCoins(nums []int) int {
	// Pretend there's a balloon worth 1 at each end that can't be burst.
	v := append(append([]int{1}, nums...), 1)
	n := len(v)
	// best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
	// while lo and hi themselves are still standing.
	best := make([][]int, n)
	for i := range best {
		best[i] = make([]int, n)
	}
	for width := 2; width < n; width++ {
		for lo := 0; lo+width < n; lo++ {
			hi := lo + width
			// Choose the balloon k to burst LAST in this stretch: by then its
			// neighbours are lo and hi, and the two sides were settled independently.
			for k := lo + 1; k < hi; k++ {
				best[lo][hi] = max(best[lo][hi], best[lo][k]+v[lo]*v[k]*v[hi]+best[k][hi])
			}
		}
	}
	return best[0][n-1]
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn max_coins(nums: Vec<i32>) -> i32 {
        // Pretend there's a balloon worth 1 at each end that can't be burst.
        let mut v = vec![1];
        v.extend(nums);
        v.push(1);
        let n = v.len();
        // best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
        // while lo and hi themselves are still standing.
        let mut best = vec![vec![0i32; n]; n];
        for width in 2..n {
            for lo in 0..n - width {
                let hi = lo + width;
                // Choose the balloon k to burst LAST in this stretch: by then its
                // neighbours are lo and hi, and the two sides were settled independently.
                for k in lo + 1..hi {
                    best[lo][hi] = best[lo][hi].max(best[lo][k] + v[lo] * v[k] * v[hi] + best[k][hi]);
                }
            }
        }
        best[0][n - 1]
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Choosing the first balloon to burst.** The two sides then share neighbours, and the answers can't be reused.
- **Forgetting the edges.** Without a 1 at each end, the formula needs special cases for the first and last balloons.
- **Filling the table in the wrong order.** Each entry needs shorter stretches inside it; fill by increasing width.
- **Treating balloons worth 0 specially.** They need no special case; they just earn nothing when burst, and multiply their neighbours' earnings by 0 while standing.

## Related

- The other exercise in this category: [the marker in the sequence](distinct-subsequences.md) (LeetCode 115).
- Concept pages: [dynamic programming](../../dsa/dynamic-programming.md), [greedy algorithms](../../dsa/greedy.md), [divide and conquer](../../dsa/divide-and-conquer.md), [growth](../../dsa/growth.md).
- More practice of the same shape: problems tagged "interval DP", such as the cheapest order to multiply a chain of matrices, or the cheapest way to cut a stick at given marks.
