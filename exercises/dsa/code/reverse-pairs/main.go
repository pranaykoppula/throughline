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
	nums := make([]int, n)
	for i := range nums {
		fmt.Fscan(in, &nums[i])
	}
	fmt.Println(reversePairs(nums))
}
