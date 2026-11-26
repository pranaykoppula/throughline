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
	buildings := make([][]int, n)
	for i := range buildings {
		buildings[i] = make([]int, 3)
		fmt.Fscan(in, &buildings[i][0], &buildings[i][1], &buildings[i][2])
	}
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()
	for _, p := range getSkyline(buildings) {
		fmt.Fprintf(out, "%d %d\n", p[0], p[1])
	}
}
