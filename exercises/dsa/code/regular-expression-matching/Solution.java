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
