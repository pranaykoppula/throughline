package main

func splitArray(nums []int, k int) int {
	// Fill each day greedily; start a new day when the next job won't fit.
	daysNeeded := func(limit int) int {
		days, load := 1, 0
		for _, x := range nums {
			if load+x > limit {
				days++
				load = 0
			}
			load += x
		}
		return days
	}
	// The answer is at least the biggest single job and at most everything in one day.
	lo, hi := 0, 0
	for _, x := range nums {
		lo = max(lo, x)
		hi += x
	}
	for lo < hi {
		mid := lo + (hi-lo)/2
		if daysNeeded(mid) <= k {
			hi = mid // this limit works; try a smaller one
		} else {
			lo = mid + 1 // too tight; the answer is bigger
		}
	}
	return lo
}
