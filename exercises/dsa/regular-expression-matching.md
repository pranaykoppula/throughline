# The rule that took the afternoon

An exercise in the category **which state, what next**. It's LeetCode 10, [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/), rated Hard.

## The situation

A company's support system routes incoming tickets by matching their reference codes against patterns the support leads write, such as `INV.*` for invoices or `RET-a*b` for a family of returns codes. The leads only need two special signs: `.` for any one character, and `*` for "the thing before me, any number of times, including none". The first version tried each way of matching in turn and went back when one failed. It worked until a lead wrote a pattern with several stars in a row, and one unlucky ticket held a matching server for most of an afternoon. The team wants a matcher whose time they can predict before it runs.

## The problem

You're given a string and a pattern. The pattern contains letters, `.` (matches any single character) and `*` (matches zero or more of the element just before it). Return whether the pattern matches the *whole* string, not just part of it.

`aa` doesn't match `a`, because the pattern covers only one character. `aa` matches `a*`, `ab` matches `.*`, and `aab` matches `c*a*b`, because `c*` can match nothing.

## The question it asks

"Given where I've got to in the text, which places in the pattern could I be at?" That's a [state machine](../../dsa/state-machines.md) question: each position in the pattern is a state, and each `*` adds a loop. See the row for which state, what next in [choosing a data structure](../../dsa/choosing.md). Because one place in the text can correspond to several places in the pattern, the honest answer is a set of states, or a table of them, rather than a single path.

## The tempting first answer

Match greedily, and when you meet `x*`, try using it for none, one, two or more characters in turn, recursing on the rest and going back when a choice fails. It's short and it's correct. It's also the backtracking engine from [power and predictability](../../dsa/power-and-predictability.md): on `aaaaaaaaaaaaaaaaaaab` against `a*a*a*a*a*a*a*a*a*c`, it tries every way of sharing the a's between the stars before giving up, and the number of ways grows exponentially with the length ([growth](../../dsa/growth.md)).

## Hints

<details markdown="1"><summary>Hint 1</summary>

The backtracking answer keeps asking the same question: "does the text from position *i* match the pattern from position *j*?" How many different questions of that kind are there?

</details>

<details markdown="1"><summary>Hint 2</summary>

There are only (length of text + 1) × (length of pattern + 1) of them. Answer each once and store it. What does the answer for (*i*, *j*) depend on?

</details>

<details markdown="1"><summary>Hint 3</summary>

If the pattern element at *j* is followed by `*`, you can skip the pair entirely (go to *j* + 2), or, if the element matches the character at *i*, use it once and stay where you are in the pattern (go to *i* + 1, *j*). Otherwise the element must match the character at *i*, and both move on.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Fill a table `can[i][j]`: does the text from position *i* match the pattern from position *j*? Work from the ends backwards, so every entry you need is already filled.

1. **The corner:** `can[m][n]` is true, where *m* and *n* are the lengths. An empty text matches an empty pattern.
2. **For every other entry,** let `first` be whether there's a character at *i* and the pattern element at *j* is that character or `.`.
   - **If the element at *j* has a `*` after it:** `can[i][j] = can[i][j + 2]` (use the pair for nothing) **or** `first and can[i + 1][j]` (use it for this character, and stay on the pair for more).
   - **Otherwise:** `can[i][j] = first and can[i + 1][j + 1]`.
3. **The answer** is `can[0][0]`.

**Why it's predictable:** backtracking answers the same (*i*, *j*) question again and again, once for every route that reaches it. The table answers each one once. That's [dynamic programming](../../dsa/dynamic-programming.md), and it's also the state machine view: a column of the table is the set of pattern positions you could be at, which is what a linear-time regular-expression engine tracks as it reads the text.

**Why the stars stay simple:** "use it once and stay on it" means a star never has to guess how many characters to take. It takes one at a time, and the table remembers the results.

