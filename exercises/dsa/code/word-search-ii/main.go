package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	var rows, cols, k int
	fmt.Fscan(in, &rows, &cols)
	board := make([][]byte, rows)
	for r := range board {
		var line string
		fmt.Fscan(in, &line)
		board[r] = []byte(line)
	}
	fmt.Fscan(in, &k)
	words := make([]string, k)
	for i := range words {
		fmt.Fscan(in, &words[i])
	}
	out := findWords(board, words)
	sort.Strings(out)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	for _, word := range out {
		fmt.Fprintln(w, word)
	}
}
