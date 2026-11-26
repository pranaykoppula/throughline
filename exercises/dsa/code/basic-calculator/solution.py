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
