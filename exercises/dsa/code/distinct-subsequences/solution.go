package main

func numDistinct(s string, t string) int {
	m := len(t)
	// ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
	// uint64 wraps on overflow; the final answer fits in 32 bits, and wrapping keeps
	// every count correct modulo 2^64, so the answer comes out right.
	ways := make([]uint64, m+1)
	ways[0] = 1 // the empty prefix of t, in exactly one way
	for i := 0; i < len(s); i++ {
		// Go right to left, so each character of s is used at most once per way.
		for j := m; j >= 1; j-- {
			if t[j-1] == s[i] {
				ways[j] += ways[j-1]
			}
		}
	}
	return int(ways[m])
}
