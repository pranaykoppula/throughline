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
	grid := make([][]int, n)
	for r := range grid {
		grid[r] = make([]int, n)
		for c := range grid[r] {
			fmt.Fscan(in, &grid[r][c])
		}
	}
	fmt.Println(swimInWater(grid))
}
