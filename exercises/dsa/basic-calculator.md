# The formula box

An exercise in the category **nesting and undo**. It's LeetCode 224, [Basic Calculator](https://leetcode.com/problems/basic-calculator/), rated Hard.

## The situation

A small charity's budgeting tool lets volunteers type a sum into a cell, such as `1200 - (350 + 80) - (90 - 15)`, and shows the result. The first version handed the text to the programming language's own `eval`, which worked until someone realised that `eval` would run any code at all that a volunteer typed. The tool needs to work out these sums itself: whole numbers, plus, minus, brackets nested as deep as people like, and spaces anywhere.

## The problem

You're given a string holding a valid expression made of non-negative whole numbers, `+`, `-`, brackets and spaces. A `-` can also be a negative sign, at the start or just after an opening bracket. Return the value of the expression, without using any built-in function that evaluates expressions.

For `(1+(4+5+2)-3)+(6+8)`, the answer is 23.

## The question it asks

"What was I in the middle of before this bracket opened?" Every opening bracket puts the outside sum on hold, and the matching closing bracket picks it up again, last opened, first closed. That's a stack, the structure behind nesting and undo. See the row for nesting and undo in [choosing a data structure](../../dsa/choosing.md). Brackets nested to any depth are exactly what [power and predictability](../../dsa/power-and-predictability.md) says a fixed-memory machine can't handle and a stack can.

## The tempting first answer

Find the innermost pair of brackets, work out what's inside, replace the brackets with the result as text, and repeat until none are left. It's correct, and it's how people do sums by hand. But each round scans and rebuilds the whole string, and a formula nested *d* deep needs *d* rounds, so the work grows with the length times the depth ([growth](../../dsa/growth.md)). It also has to cope with results that come out negative: `7-(2-5)` becomes `7--3`, and now the rewriter needs a rule for two minus signs in a row. The text rewriting is where the bugs live.

The other tempting answer is the one the charity started with: hand it to `eval`. That climbs to the top rung of the ladder, a language that can do anything, to answer a question that needs only a stack.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Without brackets, one pass is enough: keep a running total and the sign in front of the number you're reading. When you meet the next `+` or `-`, add the finished number to the total with its sign.

</details>

<details markdown="1"><summary>Hint 2</summary>

A bracket is a fresh sum that starts at 0. When it opens, what do you need to remember about the sum outside so you can carry on afterwards?

</details>

<details markdown="1"><summary>Hint 3</summary>

Remember two things: the total so far outside, and the sign just before the bracket. When the bracket closes, its total is multiplied by that sign and added to the outside total. Brackets nest, so keep these pairs on a stack.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Read the string once, left to right, keeping:

- `total`, the running total inside the current brackets;
- `sign`, +1 or −1, the sign in front of the number being read;
- `number`, the number being read, built digit by digit;
- `saved`, a stack of `(total, sign)` pairs, one for each bracket still open.

For each character:

1. **A digit:** `number = number × 10 + digit`.
2. **`+` or `-`:** the number before it is finished, so `total += sign × number`, reset `number` to 0, and set `sign` from the operator.
3. **`(`:** push `(total, sign)` and start again inside with `total = 0` and `sign = +1`.
4. **`)`:** finish the last number inside, then pop `(outside, outside_sign)` and fold the bracket in: `total = outside + outside_sign × total`.
5. **A space:** skip it.

At the end, add the last number: the answer is `total + sign × number`.

**Why the negative signs take care of themselves:** a `-` at the start or just after `(` is treated like any other minus. The number before it is 0, so adding it changes nothing, and the sign of what follows becomes −1. That's why `-(2+3)` and `1-(-2)` need no special case.

**Why it's fast:** each character is looked at once, and each bracket is pushed and popped once.

