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
