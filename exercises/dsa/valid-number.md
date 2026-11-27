# The price column

An exercise in the category **which state, what next**. It's LeetCode 65, [Valid Number](https://leetcode.com/problems/valid-number/), rated Hard.

## The situation

A wholesaler imports price lists from a few hundred suppliers every night, as text files. Most cells in the price column are ordinary numbers, but some suppliers write `1.5e3`, some `.75`, some `12.`, and every so often a cell says `call us`, `12,50` or `1e`. The import used the language's own number parser, which accepted different things on different servers and once read `NaN` as a price. The team wants one strict rule for what counts as a number, written down and checked the same way everywhere, before anything is converted.

## The problem

You're given a string. Decide whether it's a valid number under these rules:

- An optional sign, `+` or `-`.
- Then a decimal: digits, or digits followed by a dot, or digits, a dot and more digits, or a dot followed by digits. At least one digit somewhere.
- Then, optionally, an exponent: `e` or `E`, an optional sign, and at least one digit.
- Nothing else, not even spaces.

So `2`, `-0.1`, `4.`, `-.9`, `2e10` and `+6e-1` are numbers; `abc`, `1e`, `e3`, `99e2.5`, `--6` and `.` are not.

## The question it asks

"Given what I've read so far, which characters may come next?" At every point the answer depends only on a small summary of the past: have I seen a sign, digits, a dot, an e? That's a [state machine](../../dsa/state-machines.md). See the row for which state, what next in [choosing a data structure](../../dsa/choosing.md). The rules describe a regular language, the bottom rung of [power and predictability](../../dsa/power-and-predictability.md), so a fixed number of states is enough.

## The tempting first answer

A pile of flags and conditions: `seen_digit`, `seen_dot`, `seen_e`, and a branch for each character checking them in the right combination. It's linear and it can be made correct. But the rules interact (a dot is fine before the `e` and not after it; a sign is fine at the start or straight after the `e` and nowhere else), and each fix for one case breaks another. Most failed attempts at this problem are a flag-and-branch version that's right for all the cases its author thought of.

The other tempting answer is to call the language's number parser and see if it complains. That's what caused the wholesaler's trouble: each parser has its own idea of a number, and some accept `Infinity`, `NaN`, spaces or underscores.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Write down, in words, every distinct situation you can be in partway through reading a number: "nothing yet", "just read a sign", "reading digits before any dot", and so on. How many are there?

</details>

<details markdown="1"><summary>Hint 2</summary>

Group the characters into a handful of kinds: digit, sign, dot, `e`, anything else. Then for each situation and each kind of character, there's exactly one answer: which situation you're in next, or "this can't be a number".

</details>

<details markdown="1"><summary>Hint 3</summary>

Some situations are fine places to stop (after digits, or after a dot that followed digits); others aren't (after a lone sign, a lone dot, or an `e`). Which ones?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Write the rules as a table of states and moves, and run the string through it.

**The kinds of character:** digit, sign, dot, `e` or `E`, and anything else.

**The nine states:**

| State | Meaning | Can stop here? |
| --- | --- | --- |
| 0 | start, nothing read | no |
| 1 | a sign | no |
| 2 | digits, before any dot | yes |
| 3 | a dot with no digits before it | no |
| 4 | a dot after digits | yes |
| 5 | digits after the dot | yes |
| 6 | an `e` | no |
| 7 | a sign after the `e` | no |
| 8 | digits after the `e` | yes |

