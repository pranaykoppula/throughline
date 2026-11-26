package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var n int
	fmt.Fscan(in, &n)
	h := make([]int, n)
	for i := range h {
		fmt.Fscan(in, &h[i])
	}
	fmt.Println(largestRectangleArea(h))
}
