package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var n, m int
	fmt.Fscan(in, &n, &m)
	edges := make([][]int, m)
	for i := range edges {
		edges[i] = make([]int, 2)
		fmt.Fscan(in, &edges[i][0], &edges[i][1])
	}
	out := [][2]int{}
	for _, e := range criticalConnections(n, edges) {
		out = append(out, [2]int{min(e[0], e[1]), max(e[0], e[1])})
	}
	sort.Slice(out, func(i, j int) bool {
		if out[i][0] != out[j][0] {
			return out[i][0] < out[j][0]
		}
		return out[i][1] < out[j][1]
	})
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	for _, e := range out {
		fmt.Fprintf(w, "%d %d\n", e[0], e[1])
	}
}