**The moves** (a dash means the string can't be a number):

| From | digit | sign | dot | `e` | other |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 3 | – | – |
| 1 | 2 | – | 3 | – | – |
| 2 | 2 | – | 4 | 6 | – |
| 3 | 5 | – | – | – | – |
| 4 | 5 | – | – | 6 | – |
| 5 | 5 | – | – | 6 | – |
| 6 | 8 | 7 | – | – | – |
| 7 | 8 | – | – | – | – |
| 8 | 8 | – | – | – | – |

Start in state 0, follow one move per character, and stop as soon as there's no move. The string is a number if you end in state 2, 4, 5 or 8.

**Why a table beats flags:** every combination of state and character is written down exactly once, so a missing case is a visible gap in the table instead of a branch nobody thought of. Checking the design means reading seventeen entries, not tracing paths through nested conditions. That's the same reason [state machines](../../dsa/state-machines.md) make an order's lifecycle checkable.

**Why it's fast:** one table lookup per character, and the memory is the table, whatever the length of the string.

**Time:** proportional to the length. **Memory:** a fixed amount.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
class Solution:
    def isNumber(self, s: str) -> bool:
        # Kinds of character: 0 digit, 1 sign, 2 dot, 3 e or E, 4 anything else.
        def kind(c: str) -> int:
            if c.isdigit():
                return 0
            if c in "+-":
                return 1
            if c == ".":
                return 2
            if c in "eE":
                return 3
            return 4

        # States: 0 start, 1 sign, 2 digits, 3 dot with no digits before it,
        # 4 dot after digits, 5 digits after the dot, 6 e, 7 sign after e, 8 digits after e.
        # MOVES[state][kind] is the next state, or -1 when the text can't be a number.
        MOVES = [
            [2, 1, 3, -1, -1],
            [2, -1, 3, -1, -1],
            [2, -1, 4, 6, -1],
            [5, -1, -1, -1, -1],
            [5, -1, -1, 6, -1],
            [5, -1, -1, 6, -1],
            [8, 7, -1, -1, -1],
            [8, -1, -1, -1, -1],
            [8, -1, -1, -1, -1],
        ]
        state = 0
        for c in s:
            state = MOVES[state][kind(c)]
            if state == -1:
                return False
        # Only some states are the end of a whole number.
        return state in (2, 4, 5, 8)
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
    // Kinds of character: 0 digit, 1 sign, 2 dot, 3 e or E, 4 anything else.
    static int kind(char c) {
        if (isdigit((unsigned char)c)) return 0;
        if (c == '+' || c == '-') return 1;
        if (c == '.') return 2;
        if (c == 'e' || c == 'E') return 3;
        return 4;
    }

public:
    bool isNumber(string s) {
        // States: 0 start, 1 sign, 2 digits, 3 dot with no digits before it,
        // 4 dot after digits, 5 digits after the dot, 6 e, 7 sign after e, 8 digits after e.
        // moves[state][kind] is the next state, or -1 when the text can't be a number.
        static const int moves[9][5] = {
            {2, 1, 3, -1, -1},
            {2, -1, 3, -1, -1},
            {2, -1, 4, 6, -1},
            {5, -1, -1, -1, -1},
            {5, -1, -1, 6, -1},
            {5, -1, -1, 6, -1},
            {8, 7, -1, -1, -1},
            {8, -1, -1, -1, -1},
            {8, -1, -1, -1, -1},
        };
        int state = 0;
        for (char c : s) {
            state = moves[state][kind(c)];
            if (state == -1) return false;
        }
        // Only some states are the end of a whole number.
        return state == 2 || state == 4 || state == 5 || state == 8;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
class Solution {
    // States: 0 start, 1 sign, 2 digits, 3 dot with no digits before it,
    // 4 dot after digits, 5 digits after the dot, 6 e, 7 sign after e, 8 digits after e.
    // MOVES[state][kind] is the next state, or -1 when the text can't be a number.
    private static final int[][] MOVES = {
        {2, 1, 3, -1, -1},
        {2, -1, 3, -1, -1},
        {2, -1, 4, 6, -1},
        {5, -1, -1, -1, -1},
        {5, -1, -1, 6, -1},
        {5, -1, -1, 6, -1},
        {8, 7, -1, -1, -1},
        {8, -1, -1, -1, -1},
        {8, -1, -1, -1, -1},
    };

    // Kinds of character: 0 digit, 1 sign, 2 dot, 3 e or E, 4 anything else.
    private static int kind(char c) {
        if (c >= '0' && c <= '9') return 0;
        if (c == '+' || c == '-') return 1;
        if (c == '.') return 2;
        if (c == 'e' || c == 'E') return 3;
        return 4;
    }

    public boolean isNumber(String s) {
        int state = 0;
        for (char c : s.toCharArray()) {
            state = MOVES[state][kind(c)];
            if (state == -1) return false;
        }
        // Only some states are the end of a whole number.
        return state == 2 || state == 4 || state == 5 || state == 8;
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func isNumber(s string) bool {
	// Kinds of character: 0 digit, 1 sign, 2 dot, 3 e or E, 4 anything else.
	kind := func(c byte) int {
		switch {
		case c >= '0' && c <= '9':
			return 0
		case c == '+' || c == '-':
			return 1
		case c == '.':
			return 2
		case c == 'e' || c == 'E':
			return 3
		}
		return 4
	}
	// States: 0 start, 1 sign, 2 digits, 3 dot with no digits before it,
	// 4 dot after digits, 5 digits after the dot, 6 e, 7 sign after e, 8 digits after e.
	// moves[state][kind] is the next state, or -1 when the text can't be a number.
	moves := [9][5]int{
		{2, 1, 3, -1, -1},
		{2, -1, 3, -1, -1},
		{2, -1, 4, 6, -1},
		{5, -1, -1, -1, -1},
		{5, -1, -1, 6, -1},
		{5, -1, -1, 6, -1},
		{8, 7, -1, -1, -1},
		{8, -1, -1, -1, -1},
		{8, -1, -1, -1, -1},
	}
	state := 0
	for i := 0; i < len(s); i++ {
		state = moves[state][kind(s[i])]
		if state == -1 {
			return false
		}
	}
	// Only some states are the end of a whole number.
	return state == 2 || state == 4 || state == 5 || state == 8
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn is_number(s: String) -> bool {
        // Kinds of character: 0 digit, 1 sign, 2 dot, 3 e or E, 4 anything else.
        let kind = |c: u8| match c {
            b'0'..=b'9' => 0,
            b'+' | b'-' => 1,
            b'.' => 2,
            b'e' | b'E' => 3,
            _ => 4,
        };
        // States: 0 start, 1 sign, 2 digits, 3 dot with no digits before it,
        // 4 dot after digits, 5 digits after the dot, 6 e, 7 sign after e, 8 digits after e.
        // MOVES[state][kind] is the next state, or -1 when the text can't be a number.
        const MOVES: [[i32; 5]; 9] = [
            [2, 1, 3, -1, -1],
            [2, -1, 3, -1, -1],
            [2, -1, 4, 6, -1],
            [5, -1, -1, -1, -1],
            [5, -1, -1, 6, -1],
            [5, -1, -1, 6, -1],
            [8, 7, -1, -1, -1],
            [8, -1, -1, -1, -1],
            [8, -1, -1, -1, -1],
        ];
        let mut state = 0i32;
        for &c in s.as_bytes() {
            state = MOVES[state as usize][kind(c)];
            if state == -1 {
                return false;
            }
        }
        // Only some states are the end of a whole number.
        matches!(state, 2 | 4 | 5 | 8)
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Accepting a lone dot or a lone sign.** `.`, `+` and `+.` contain no digits. The states for "a dot with no digits yet" and "a sign" must not be places to stop.
- **Allowing a dot in the exponent.** `99e2.5` isn't a number; after the `e`, only an optional sign and digits are allowed.
- **Forgetting the digits after `e`.** `1e` and `1e+` aren't numbers.
- **Trusting the language's parser.** Each has its own rules, and several accept `inf`, `NaN`, spaces or digit separators.

## Related

- The other exercise in this category: [the rule that took the afternoon](regular-expression-matching.md) (LeetCode 10).
- Concept pages: [state machines](../../dsa/state-machines.md), [power and predictability](../../dsa/power-and-predictability.md), [input validation](../../security/input-validation.md), [encodings](../../info/encodings.md).
- More practice of the same shape: writing the same rules as a regular expression, `^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$`, and checking that it agrees with your table on the tests.
