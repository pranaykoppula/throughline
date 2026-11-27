package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var n int
	fmt.Fscan(in, &n)
	courses := make([][]int, n)
	for i := range courses {
		courses[i] = make([]int, 2)
		fmt.Fscan(in, &courses[i][0], &courses[i][1])
	}
	fmt.Println(scheduleCourse(courses))
}
