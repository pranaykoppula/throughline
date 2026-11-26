package main

func firstMissingPositive(nums []int) int {
	n := len(nums)
	// Use the slice itself as the table: number v belongs at position v - 1.
	for i := 0; i < n; i++ {
		// Keep swapping until this slot holds something that can't be placed,
		// or already sits where it belongs.
		for nums[i] >= 1 && nums[i] <= n && nums[nums[i]-1] != nums[i] {
			home := nums[i] - 1
			nums[i], nums[home] = nums[home], nums[i]
		}
	}
	// The first slot not holding its own number marks the gap.
	for i := 0; i < n; i++ {
		if nums[i] != i+1 {
			return i + 1
		}
	}
	return n + 1
}
