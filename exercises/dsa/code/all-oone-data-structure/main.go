package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	counts := Constructor()
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()
	var op, key string
	for {
		if _, err := fmt.Fscan(in, &op); err != nil {
			break
		}
		switch op {
		case "inc":
			fmt.Fscan(in, &key)
			counts.Inc(key)
		case "dec":
			fmt.Fscan(in, &key)
			counts.Dec(key)
		case "max":
			fmt.Fprintf(out, "\"%s\"\n", counts.GetMaxKey())
		default:
			fmt.Fprintf(out, "\"%s\"\n", counts.GetMinKey())
		}
	}
}
