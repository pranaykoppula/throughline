impl Solution {
    pub fn is_match(s: String, p: String) -> bool {
        let (s, p) = (s.as_bytes(), p.as_bytes());
        let (m, n) = (s.len(), p.len());
        // can[i][j]: does the text from position i match the pattern from position j?
        let mut can = vec![vec![false; n + 1]; m + 1];
        can[m][n] = true; // nothing left of either: a match
        for i in (0..=m).rev() {
            for j in (0..n).rev() {
                let first = i < m && (p[j] == s[i] || p[j] == b'.');
                if j + 1 < n && p[j + 1] == b'*' {
                    // Skip "x*" entirely, or use it for one character and stay on it.
                    can[i][j] = can[i][j + 2] || (first && can[i + 1][j]);
                } else {
                    can[i][j] = first && can[i + 1][j + 1];
                }
            }
        }
        can[0][0]
    }
}
