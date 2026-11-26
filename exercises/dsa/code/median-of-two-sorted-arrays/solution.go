package main

import "math"

func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
	// Search the shorter slice, so the halving takes the fewest steps.
	if len(nums1) > len(nums2) {
		return findMedianSortedArrays(nums2, nums1)
	}
	a, b := nums1, nums2
	m, n := len(a), len(b)
	half := (m + n + 1) / 2
	lo, hi := 0, m
	for lo <= hi {
		// Take i from a and the rest of the left half from b.
		i := (lo + hi) / 2
		j := half - i
		aLeft, aRight, bLeft, bRight := math.MinInt, math.MaxInt, math.MinInt, math.MaxInt
		if i > 0 {
			aLeft = a[i-1]
		}
		if i < m {
			aRight = a[i]
		}
		if j > 0 {
			bLeft = b[j-1]
		}
		if j < n {
			bRight = b[j]
		}
		if aLeft > bRight {
			hi = i - 1 // took too many from a
		} else if bLeft > aRight {
			lo = i + 1 // took too few from a
		} else {
			// Every left value is no bigger than every right value.
			if (m+n)%2 == 1 {
				return float64(max(aLeft, bLeft))
			}
			return float64(max(aLeft, bLeft)+min(aRight, bRight)) / 2
		}
	}
	return 0 // not reached for sorted inputs
}
