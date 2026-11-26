# The shortest crash signature

An exercise in the category **find by key**. It's LeetCode 76, [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/), rated Hard.

## The situation

A home-router maker's support team has learned that a particular crash follows a recognisable pattern of events in the device's log: two power dips, a firmware check and a radio reset, in any order and with anything in between. Each router keeps a long log of single-letter event codes. When a customer reports a crash, the engineer wants the shortest stretch of that log containing the whole signature, counting repeats, because that's the stretch most likely to show what actually went wrong. Logs run to tens of thousands of events.

## The problem

You're given a long string *s* and a shorter string *t*. Find the shortest run of consecutive characters in *s* that contains every character of *t*, including repeated characters as many times as they appear in *t*. If there's no such run, return an empty string. Upper and lower case count as different characters.

For *s* = `ADOBECODEBANC` and *t* = `ABC`, the shortest run containing an A, a B and a C is `BANC`.

## The question it asks

"How many of each key do I still need?", asked after every step. Counting by key is a [hash table](../../dsa/hash-tables.md) question, and the counts change as a window slides over the log. See the find-by-key row in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Try every starting point, and from each one extend to the right until the run contains the whole signature, keeping the shortest. Checking whether a run contains the signature means comparing counts, and with every start and every end, the work grows with the square of the log's length ([growth](../../dsa/growth.md)). For a log of 30,000 events, that's hundreds of millions of steps, for a question asked about a single crash.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Suppose the run from position *i* to position *j* contains the signature. Then so does every longer run that starts at *i*. And the shortest run starting at *i* + 1 can't end before *j*.

</details>

<details markdown="1"><summary>Hint 2</summary>

So both ends of the window only ever need to move right. Grow the right end until the window contains the signature, then shrink the left end while it still does.

</details>

<details markdown="1"><summary>Hint 3</summary>

Checking "does the window contain the signature?" by comparing every count is slow. Keep one number instead: how many of the signature's characters, counting repeats, the window is still missing. When does it go up, and when does it go down?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Keep a count of what the window still needs: start with the count of each character in *t*, and a single number, `missing`, equal to the length of *t*.

1. **Move the right end one step.** For the new character, if it was still needed (its count is above zero), it reduces `missing` by one. Either way, decrease its count. A count below zero means the window has spare copies.
2. **While nothing is missing, shrink from the left.** Record the window if it's the shortest so far. Then remove the leftmost character: increase its count, and if that count rises above zero, the window now lacks it, so `missing` goes up by one and the shrinking stops.
3. **Repeat until the right end reaches the end of *s*.**

The counts work as a small hash table from character to "still needed". Because characters are a small fixed set, an array of 128 counts is enough and faster than a general map.

**Why it's linear:** each end of the window only moves right, so each character enters the window once and leaves once. Checking whether the window is complete is a single comparison of `missing` with zero, not a comparison of every count.

**Time:** proportional to the lengths of *s* and *t*. **Memory:** a fixed table of counts.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)          # how many of each event the window still needs
        missing = len(t)           # total events still needed, repeats included
        best_start, best_len = 0, len(s) + 1
        left = 0
        for right, ch in enumerate(s):
            # Taking in one more event.
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1
            # While the window has everything, shrink it from the left.
            while missing == 0:
                if right - left + 1 < best_len:
                    best_start, best_len = left, right - left + 1
                gone = s[left]
                need[gone] += 1
                if need[gone] > 0:
                    missing += 1
                left += 1
        return s[best_start:best_start + best_len] if best_len <= len(s) else ""
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        // How many of each event the window still needs; negative means spare.
        array<int, 128> need{};
        for (char c : t) need[c]++;
        int missing = t.size();  // total events still needed, repeats included
        int bestStart = 0, bestLen = INT_MAX, left = 0;
        for (int right = 0; right < (int)s.size(); right++) {
            // Taking in one more event.
            if (need[s[right]]-- > 0) missing--;
            // While the window has everything, shrink it from the left.
            while (missing == 0) {
                if (right - left + 1 < bestLen) {
                    bestStart = left;
                    bestLen = right - left + 1;
                }
                if (++need[s[left]] > 0) missing++;
                left++;
            }
        }
        return bestLen == INT_MAX ? "" : s.substr(bestStart, bestLen);
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    public String minWindow(String s, String t) {
        // How many of each event the window still needs; negative means spare.
        int[] need = new int[128];
        for (char c : t.toCharArray()) need[c]++;
        int missing = t.length();  // total events still needed, repeats included
        int bestStart = 0, bestLen = Integer.MAX_VALUE, left = 0;
        for (int right = 0; right < s.length(); right++) {
            // Taking in one more event.
            if (need[s.charAt(right)]-- > 0) missing--;
            // While the window has everything, shrink it from the left.
            while (missing == 0) {
                if (right - left + 1 < bestLen) {
                    bestStart = left;
                    bestLen = right - left + 1;
                }
                if (++need[s.charAt(left)] > 0) missing++;
                left++;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLen);
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func minWindow(s string, t string) string {
	// How many of each event the window still needs; negative means spare.
	var need [128]int
	for i := 0; i < len(t); i++ {
		need[t[i]]++
	}
	missing := len(t) // total events still needed, repeats included
	bestStart, bestLen, left := 0, len(s)+1, 0
	for right := 0; right < len(s); right++ {
		// Taking in one more event.
		if need[s[right]] > 0 {
			missing--
		}
		need[s[right]]--
		// While the window has everything, shrink it from the left.
		for missing == 0 {
			if right-left+1 < bestLen {
				bestStart, bestLen = left, right-left+1
			}
			need[s[left]]++
			if need[s[left]] > 0 {
				missing++
			}
			left++
		}
	}
	if bestLen > len(s) {
		return ""
	}
	return s[bestStart : bestStart+bestLen]
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn min_window(s: String, t: String) -> String {
        let s = s.as_bytes();
        // How many of each event the window still needs; negative means spare.
        let mut need = [0i32; 128];
        for &c in t.as_bytes() {
            need[c as usize] += 1;
        }
        let mut missing = t.len(); // total events still needed, repeats included
        let (mut best_start, mut best_len, mut left) = (0usize, usize::MAX, 0usize);
        for right in 0..s.len() {
            // Taking in one more event.
            let c = s[right] as usize;
            if need[c] > 0 {
                missing -= 1;
            }
            need[c] -= 1;
            // While the window has everything, shrink it from the left.
            while missing == 0 {
                if right - left + 1 < best_len {
                    best_start = left;
                    best_len = right - left + 1;
                }
                let g = s[left] as usize;
                need[g] += 1;
                if need[g] > 0 {
                    missing += 1;
                }
                left += 1;
            }
        }
        if best_len == usize::MAX {
            String::new()
        } else {
            String::from_utf8(s[best_start..best_start + best_len].to_vec()).unwrap()
        }
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Treating the signature as a set.** `aa` needs two a's; the counts, not just presence, must be met.
- **Recomputing completeness by comparing all counts at every step.** It's correct and much slower; the single `missing` number does the same job.
- **Changing `missing` for spare characters.** Only a character that was still needed reduces it, and only one whose count rises above zero increases it.
- **Returning the window instead of recording it.** The shortest window appears while shrinking, before the character that breaks it is removed.
- **Ignoring case.** `A` and `a` are different events.

## Related

- The other exercise in this category: [the first free locker](first-missing-positive.md) (LeetCode 41).
- Concept pages: [hash tables](../../dsa/hash-tables.md), [growth](../../dsa/growth.md), [search](../../dsa/search.md).
- More practice of the same shape: problems tagged "sliding window" on LeetCode or NeetCode.
