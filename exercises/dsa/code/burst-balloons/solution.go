package main

func maxCoins(nums []int) int {
	// Pretend there's a balloon worth 1 at each end that can't be burst.
	v := append(append([]int{1}, nums...), 1)
	n := len(v)
	// best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
	// while lo and hi themselves are still standing.
	best := make([][]int, n)
	for i := range best {
		best[i] = make([]int, n)
	}
	for width := 2; width < n; width++ {
		for lo := 0; lo+width < n; lo++ {
			hi := lo + width
			// Choose the balloon k to burst LAST in this stretch: by then its
			// neighbours are lo and hi, and the two sides were settled independently.
			for k := lo + 1; k < hi; k++ {
				best[lo][hi] = max(best[lo][hi], best[lo][k]+v[lo]*v[k]*v[hi]+best[k][hi])
			}
		}
	}
	return best[0][n-1]
}
