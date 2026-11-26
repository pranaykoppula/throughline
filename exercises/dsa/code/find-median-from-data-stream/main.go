package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	finder := Constructor()
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()
	var op string
	for {
		if _, err := fmt.Fscan(in, &op); err != nil {
			break
		}
		if op == "add" {
			var x int
			fmt.Fscan(in, &x)
			finder.AddNum(x)
		} else {
			fmt.Fprintf(out, "%.5f\n", finder.FindMedian())
		}
	}
}
