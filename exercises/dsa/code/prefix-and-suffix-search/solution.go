package main

// One trie of keys "suffix{word", for every suffix of every word.
// "{" comes straight after "z", so slot 26 can't be confused with a letter.
type WordFilter struct {
	next [][27]int32 // child node numbers, 0 for none
	best []int       // the largest index of any word whose key passes through
}

func Constructor(words []string) WordFilter {
	t := WordFilter{next: make([][27]int32, 1), best: []int{-1}}
	for index, word := range words {
		for start := 0; start <= len(word); start++ {
			key := word[start:] + "{" + word
			node := 0
			for i := 0; i < len(key); i++ {
				slot := key[i] - 'a'
				if t.next[node][slot] == 0 {
					t.next = append(t.next, [27]int32{})
					t.best = append(t.best, -1)
					t.next[node][slot] = int32(len(t.next) - 1)
				}
				node = int(t.next[node][slot])
				t.best[node] = index // later words overwrite earlier ones
			}
		}
	}
	return t
}

func (this *WordFilter) F(pref string, suff string) int {
	// A word with this prefix and suffix has the key "suff{pref..." in the trie.
	key := suff + "{" + pref
	node := 0
	for i := 0; i < len(key); i++ {
		node = int(this.next[node][key[i]-'a'])
		if node == 0 {
			return -1
		}
	}
	return this.best[node]
}
