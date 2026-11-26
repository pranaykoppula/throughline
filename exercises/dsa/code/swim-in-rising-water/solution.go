package main

import "container/heap"

// Squares we can reach: {level needed, row, column}, lowest level on top.
type cellHeap [][3]int

func (h cellHeap) Len() int           { return len(h) }
func (h cellHeap) Less(i, j int) bool { return h[i][0] < h[j][0] }
func (h cellHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *cellHeap) Push(x any)        { *h = append(*h, x.([3]int)) }
func (h *cellHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func swimInWater(grid [][]int) int {
	n := len(grid)
	seen := make([][]bool, n)
	for i := range seen {
		seen[i] = make([]bool, n)
	}
	frontier := &cellHeap{{grid[0][0], 0, 0}}
	seen[0][0] = true
	steps := [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for frontier.Len() > 0 {
		top := heap.Pop(frontier).([3]int)
		level, r, c := top[0], top[1], top[2]
		if r == n-1 && c == n-1 {
			return level
		}
		for _, s := range steps {
			nr, nc := r+s[0], c+s[1]
			if nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc] {
				seen[nr][nc] = true
				// Reaching the neighbour needs the higher of the two levels.
				heap.Push(frontier, [3]int{max(level, grid[nr][nc]), nr, nc})
			}
		}
	}
	return -1
}
