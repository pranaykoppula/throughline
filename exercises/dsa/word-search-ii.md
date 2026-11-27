# The letter grid

An exercise in the category **everything with this prefix**. It's LeetCode 212, [Word Search II](https://leetcode.com/problems/word-search-ii/), rated Hard.

## The situation

A newspaper runs a daily word puzzle: a grid of letters in which readers trace words through neighbouring squares, up, down, left or right, never using a square twice in the same word. Before each grid is printed, the puzzle editor's software lists every word from a dictionary of tens of thousands that can be found in it, to check the grid isn't too easy or too hard and to print the answers the next day.

## The problem

You're given a grid of lowercase letters and a list of words. Return every word in the list that can be traced in the grid through horizontally or vertically neighbouring squares, using each square at most once per word. Each word should appear once in the answer, in any order.

For the grid

```
o a a n
e t a e
i h k r
i f l v
```

and the words `oath`, `pea`, `eat` and `rain`, the answer is `eat` and `oath`.

## The question it asks

"Does any word start with what I've traced so far?" At every step of tracing, the only thing worth knowing is whether the letters so far are the beginning of some word in the dictionary, and which words. That's a question about everything with this prefix, which is what a [trie](../../dsa/tries.md) answers. See the row for everything with this prefix in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Search the grid once for each word: start at every square and trace the word letter by letter, going back when a letter doesn't fit. It's the natural way to solve the single-word version, and it's correct. But it repeats almost the same search for every word: `oath`, `oat`, `oats` and `oaths` all retrace the same `o-a-t` paths. With tens of thousands of words, the editor's software spends nearly all its time redoing work ([growth](../../dsa/growth.md)).

## Hints

<details markdown="1"><summary>Hint 1</summary>

Turn it round. Instead of searching the grid for each word, walk the grid once and ask, at every step, whether the path so far could still become a word. What would you need to answer that instantly?

</details>

<details markdown="1"><summary>Hint 2</summary>

Put all the words in a trie. Walk the grid and the trie together: moving to a neighbouring square means following that letter's branch in the trie. If there's no branch, no word continues this way, so stop.

</details>

<details markdown="1"><summary>Hint 3</summary>

Once a word has been found, you don't need to find it again. Can you change the trie so later walks don't waste time on branches whose words have all been found?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

1. **Build a trie of the words.** Each node is the prefix spelled by the path to it; mark the nodes where a whole word ends.
2. **Start a walk from every square,** at the trie's root. At each square:
   - Follow the branch for its letter. If there isn't one, go back: nothing in the dictionary starts this way.
   - If the node marks a whole word, add it to the answer and remove the mark, so it's reported once.
   - Mark the square as used, walk into each unused neighbour, then unmark it.
   - **Prune:** if the node now has no children and no word, delete it from its parent. Every word below it has been found.

**Why the trie is the right shape:** the walk only ever asks "what can come next after this prefix?", and the trie answers that in one step for every word at once. All the words that share a beginning share one search. It's the same reason the pharmacy search box on the [tries](../../dsa/tries.md) page keeps up with typing.

**Why the pruning matters:** without it, a grid full of the same letter keeps walking down branches whose words were found long ago. Removing finished branches means the work shrinks as the answer grows.

**Time:** in the worst case, the number of squares × 4 × 3^(*L* − 1), where *L* is the longest word, since each step after the first has at most three new neighbours. The trie and the pruning make it far smaller in practice. **Memory:** the total length of the words, for the trie.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # A trie of the words: each node is a dict of next letters, and "$" marks a whole word.
        root = {}
        for w in words:
            node = root
            for ch in w:
                node = node.setdefault(ch, {})
            node["$"] = w
        rows, cols = len(board), len(board[0])
        found = []

        def walk(r: int, c: int, parent: dict) -> None:
            ch = board[r][c]
            node = parent.get(ch)
            if node is None:
                return              # no word continues this way: stop here
            if "$" in node:
                found.append(node.pop("$"))   # report each word once
            board[r][c] = "#"       # don't reuse this square in the same word
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                    walk(nr, nc, node)
            board[r][c] = ch
            if not node:
                parent.pop(ch)      # every word down here is found: prune the branch

        for r in range(rows):
            for c in range(cols):
                walk(r, c, root)
        return found
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
    struct Node {
        Node* next[26] = {};
        string word;  // set when a whole word ends here
        int children = 0;
    };
    vector<string> found;

    void walk(vector<vector<char>>& board, int r, int c, Node* parent) {
        char ch = board[r][c];
        Node* node = parent->next[ch - 'a'];
        if (!node) return;  // no word continues this way: stop here
        if (!node->word.empty()) {
            found.push_back(node->word);  // report each word once
            node->word.clear();
        }
        board[r][c] = '#';  // don't reuse this square in the same word
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nr < (int)board.size() && nc >= 0 && nc < (int)board[0].size() && board[nr][nc] != '#')
                walk(board, nr, nc, node);
        }
        board[r][c] = ch;
        if (node->children == 0 && node->word.empty()) {
            parent->next[ch - 'a'] = nullptr;  // every word down here is found: prune the branch
            parent->children--;
        }
    }

