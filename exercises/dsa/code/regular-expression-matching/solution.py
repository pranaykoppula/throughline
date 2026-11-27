class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        # can[i][j]: does the text from position i match the pattern from position j?
        can = [[False] * (n + 1) for _ in range(m + 1)]
        can[m][n] = True   # nothing left of either: a match
        for i in range(m, -1, -1):
            for j in range(n - 1, -1, -1):
                first = i < m and p[j] in (s[i], ".")
                if j + 1 < n and p[j + 1] == "*":
                    # Skip "x*" entirely, or use it for one character and stay on it.
                    can[i][j] = can[i][j + 2] or (first and can[i + 1][j])
                else:
                    can[i][j] = first and can[i + 1][j + 1]
        return can[0][0]
