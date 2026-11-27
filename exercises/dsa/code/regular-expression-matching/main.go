package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	s, _ := in.ReadString('\n')
	p, _ := in.ReadString('\n')
	s = strings.TrimRight(s, "\n")
	p = strings.TrimRight(p, "\n")
	if isMatch(s, p) {
		fmt.Println("true")
	} else {
		fmt.Println("false")
	}
}
