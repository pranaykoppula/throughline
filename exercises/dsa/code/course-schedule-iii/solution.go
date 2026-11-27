package main

import (
	"container/heap"
	"sort"
)

// Durations of the courses kept so far, longest on top.
type maxHeap []int

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *maxHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func scheduleCourse(courses [][]int) int {
	// Consider courses in order of deadline: the earliest deadline first.
	sort.Slice(courses, func(i, j int) bool { return courses[i][1] < courses[j][1] })
	taken := &maxHeap{}
	day := 0 // the day the kept courses finish, taken one after another
	for _, c := range courses {
		heap.Push(taken, c[0])
		day += c[0]
		if day > c[1] {
			// Too late: drop the longest course kept so far. It frees the most time,
			// and the rest still finish in time because their deadlines are earlier.
			day -= heap.Pop(taken).(int)
		}
	}
	return taken.Len()
}
