package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var n int
	fmt.Fscan(in, &n)
	nums := make([]int, n)
	for i := range nums {
		fmt.Fscan(in, &nums[i])
	}
	out := countSmaller(nums)
	parts := make([]string, len(out))
	for i, c := range out {
		parts[i] = strconv.Itoa(c)
	}
	fmt.Println(strings.Join(parts, " "))
}
