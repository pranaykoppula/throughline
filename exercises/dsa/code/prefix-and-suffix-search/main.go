package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var n, q int
	fmt.Fscan(in, &n)
	words := make([]string, n)
	for i := range words {
		fmt.Fscan(in, &words[i])
	}
	search := Constructor(words)
	fmt.Fscan(in, &q)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()
	for i := 0; i < q; i++ {
		var pref, suff string
		fmt.Fscan(in, &pref, &suff)
		fmt.Fprintln(out, search.F(pref, suff))
	}
}
