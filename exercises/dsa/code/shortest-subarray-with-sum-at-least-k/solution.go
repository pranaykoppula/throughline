package main

func shortestSubarray(nums []int, k int) int {
	n := len(nums)
	// prefix[j] - prefix[i] is the total of days i .. j-1.
	prefix := make([]int, n+1)
	for i, x := range nums {
		prefix[i+1] = prefix[i] + x
	}
	best := n + 1
	// Start points worth keeping, with prefix totals increasing from front to back.
	starts := []int{}
	for j := 0; j <= n; j++ {
		// The oldest start that already reaches k gives its best answer now.
		for len(starts) > 0 && prefix[j]-prefix[starts[0]] >= k {
			if j-starts[0] < best {
				best = j - starts[0]
			}
			starts = starts[1:]
		}
		// A start with a total at least as high as this one is never better.
		for len(starts) > 0 && prefix[starts[len(starts)-1]] >= prefix[j] {
			starts = starts[:len(starts)-1]
		}
		starts = append(starts, j)
	}
	if best <= n {
		return best
	}
	return -1
}
