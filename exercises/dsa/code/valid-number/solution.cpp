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
