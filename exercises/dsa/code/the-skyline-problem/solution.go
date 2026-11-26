package main

import (
	"container/heap"
	"sort"
)

// Buildings that have started: {height, right edge}, tallest on top.
type standingHeap [][2]int

func (h standingHeap) Len() int           { return len(h) }
func (h standingHeap) Less(i, j int) bool { return h[i][0] > h[j][0] }
func (h standingHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *standingHeap) Push(x any)        { *h = append(*h, x.([2]int)) }
func (h *standingHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func getSkyline(buildings [][]int) [][]int {
	// Every place the outline can change: a building's left or right edge.
	seen := map[int]bool{}
	edges := []int{}
	for _, b := range buildings {
		for _, x := range []int{b[0], b[1]} {
			if !seen[x] {
				seen[x] = true
				edges = append(edges, x)
			}
		}
	}
	sort.Ints(edges)

	skyline := [][]int{}
	standing := &standingHeap{}
	i := 0
	for _, x := range edges {
		// Buildings that start here join the heap (the input is sorted by left edge).
		for i < len(buildings) && buildings[i][0] <= x {
			heap.Push(standing, [2]int{buildings[i][2], buildings[i][1]})
			i++
		}
		// The tallest might have ended already; drop it only when it's on top.
		for standing.Len() > 0 && (*standing)[0][1] <= x {
			heap.Pop(standing)
		}
		height := 0
		if standing.Len() > 0 {
			height = (*standing)[0][0]
		}
		if len(skyline) == 0 || skyline[len(skyline)-1][1] != height {
			skyline = append(skyline, []int{x, height})
		}
	}
	return skyline
}
