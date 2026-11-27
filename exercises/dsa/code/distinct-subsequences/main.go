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
	t, _ := in.ReadString('\n')
	fmt.Println(numDistinct(strings.TrimRight(s, "\n"), strings.TrimRight(t, "\n")))
}
