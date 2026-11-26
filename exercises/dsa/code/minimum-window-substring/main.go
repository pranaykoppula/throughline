package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var s, t string
	fmt.Fscan(in, &s, &t)
	fmt.Println(minWindow(s, t))
}
