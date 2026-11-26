package main

import "container/heap"

// A min-heap of ints; the low half stores negated values to act as a max-heap.
type intHeap []int

func (h intHeap) Len() int           { return len(h) }
func (h intHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h intHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *intHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *intHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type MedianFinder struct {
	// The smaller half (negated) and the larger half.
	// The smaller half holds the same number of values, or one more.
	low, high *intHeap
}

func Constructor() MedianFinder {
	return MedianFinder{low: &intHeap{}, high: &intHeap{}}
}

func (this *MedianFinder) AddNum(num int) {
	// Pass the new value through the low half, so the biggest of the low half moves up.
	heap.Push(this.low, -num)
	heap.Push(this.high, -heap.Pop(this.low).(int))
	// Keep the low half the same size as the high half, or one bigger.
	if this.high.Len() > this.low.Len() {
		heap.Push(this.low, -heap.Pop(this.high).(int))
	}
}

func (this *MedianFinder) FindMedian() float64 {
	if this.low.Len() > this.high.Len() {
		return float64(-(*this.low)[0])
	}
	return float64(-(*this.low)[0]+(*this.high)[0]) / 2
}