**Time:** proportional to the length. **Memory:** proportional to the deepest nesting.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
class Solution:
    def calculate(self, s: str) -> int:
        total = 0      # the running total inside the current brackets
        sign = 1       # the sign in front of the number being read
        number = 0     # the number being read, digit by digit
        saved = []     # (total, sign) waiting outside each open bracket
        for ch in s:
            if ch.isdigit():
                number = number * 10 + int(ch)
            elif ch in "+-":
                total += sign * number
                number = 0
                sign = 1 if ch == "+" else -1
            elif ch == "(":
                # Put the outside aside, and start a fresh total inside.
                saved.append((total, sign))
                total, sign = 0, 1
            elif ch == ")":
                total += sign * number
                number = 0
                # Fold the bracket's total back into the outside.
                outside, outside_sign = saved.pop()
                total = outside + outside_sign * total
        return total + sign * number
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
public:
    int calculate(string s) {
        long long total = 0;   // the running total inside the current brackets
        int sign = 1;          // the sign in front of the number being read
        long long number = 0;  // the number being read, digit by digit
        vector<pair<long long, int>> saved;  // (total, sign) outside each open bracket
        for (char ch : s) {
            if (isdigit(ch)) {
                number = number * 10 + (ch - '0');
            } else if (ch == '+' || ch == '-') {
                total += sign * number;
                number = 0;
                sign = ch == '+' ? 1 : -1;
            } else if (ch == '(') {
                // Put the outside aside, and start a fresh total inside.
                saved.push_back({total, sign});
                total = 0;
                sign = 1;
            } else if (ch == ')') {
                total += sign * number;
                number = 0;
                // Fold the bracket's total back into the outside.
                auto [outside, outsideSign] = saved.back();
                saved.pop_back();
                total = outside + outsideSign * total;
            }
        }
        return (int)(total + sign * number);
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int calculate(String s) {
        long total = 0;   // the running total inside the current brackets
        int sign = 1;     // the sign in front of the number being read
        long number = 0;  // the number being read, digit by digit
        Deque<long[]> saved = new ArrayDeque<>();  // {total, sign} outside each open bracket
        for (char ch : s.toCharArray()) {
            if (Character.isDigit(ch)) {
                number = number * 10 + (ch - '0');
            } else if (ch == '+' || ch == '-') {
                total += sign * number;
                number = 0;
                sign = ch == '+' ? 1 : -1;
            } else if (ch == '(') {
                // Put the outside aside, and start a fresh total inside.
                saved.push(new long[] {total, sign});
                total = 0;
                sign = 1;
            } else if (ch == ')') {
                total += sign * number;
                number = 0;
                // Fold the bracket's total back into the outside.
                long[] outside = saved.pop();
                total = outside[0] + outside[1] * total;
            }
        }
        return (int) (total + sign * number);
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func calculate(s string) int {
	total := 0  // the running total inside the current brackets
	sign := 1   // the sign in front of the number being read
	number := 0 // the number being read, digit by digit
	saved := [][2]int{} // {total, sign} outside each open bracket
	for i := 0; i < len(s); i++ {
		ch := s[i]
		switch {
		case ch >= '0' && ch <= '9':
			number = number*10 + int(ch-'0')
		case ch == '+' || ch == '-':
			total += sign * number
			number = 0
			sign = 1
			if ch == '-' {
				sign = -1
			}
		case ch == '(':
			// Put the outside aside, and start a fresh total inside.
			saved = append(saved, [2]int{total, sign})
			total, sign = 0, 1
		case ch == ')':
			total += sign * number
			number = 0
			// Fold the bracket's total back into the outside.
			outside := saved[len(saved)-1]
			saved = saved[:len(saved)-1]
			total = outside[0] + outside[1]*total
		}
	}
	return total + sign*number
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn calculate(s: String) -> i32 {
        let mut total: i64 = 0; // the running total inside the current brackets
        let mut sign: i64 = 1; // the sign in front of the number being read
        let mut number: i64 = 0; // the number being read, digit by digit
        let mut saved: Vec<(i64, i64)> = Vec::new(); // (total, sign) outside each open bracket
        for ch in s.chars() {
            match ch {
                '0'..='9' => number = number * 10 + ch.to_digit(10).unwrap() as i64,
                '+' | '-' => {
                    total += sign * number;
                    number = 0;
                    sign = if ch == '+' { 1 } else { -1 };
                }
                '(' => {
                    // Put the outside aside, and start a fresh total inside.
                    saved.push((total, sign));
                    total = 0;
                    sign = 1;
                }
                ')' => {
                    total += sign * number;
                    number = 0;
                    // Fold the bracket's total back into the outside.
                    let (outside, outside_sign) = saved.pop().unwrap();
                    total = outside + outside_sign * total;
                }
                _ => {}
            }
        }
        (total + sign * number) as i32
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Forgetting the last number.** The loop only adds a number when the next operator or bracket arrives; the one at the very end needs adding after the loop.
- **Losing the sign before a bracket.** `5 - (2 + 3)` is 0, not 10. The sign has to be saved with the outside total and applied to the whole bracket.
- **Reading numbers one digit at a time.** `123` is one number; keep building it until a non-digit arrives.
- **Special-casing unary minus.** Treating it as "0 minus" falls out of the running total for free; extra branches for it are where bugs creep in.

## Related

- The other exercise in this category: [the biggest banner](largest-rectangle-in-histogram.md) (LeetCode 84).
- Concept pages: [power and predictability](../../dsa/power-and-predictability.md), [state machines](../../dsa/state-machines.md), [input validation](../../security/input-validation.md), [growth](../../dsa/growth.md).
- More practice of the same shape: the versions of this problem with multiplication and division (Basic Calculator II and III), where a stack also has to respect which operator binds tighter.
