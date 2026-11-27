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
