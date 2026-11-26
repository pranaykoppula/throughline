package main

func maxSlidingWindow(nums []int, k int) []int {
	// Indices of readings that could still be a window's maximum,
	// with their values in decreasing order from front to back.
	candidates := []int{}
	result := []int{}
	for i, x := range nums {
		// A new reading outlives every smaller one before it.
		for len(candidates) > 0 && nums[candidates[len(candidates)-1]] <= x {
			candidates = candidates[:len(candidates)-1]
		}
		candidates = append(candidates, i)
		// The front has slid out of the window.
		if candidates[0] <= i-k {
			candidates = candidates[1:]
		}
		if i >= k-1 {
			result = append(result, nums[candidates[0]])
		}
	}
	return result
}