**Time:** proportional to the text's length × the pattern's length. **Memory:** the same, or one row if you keep only the row below.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        # can[i][j]: does the text from position i match the pattern from position j?
        can = [[False] * (n + 1) for _ in range(m + 1)]
        can[m][n] = True   # nothing left of either: a match
        for i in range(m, -1, -1):
            for j in range(n - 1, -1, -1):
                first = i < m and p[j] in (s[i], ".")
                if j + 1 < n and p[j + 1] == "*":
                    # Skip "x*" entirely, or use it for one character and stay on it.
                    can[i][j] = can[i][j + 2] or (first and can[i + 1][j])
                else:
                    can[i][j] = first and can[i + 1][j + 1]
        return can[0][0]
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.size(), n = p.size();
        // can[i][j]: does the text from position i match the pattern from position j?
        vector<vector<bool>> can(m + 1, vector<bool>(n + 1, false));
        can[m][n] = true;  // nothing left of either: a match
        for (int i = m; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                bool first = i < m && (p[j] == s[i] || p[j] == '.');
                if (j + 1 < n && p[j + 1] == '*') {
                    // Skip "x*" entirely, or use it for one character and stay on it.
                    can[i][j] = can[i][j + 2] || (first && can[i + 1][j]);
                } else {
                    can[i][j] = first && can[i + 1][j + 1];
                }
            }
        }
        return can[0][0];
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    public boolean isMatch(String s, String p) {
        int m = s.length(), n = p.length();
        // can[i][j]: does the text from position i match the pattern from position j?
        boolean[][] can = new boolean[m + 1][n + 1];
        can[m][n] = true;  // nothing left of either: a match
        for (int i = m; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                boolean first = i < m && (p.charAt(j) == s.charAt(i) || p.charAt(j) == '.');
                if (j + 1 < n && p.charAt(j + 1) == '*') {
                    // Skip "x*" entirely, or use it for one character and stay on it.
                    can[i][j] = can[i][j + 2] || (first && can[i + 1][j]);
                } else {
                    can[i][j] = first && can[i + 1][j + 1];
                }
            }
        }
        return can[0][0];
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func isMatch(s string, p string) bool {
	m, n := len(s), len(p)
	// can[i][j]: does the text from position i match the pattern from position j?
	can := make([][]bool, m+1)
	for i := range can {
		can[i] = make([]bool, n+1)
	}
	can[m][n] = true // nothing left of either: a match
	for i := m; i >= 0; i-- {
		for j := n - 1; j >= 0; j-- {
			first := i < m && (p[j] == s[i] || p[j] == '.')
			if j+1 < n && p[j+1] == '*' {
				// Skip "x*" entirely, or use it for one character and stay on it.
				can[i][j] = can[i][j+2] || (first && can[i+1][j])
			} else {
				can[i][j] = first && can[i+1][j+1]
			}
		}
	}
	return can[0][0]
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn is_match(s: String, p: String) -> bool {
        let (s, p) = (s.as_bytes(), p.as_bytes());
        let (m, n) = (s.len(), p.len());
        // can[i][j]: does the text from position i match the pattern from position j?
        let mut can = vec![vec![false; n + 1]; m + 1];
        can[m][n] = true; // nothing left of either: a match
        for i in (0..=m).rev() {
            for j in (0..n).rev() {
                let first = i < m && (p[j] == s[i] || p[j] == b'.');
                if j + 1 < n && p[j + 1] == b'*' {
                    // Skip "x*" entirely, or use it for one character and stay on it.
                    can[i][j] = can[i][j + 2] || (first && can[i + 1][j]);
                } else {
                    can[i][j] = first && can[i + 1][j + 1];
                }
            }
        }
        can[0][0]
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Matching only part of the text.** The pattern must cover all of it; `can[m][n]` is the only empty-text case that starts true.
- **Forgetting that a star can match nothing.** `c*a*b` matches `aab`; the `c*` pair has to be skippable even when there's no text left.
- **Treating `*` as a wildcard on its own.** Here it always repeats the element before it; `.*` is "anything", `*` alone isn't.
- **Reading past the end of the text.** `first` must check that there's a character at *i* before comparing.

## Related

- The other exercise in this category: [the price column](valid-number.md) (LeetCode 65).
- Concept pages: [power and predictability](../../dsa/power-and-predictability.md), [state machines](../../dsa/state-machines.md), [dynamic programming](../../dsa/dynamic-programming.md), [growth](../../dsa/growth.md).
- More practice of the same shape: wildcard matching with `?` and `*`, where `*` matches any run of characters on its own.
