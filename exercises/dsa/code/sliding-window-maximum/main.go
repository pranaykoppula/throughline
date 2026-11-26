package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var n, k int
	fmt.Fscan(in, &n, &k)
	nums := make([]int, n)
	for i := range nums {
		fmt.Fscan(in, &nums[i])
	}
	r := maxSlidingWindow(nums, k)
	parts := make([]string, len(r))
	for i, x := range r {
		parts[i] = fmt.Sprint(x)
	}
	fmt.Println(strings.Join(parts, " "))
}
