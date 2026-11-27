# The marker in the sequence

An exercise in the category **overlapping questions**. It's LeetCode 115, [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/), rated Hard.

## The situation

A lab studying a gene looks for a short marker sequence inside long stretches of DNA, read as letters. The marker doesn't have to appear in one piece: the biologists are interested in every way its letters can be picked out in order from the longer stretch, skipping letters in between, because each way is a different possible alignment. For each stretch, they want to know how many alignments there are. The stretches are a thousand letters long, and there are millions of them.

## The problem

You're given two strings, *s* and *t*. Count the number of ways to delete some of the characters of *s*, keeping the rest in order, so that what remains is exactly *t*. Two ways are different if they keep different positions of *s*. The answer fits in a 32-bit integer.

For `rabbbit` and `rabbit`, the answer is 3: any one of the three b's can be the one left out.

## The question it asks

"In how many ways does this part of *s* contain this part of *t*?" The same question, for the same pair of prefixes, comes up again and again along different routes. That's overlapping questions, which is what [dynamic programming](../../dsa/dynamic-programming.md) answers. See the row for overlapping questions in [choosing a data structure](../../dsa/choosing.md). It's a close relative of the comparison behind `diff`, in the story on that page.

## The tempting first answer

Try every way of picking positions: for each character of *s*, keep it or skip it, and at the end check whether what's kept is *t*. That's 2^1000 choices for a thousand-letter stretch ([growth](../../dsa/growth.md)). Matching as you go, so you stop when a kept letter is wrong, helps a lot and is still exponential: in a stretch of a thousand a's, looking for twenty a's, every route succeeds and there are astronomically many of them to walk.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Look at the first character of *s*. Either it isn't used, and you need the ways for the rest of *s* and all of *t*; or, if it equals the first character of *t*, it's used, and you need the ways for the rest of *s* and the rest of *t*. How many different (rest of *s*, rest of *t*) questions can there be?

</details>

<details markdown="1"><summary>Hint 2</summary>

There are only (length of *s* + 1) × (length of *t* + 1). Answer each once. Read *s* from left to right, and keep, for each prefix of *t*, the number of ways the part of *s* read so far contains it.

</details>

<details markdown="1"><summary>Hint 3</summary>

When the next character of *s* is *c*, every way of making `t[:j−1]` can be finished by this *c* if `t[j−1]` is *c*. Update the counts so that one character of *s* isn't used twice in the same way.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Keep one row of counts, `ways[j]`: the number of ways the part of *s* read so far contains the first *j* characters of *t*.

1. **Start** with `ways[0] = 1` (the empty prefix of *t*, made by keeping nothing) and every other entry 0.
2. **For each character *c* of *s*,** go through *j* from the end of *t* down to 1. If `t[j − 1]` is *c*, add `ways[j − 1]` to `ways[j]`: every way of making the shorter prefix can be finished with this *c*.
3. **The answer** is `ways[len(t)]`.

**Why right to left:** each update reads the entry to its left. Going right to left means it reads the value from before this character of *s* was considered, so the same character can't be used for two letters of *t* in one way. Going left to right would let `aa` appear in `a`.

**Why one row is enough:** the full table has a row per prefix of *s*, but each row is built only from the one before it. Overwriting one row in the right order keeps the memory down to the length of *t*.

**About overflow:** the final count fits in 32 bits, but counts for shorter prefixes of *t* can be far larger: in a thousand a's, the number of ways to pick five hundred is a 300-digit number. The code uses unsigned 64-bit arithmetic, which wraps around instead of failing. Every count is then correct modulo 2⁶⁴, and since the true answer is less than 2³¹, it comes out exactly right. Python's integers simply grow.

**Time:** proportional to the length of *s* × the length of *t*. **Memory:** proportional to the length of *t*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        # ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
        ways = [1] + [0] * len(t)   # the empty prefix of t, in exactly one way
        for ch in s:
            # Go right to left, so each character of s is used at most once per way.
            for j in range(len(t), 0, -1):
                if t[j - 1] == ch:
                    ways[j] += ways[j - 1]   # every way to make t[:j-1], finished with this ch
        return ways[len(t)]
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        // ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
        // Unsigned arithmetic wraps instead of overflowing; the final answer fits in 32 bits,
        // and wrapping keeps every count correct modulo 2^64, so the answer comes out right.
        vector<unsigned long long> ways(t.size() + 1, 0);
        ways[0] = 1;  // the empty prefix of t, in exactly one way
        for (char ch : s) {
            // Go right to left, so each character of s is used at most once per way.
            for (size_t j = t.size(); j >= 1; j--) {
                if (t[j - 1] == ch) ways[j] += ways[j - 1];
            }
        }
        return (int)ways[t.size()];
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    public int numDistinct(String s, String t) {
        int m = t.length();
        // ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
        // Java's long wraps on overflow; the final answer fits in 32 bits, and wrapping keeps
        // every count correct modulo 2^64, so the answer comes out right.
        long[] ways = new long[m + 1];
        ways[0] = 1;  // the empty prefix of t, in exactly one way
        for (char ch : s.toCharArray()) {
            // Go right to left, so each character of s is used at most once per way.
            for (int j = m; j >= 1; j--) {
                if (t.charAt(j - 1) == ch) ways[j] += ways[j - 1];
            }
        }
        return (int) ways[m];
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func numDistinct(s string, t string) int {
	m := len(t)
	// ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
	// uint64 wraps on overflow; the final answer fits in 32 bits, and wrapping keeps
	// every count correct modulo 2^64, so the answer comes out right.
	ways := make([]uint64, m+1)
	ways[0] = 1 // the empty prefix of t, in exactly one way
	for i := 0; i < len(s); i++ {
		// Go right to left, so each character of s is used at most once per way.
		for j := m; j >= 1; j-- {
			if t[j-1] == s[i] {
				ways[j] += ways[j-1]
			}
		}
	}
	return int(ways[m])
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn num_distinct(s: String, t: String) -> i32 {
        let (s, t) = (s.as_bytes(), t.as_bytes());
        let m = t.len();
        // ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
        // Wrapping addition can't panic; the final answer fits in 32 bits, and wrapping keeps
        // every count correct modulo 2^64, so the answer comes out right.
        let mut ways = vec![0u64; m + 1];
        ways[0] = 1; // the empty prefix of t, in exactly one way
        for &ch in s {
            // Go right to left, so each character of s is used at most once per way.
            for j in (1..=m).rev() {
                if t[j - 1] == ch {
                    ways[j] = ways[j].wrapping_add(ways[j - 1]);
                }
            }
        }
        ways[m] as i32
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Updating left to right with one row.** It reuses a character of *s* within a single way; go right to left, or keep two rows.
- **Signed overflow.** Shorter prefixes' counts can overflow even 64 bits. In C++ that's undefined behaviour for signed integers; use unsigned, or arithmetic that wraps.
- **Forgetting the empty prefix.** `ways[0]` is 1, not 0, or nothing ever gets counted.
- **Counting distinct strings instead of distinct choices of position.** The three answers for `rabbbit` all spell the same word; they count separately because they keep different b's.

## Related

- The other exercise in this category: [the last balloon](burst-balloons.md) (LeetCode 312).
- Concept pages: [dynamic programming](../../dsa/dynamic-programming.md), [growth](../../dsa/growth.md).
- More practice of the same shape: the edit distance between two words, and the longest common subsequence, the comparison behind `diff`.
