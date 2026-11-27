package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	line = strings.TrimRight(line, "\n")
	if isNumber(line) {
		fmt.Println("true")
	} else {
		fmt.Println("false")
	}
}
