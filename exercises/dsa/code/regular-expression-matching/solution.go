package main

func isMatch(s string, p string) bool {
	m, n := len(s), len(p)
	// can[i][j]: does the text from position i match the pattern from position j?
	can := make([][]bool, m+1)
	for i := range can {
		can[i] = make([]bool, n+1)
	}
	can[m][n] = true // nothing left of either: a match
	for i := m; i >= 0; i-- {
		for j := n - 1; j >= 0; j-- {
			first := i < m && (p[j] == s[i] || p[j] == '.')
			if j+1 < n && p[j+1] == '*' {
				// Skip "x*" entirely, or use it for one character and stay on it.
				can[i][j] = can[i][j+2] || (first && can[i+1][j])
			} else {
				can[i][j] = first && can[i+1][j+1]
			}
		}
	}
	return can[0][0]
}
