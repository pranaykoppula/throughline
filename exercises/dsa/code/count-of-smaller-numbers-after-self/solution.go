package main

func countSmaller(nums []int) []int {
	n := len(nums)
	counts := make([]int, n)
	merged := make([]int, n)
	order := make([]int, n) // positions, to be sorted by value
	for i := range order {
		order[i] = i
	}
	// Sort order[lo:hi] by value, counting for each position
	// how many smaller values from its right cross to its left.
	var sortRange func(lo, hi int)
	sortRange = func(lo, hi int) {
		if hi-lo <= 1 {
			return
		}
		mid := (lo + hi) / 2
		sortRange(lo, mid)
		sortRange(mid, hi)
		j, k := mid, lo
		for i := lo; i < mid; i++ {
			// Every right-half value placed before this one is smaller and was to its right.
			for j < hi && nums[order[j]] < nums[order[i]] {
				merged[k] = order[j]
				k++
				j++
			}
			counts[order[i]] += j - mid
			merged[k] = order[i]
			k++
		}
		for ; j < hi; j++ {
			merged[k] = order[j]
			k++
		}
		copy(order[lo:hi], merged[lo:hi])
	}
	sortRange(0, n)
	return counts
}
