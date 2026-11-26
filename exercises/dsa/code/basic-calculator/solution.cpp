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
