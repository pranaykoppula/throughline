class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.size(), n = p.size();
        // can[i][j]: does the text from position i match the pattern from position j?
        vector<vector<bool>> can(m + 1, vector<bool>(n + 1, false));
        can[m][n] = true;  // nothing left of either: a match
        for (int i = m; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                bool first = i < m && (p[j] == s[i] || p[j] == '.');
                if (j + 1 < n && p[j + 1] == '*') {
                    // Skip "x*" entirely, or use it for one character and stay on it.
                    can[i][j] = can[i][j + 2] || (first && can[i + 1][j]);
                } else {
                    can[i][j] = first && can[i + 1][j + 1];
                }
            }
        }
        return can[0][0];
    }
};
