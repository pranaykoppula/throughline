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
