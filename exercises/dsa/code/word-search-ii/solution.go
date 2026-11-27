package main

type trieNode struct {
	next     [26]*trieNode
	word     string // set when a whole word ends here
	children int
}

func findWords(board [][]byte, words []string) []string {
	// A trie of the words.
	root := &trieNode{}
	for _, w := range words {
		node := root
		for i := 0; i < len(w); i++ {
			ch := w[i] - 'a'
			if node.next[ch] == nil {
				node.next[ch] = &trieNode{}
				node.children++
			}
			node = node.next[ch]
		}
		node.word = w
	}
	rows, cols := len(board), len(board[0])
	found := []string{}
	var walk func(r, c int, parent *trieNode)
	walk = func(r, c int, parent *trieNode) {
		ch := board[r][c]
		node := parent.next[ch-'a']
		if node == nil {
			return // no word continues this way: stop here
		}
		if node.word != "" {
			found = append(found, node.word) // report each word once
			node.word = ""
		}
		board[r][c] = '#' // don't reuse this square in the same word
		for _, d := range [4][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr][nc] != '#' {
				walk(nr, nc, node)
			}
		}
		board[r][c] = ch
		if node.children == 0 && node.word == "" {
			parent.next[ch-'a'] = nil // every word down here is found: prune the branch
			parent.children--
		}
	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			walk(r, c, root)
		}
	}
	return found
}
