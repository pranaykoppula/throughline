package main

func candy(ratings []int) int {
	n := len(ratings)
	give := make([]int, n)
	for i := range give {
		give[i] = 1 // everyone gets at least one
	}
	// Left to right: anyone rated above their left neighbour gets one more than them.
	for i := 1; i < n; i++ {
		if ratings[i] > ratings[i-1] {
			give[i] = give[i-1] + 1
		}
	}
	// Right to left: the same for right neighbours, without undoing the first pass.
	for i := n - 2; i >= 0; i-- {
		if ratings[i] > ratings[i+1] {
			give[i] = max(give[i], give[i+1]+1)
		}
	}
	total := 0
	for _, g := range give {
		total += g
	}
	return total
}
