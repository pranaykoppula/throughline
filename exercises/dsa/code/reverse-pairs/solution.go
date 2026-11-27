package main

func reversePairs(nums []int) int {
	a := append([]int(nil), nums...)
	merged := make([]int, len(a))
	// Sort a[lo:hi], and return how many pairs i < j in it have a[i] > 2 * a[j].
	var sortRange func(lo, hi int) int
	sortRange = func(lo, hi int) int {
		if hi-lo <= 1 {
			return 0
		}
		mid := (lo + hi) / 2
		count := sortRange(lo, mid) + sortRange(mid, hi)
		// Both halves are sorted: count the pairs that cross from left to right.
		j := mid
		for i := lo; i < mid; i++ {
			for j < hi && a[i] > 2*a[j] { // Go's int is 64 bits, so 2 * a[j] can't overflow
				j++
			}
			count += j - mid
		}
		// Then merge, as merge sort does.
		i, r, k := lo, mid, lo
		for i < mid || r < hi {
			if r == hi || (i < mid && a[i] <= a[r]) {
				merged[k] = a[i]
				i++
			} else {
				merged[k] = a[r]
				r++
			}
			k++
		}
		copy(a[lo:hi], merged[lo:hi])
		return count
	}
	return sortRange(0, len(a))
}
