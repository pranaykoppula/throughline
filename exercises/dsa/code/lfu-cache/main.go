package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var capacity int
	fmt.Fscan(in, &capacity)
	cache := Constructor(capacity)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()
	var op string
	for {
		if _, err := fmt.Fscan(in, &op); err != nil {
			break
		}
		if op == "get" {
			var k int
			fmt.Fscan(in, &k)
			fmt.Fprintln(out, cache.Get(k))
		} else {
			var k, v int
			fmt.Fscan(in, &k, &v)
			cache.Put(k, v)
		}
	}
}