public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        // A trie of the words.
        Node* root = new Node();
        for (auto& w : words) {
            Node* node = root;
            for (char ch : w) {
                if (!node->next[ch - 'a']) {
                    node->next[ch - 'a'] = new Node();
                    node->children++;
                }
                node = node->next[ch - 'a'];
            }
            node->word = w;
        }
        for (int r = 0; r < (int)board.size(); r++)
            for (int c = 0; c < (int)board[0].size(); c++) walk(board, r, c, root);
        return found;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    private static class Node {
        Node[] next = new Node[26];
        String word;  // set when a whole word ends here
        int children = 0;
    }

    private final List<String> found = new ArrayList<>();

    public List<String> findWords(char[][] board, String[] words) {
        // A trie of the words.
        Node root = new Node();
        for (String w : words) {
            Node node = root;
            for (char ch : w.toCharArray()) {
                if (node.next[ch - 'a'] == null) {
                    node.next[ch - 'a'] = new Node();
                    node.children++;
                }
                node = node.next[ch - 'a'];
            }
            node.word = w;
        }
        for (int r = 0; r < board.length; r++)
            for (int c = 0; c < board[0].length; c++) walk(board, r, c, root);
        return found;
    }

    private void walk(char[][] board, int r, int c, Node parent) {
        char ch = board[r][c];
        Node node = parent.next[ch - 'a'];
        if (node == null) return;  // no word continues this way: stop here
        if (node.word != null) {
            found.add(node.word);  // report each word once
            node.word = null;
        }
        board[r][c] = '#';  // don't reuse this square in the same word
        int[][] steps = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int[] d : steps) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < board.length && nc >= 0 && nc < board[0].length && board[nr][nc] != '#')
                walk(board, nr, nc, node);
        }
        board[r][c] = ch;
        if (node.children == 0 && node.word == null) {
            parent.next[ch - 'a'] = null;  // every word down here is found: prune the branch
            parent.children--;
        }
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
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
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
#[derive(Default)]
struct TrieNode {
    next: [Option<Box<TrieNode>>; 26],
    word: Option<String>, // set when a whole word ends here
}

impl Solution {
    pub fn find_words(board: Vec<Vec<char>>, words: Vec<String>) -> Vec<String> {
        // A trie of the words.
        let mut root = TrieNode::default();
        for w in words {
            let mut node = &mut root;
            for b in w.bytes() {
                node = node.next[(b - b'a') as usize].get_or_insert_with(Default::default);
            }
            node.word = Some(w);
        }
        let mut board: Vec<Vec<u8>> = board.into_iter().map(|row| row.into_iter().map(|c| c as u8).collect()).collect();
        let mut found = Vec::new();
        for r in 0..board.len() {
            for c in 0..board[0].len() {
                Self::walk(&mut board, r, c, &mut root, &mut found);
            }
        }
        found
    }

    fn walk(board: &mut Vec<Vec<u8>>, r: usize, c: usize, parent: &mut TrieNode, found: &mut Vec<String>) {
        let ch = board[r][c];
        let slot = (ch - b'a') as usize;
        let node = match parent.next[slot].as_mut() {
            Some(node) => node,
            None => return, // no word continues this way: stop here
        };
        if let Some(w) = node.word.take() {
            found.push(w); // report each word once
        }
        board[r][c] = b'#'; // don't reuse this square in the same word
        let (rows, cols) = (board.len() as i32, board[0].len() as i32);
        for (dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let (nr, nc) = (r as i32 + dr, c as i32 + dc);
            if nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr as usize][nc as usize] != b'#' {
                Self::walk(board, nr as usize, nc as usize, node, found);
            }
        }
        board[r][c] = ch;
        if node.word.is_none() && node.next.iter().all(|n| n.is_none()) {
            parent.next[slot] = None; // every word down here is found: prune the branch
        }
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Reporting a word twice.** A word can be traced in more than one place; remove its mark once it's found.
- **Reusing a square.** Mark the square as used before walking on, and unmark it when you come back.
- **Building a set of every path's letters.** Recording every prefix the grid can spell, and then looking up each word, explodes long before the trie does.
- **Forgetting to restore the grid.** If you mark squares by overwriting them, put the letter back before returning.

## Related

- The other exercise in this category: [the shop's search box](prefix-and-suffix-search.md) (LeetCode 745).
- Concept pages: [tries](../../dsa/tries.md), [hash tables](../../dsa/hash-tables.md), [growth](../../dsa/growth.md).
- More practice of the same shape: the single-word version (Word Search, LeetCode 79), and finding all words that can be built from other words in a list.
