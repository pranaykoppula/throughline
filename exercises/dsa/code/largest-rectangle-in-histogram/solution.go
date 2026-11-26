package main

func largestRectangleArea(heights []int) int {
	n, best := len(heights), 0
	// Positions of bars still waiting to learn how far right they reach,
	// with heights increasing from bottom to top.
	stack := []int{}
	for i := 0; i <= n; i++ {
		h := 0 // a zero at the end settles every bar
		if i < n {
			h = heights[i]
		}
		// A shorter bar ends every taller bar still waiting.
		for len(stack) > 0 && heights[stack[len(stack)-1]] >= h {
			height := heights[stack[len(stack)-1]]
			stack = stack[:len(stack)-1]
			// It stretched left to just after the bar now below it in the stack.
			left := 0
			if len(stack) > 0 {
				left = stack[len(stack)-1] + 1
			}
			best = max(best, height*(i-left))
		}
		stack = append(stack, i)
	}
	return best
}
