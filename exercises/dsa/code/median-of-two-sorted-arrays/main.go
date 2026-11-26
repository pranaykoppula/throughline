package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var m, n int
	fmt.Fscan(in, &m)
	a := make([]int, m)
	for i := range a {
		fmt.Fscan(in, &a[i])
	}
	fmt.Fscan(in, &n)
	b := make([]int, n)
	for i := range b {
		fmt.Fscan(in, &b[i])
	}
	fmt.Printf("%.5f\n", findMedianSortedArrays(a, b))
}
