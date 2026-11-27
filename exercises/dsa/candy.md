# The stickers on the chart

An exercise in the category **the best step now**. It's LeetCode 135, [Candy](https://leetcode.com/problems/candy/), rated Hard.

## The situation

A primary school teacher gives out stickers at the end of each week. The children sit in a row, and each has a score for the week. Every child gets at least one sticker, and any child who scored higher than a neighbour in the row must get more stickers than that neighbour, because the children check. Stickers cost money, and the school buys them for the whole year, so the teacher wants the fewest that keep everyone's rules.

## The problem

You're given a list of ratings for children standing in a line. Give each child some candies so that every child gets at least one, and every child with a higher rating than an immediate neighbour gets more candies than that neighbour. Return the smallest total.

For ratings `1 0 2`, the answer is 5: give 2, 1 and 2.

## The question it asks

"What's the least this child can have, given their neighbours?" Each child's number depends only on the runs of rising ratings that lead up to them from each side. A rule that fixes each child at the smallest value it can have, without ever needing to undo it, is the best step now: a [greedy algorithm](../../dsa/greedy.md). See the row for the best step now in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Give everyone one candy, then sweep the line repeatedly, giving one more than the neighbour to every child who is rated above a neighbour but doesn't have more candies. Repeat until a sweep changes nothing. It's correct, and it converges, but a long falling run fixes only one more child per sweep, so it can take as many sweeps as there are children ([growth](../../dsa/growth.md)).

The other tempting answer is a single left-to-right pass: one more than the left neighbour when rising, one otherwise. It's fast and it handles every rising run. It fails on falling runs, where a child must have more than the child to their **right**, which hasn't been decided yet.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Each child has two separate rules: one about the left neighbour and one about the right. Can you satisfy them one at a time?

</details>

<details markdown="1"><summary>Hint 2</summary>

A left-to-right pass satisfies every "more than my left neighbour" rule with the fewest candies. A right-to-left pass could do the same for right neighbours. How do you combine the two without breaking the first?

</details>

<details markdown="1"><summary>Hint 3</summary>

In the second pass, only ever raise a child's count, to one more than the right neighbour's, if it isn't already that high. Why can raising never break a rule the first pass satisfied?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

1. **Give everyone 1.**
2. **Left to right:** if a child's rating is higher than the left neighbour's, give them one more than the left neighbour has.
3. **Right to left:** if a child's rating is higher than the right neighbour's, raise them to one more than the right neighbour has, unless they already have at least that.
4. **Return the total.**

**Why it's the fewest:** after the first pass, each child has exactly the length of the rising run that ends at them from the left, which is the least any arrangement can give them for the left rule. The second pass does the same from the right, and each child ends with the larger of the two, which is the least that satisfies both. Nobody gets more than a rule forces.

**Why the second pass doesn't break the first:** it only raises counts, and only for a child rated above their right neighbour. Raising child *i* could only break a rule that says *i* + 1 must have more than *i*, and that rule exists only if *i* + 1 is rated higher, which is the opposite of why *i* was raised. And *i*'s own rule against their left neighbour still holds, because *i* only went up.

**Time:** proportional to *n*. **Memory:** proportional to *n*, or a fixed amount with a cleverer single pass that counts the lengths of rising and falling runs.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        give = [1] * n   # everyone gets at least one
        # Left to right: anyone rated above their left neighbour gets one more than them.
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                give[i] = give[i - 1] + 1
        # Right to left: the same for right neighbours, without undoing the first pass.
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                give[i] = max(give[i], give[i + 1] + 1)
        return sum(give)
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> give(n, 1);  // everyone gets at least one
        // Left to right: anyone rated above their left neighbour gets one more than them.
        for (int i = 1; i < n; i++)
            if (ratings[i] > ratings[i - 1]) give[i] = give[i - 1] + 1;
        // Right to left: the same for right neighbours, without undoing the first pass.
        for (int i = n - 2; i >= 0; i--)
            if (ratings[i] > ratings[i + 1]) give[i] = max(give[i], give[i + 1] + 1);
        return accumulate(give.begin(), give.end(), 0);
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.Arrays;

class Solution {
    public int candy(int[] ratings) {
        int n = ratings.length;
        int[] give = new int[n];
        Arrays.fill(give, 1);  // everyone gets at least one
        // Left to right: anyone rated above their left neighbour gets one more than them.
        for (int i = 1; i < n; i++)
            if (ratings[i] > ratings[i - 1]) give[i] = give[i - 1] + 1;
        // Right to left: the same for right neighbours, without undoing the first pass.
        for (int i = n - 2; i >= 0; i--)
            if (ratings[i] > ratings[i + 1]) give[i] = Math.max(give[i], give[i + 1] + 1);
        int total = 0;
        for (int g : give) total += g;
        return total;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func candy(ratings []int) int {
	n := len(ratings)
	give := make([]int, n)
	for i := range give {
		give[i] = 1 // everyone gets at least one
	}
	// Left to right: anyone rated above their left neighbour gets one more than them.
	for i := 1; i < n; i++ {
		if ratings[i] > ratings[i-1] {
			give[i] = give[i-1] + 1
		}
	}
	// Right to left: the same for right neighbours, without undoing the first pass.
	for i := n - 2; i >= 0; i-- {
		if ratings[i] > ratings[i+1] {
			give[i] = max(give[i], give[i+1]+1)
		}
	}
	total := 0
	for _, g := range give {
		total += g
	}
	return total
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn candy(ratings: Vec<i32>) -> i32 {
        let n = ratings.len();
        let mut give = vec![1; n]; // everyone gets at least one
        // Left to right: anyone rated above their left neighbour gets one more than them.
        for i in 1..n {
            if ratings[i] > ratings[i - 1] {
                give[i] = give[i - 1] + 1;
            }
        }
        // Right to left: the same for right neighbours, without undoing the first pass.
        for i in (0..n.saturating_sub(1)).rev() {
            if ratings[i] > ratings[i + 1] {
                give[i] = give[i].max(give[i + 1] + 1);
            }
        }
        give.iter().sum()
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **One pass only.** Falling runs need the second pass from the right.
- **Overwriting in the second pass.** Take the larger of the two counts; setting it to the right-hand value can break a left rule.
- **Giving more to equal neighbours.** Equal ratings have no rule between them; `1 2 2` needs 4 candies, not 6.
- **Assuming the peak is simple.** A peak needs more than both slopes beside it, so it's the larger of the two run lengths, not their sum.

## Related

- The other exercise in this category: Course Schedule III (LeetCode 630), coming in a later batch.
- Concept pages: [greedy algorithms](../../dsa/greedy.md), [growth](../../dsa/growth.md).
- More practice of the same shape: problems tagged "two passes", such as trapping rain water between bars, where each position also depends on the best to its left and to its right.
