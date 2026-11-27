# The shop's search box

An exercise in the category **everything with this prefix**. It's LeetCode 745, [Prefix and Suffix Search](https://leetcode.com/problems/prefix-and-suffix-search/), rated Hard.

## The situation

A hardware shop's catalogue gives every part a short code, and staff often remember only how a code starts and how it ends: "it began with `br` and ended in `kt`, the bracket one". The stock system keeps codes in the order they were added, and newer codes replace older parts, so when several match, staff want the newest. The search box has to answer as fast as people type, all day, for a catalogue of ten thousand codes.

## The problem

Build a structure from a list of words. It must answer queries `f(prefix, suffix)`: the largest index of a word that starts with `prefix` and ends with `suffix`, or −1 if there isn't one. Words and queries are short, up to seven lowercase letters, and there can be many thousands of queries.

For the list `apple`, the query `f("a", "e")` returns 0.

## The question it asks

"Which words have this prefix?" is what a [trie](../../dsa/tries.md) answers. This problem asks about a prefix and a suffix at once, and the trick is to turn the pair into a single prefix. See the row for everything with this prefix in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

For each query, go through every word and check its start and end. It's correct and needs no set-up, but every query costs time in proportion to the whole catalogue, and the search box asks thousands of times ([growth](../../dsa/growth.md)).

The next idea is two tries: one of the words, to find everything with the prefix, and one of the reversed words, for the suffix. Then intersect the two lists. Each trie lookup is fast, but a short prefix like `b` can match thousands of codes, and intersecting two long lists for every keystroke is the slow part again.

## Hints

<details markdown="1"><summary>Hint 1</summary>

A trie answers one prefix question very fast. Can you write the suffix and the prefix together as one string, so that "starts with `br` and ends with `kt`" becomes a single "starts with" question?

</details>

<details markdown="1"><summary>Hint 2</summary>

For the word `apple`, insert `{apple`, `e{apple`, `le{apple`, `ple{apple`, `pple{apple` and `apple{apple` into one trie, where `{` is a character that never appears in a word. Then which string would you look up for the query `f("a", "le")`?

</details>

<details markdown="1"><summary>Hint 3</summary>

Look up `le{a`. Every key that starts with it belongs to a word ending in `le` and starting with `a`. To return the largest index straight away, what should each node store?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

1. **Build one trie.** For each word, at index *i*, and for each of its suffixes, including the empty one and the whole word, insert the key `suffix + "{" + word`. As you walk down inserting, set every node's stored index to *i*. Words are added in order, so each node ends up holding the largest index of any word whose key passes through it.
2. **Answer a query** by walking the trie along `suff + "{" + pref`. If the walk falls off the trie, return −1. Otherwise return the index stored at the node you reach.

**Why it works:** a key `suffix{word` starts with `suff{pref` exactly when `suff` is a suffix of the word, so the key's first part equals it, and `pref` is a prefix of the word, which comes after the `{`. So the node for `suff{pref` sits above the keys of precisely the words that match. The `{` matters because it stops a suffix running on into the prefix.

**Why `{`:** it's the character straight after `z`, so in code it fits in slot 26 of an array of 27 children without a special case.

**The trade:** each word of length *L* adds *L* + 1 keys of up to 2*L* + 1 characters, so building costs about *L*² per word. With words of at most seven letters, that's a fixed amount per word, and every query becomes one walk of at most fifteen steps. This is spending memory and set-up time to make the frequent operation cheap, the same trade an index makes in a database.

**Time:** building, proportional to the number of words × *L*²; each query, proportional to *L*. **Memory:** proportional to the number of words × *L*².

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class WordFilter:
    def __init__(self, words: List[str]):
        # One trie of keys "suffix{word", for every suffix of every word.
        # "{" comes straight after "z", so it can't be confused with a letter.
        # Each node remembers the largest index of any word whose key passes through it.
        self.root = {}
        for index, word in enumerate(words):
            for start in range(len(word) + 1):
                node = self.root
                for ch in word[start:] + "{" + word:
                    node = node.setdefault(ch, {})
                    node["index"] = index   # later words overwrite earlier ones

    def f(self, pref: str, suff: str) -> int:
        # A word with this prefix and suffix has the key "suff{pref..." in the trie.
        node = self.root
        for ch in suff + "{" + pref:
            node = node.get(ch)
            if node is None:
                return -1
        return node["index"]
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class WordFilter {
    // One trie of keys "suffix{word", for every suffix of every word.
    // "{" comes straight after "z", so slot 26 can't be confused with a letter.
    vector<array<int, 27>> next;  // child node numbers, 0 for none
    vector<int> best;             // the largest index of any word whose key passes through

    int newNode() {
        next.push_back({});
        best.push_back(-1);
        return next.size() - 1;
    }

public:
    WordFilter(vector<string>& words) {
        newNode();  // the root
        for (int index = 0; index < (int)words.size(); index++) {
            const string& word = words[index];
            for (size_t start = 0; start <= word.size(); start++) {
                string key = word.substr(start) + "{" + word;
                int node = 0;
                for (char ch : key) {
                    int slot = ch - 'a';
                    if (!next[node][slot]) {
                        int child = newNode();
                        next[node][slot] = child;
                    }
                    node = next[node][slot];
                    best[node] = index;  // later words overwrite earlier ones
                }
            }
        }
    }

    int f(string pref, string suff) {
        // A word with this prefix and suffix has the key "suff{pref..." in the trie.
        int node = 0;
        for (char ch : suff + "{" + pref) {
            node = next[node][ch - 'a'];
            if (!node) return -1;
        }
        return best[node];
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayList;
import java.util.List;

class WordFilter {
    // One trie of keys "suffix{word", for every suffix of every word.
    // "{" comes straight after "z", so slot 26 can't be confused with a letter.
    private final List<int[]> next = new ArrayList<>();   // child node numbers, 0 for none
    private final List<Integer> best = new ArrayList<>(); // largest index of a word passing through

    private int newNode() {
        next.add(new int[27]);
        best.add(-1);
        return next.size() - 1;
    }

    public WordFilter(String[] words) {
        newNode();  // the root
        for (int index = 0; index < words.length; index++) {
            String word = words[index];
            for (int start = 0; start <= word.length(); start++) {
                String key = word.substring(start) + "{" + word;
                int node = 0;
                for (char ch : key.toCharArray()) {
                    int slot = ch - 'a';
                    if (next.get(node)[slot] == 0) {
                        int child = newNode();
                        next.get(node)[slot] = child;
                    }
                    node = next.get(node)[slot];
                    best.set(node, index);  // later words overwrite earlier ones
                }
            }
        }
    }

    public int f(String pref, String suff) {
        // A word with this prefix and suffix has the key "suff{pref..." in the trie.
        int node = 0;
        for (char ch : (suff + "{" + pref).toCharArray()) {
            node = next.get(node)[ch - 'a'];
            if (node == 0) return -1;
        }
        return best.get(node);
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
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
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
// One trie of keys "suffix{word", for every suffix of every word.
// "{" comes straight after "z", so slot 26 can't be confused with a letter.
struct WordFilter {
    next: Vec<[u32; 27]>, // child node numbers, 0 for none
    best: Vec<i32>,       // the largest index of any word whose key passes through
}

impl WordFilter {
    fn new(words: Vec<String>) -> Self {
        let mut t = WordFilter { next: vec![[0; 27]], best: vec![-1] };
        for (index, word) in words.iter().enumerate() {
            for start in 0..=word.len() {
                let key = format!("{}{{{}", &word[start..], word);
                let mut node = 0;
                for b in key.bytes() {
                    let slot = (b - b'a') as usize;
                    if t.next[node][slot] == 0 {
                        t.next.push([0; 27]);
                        t.best.push(-1);
                        t.next[node][slot] = (t.next.len() - 1) as u32;
                    }
                    node = t.next[node][slot] as usize;
                    t.best[node] = index as i32; // later words overwrite earlier ones
                }
            }
        }
        t
    }

    fn f(&self, pref: String, suff: String) -> i32 {
        // A word with this prefix and suffix has the key "suff{pref..." in the trie.
        let mut node = 0;
        for b in format!("{}{{{}", suff, pref).bytes() {
            node = self.next[node][(b - b'a') as usize] as usize;
            if node == 0 {
                return -1;
            }
        }
        self.best[node]
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Forgetting the empty suffix and the whole word.** Insert a key for every suffix from the whole word down to nothing, or queries whose suffix is the whole word fail.
- **Using a separator that can appear in a word.** It must be a character no word contains, or `ab` + suffix can be confused with a longer suffix.
- **Keeping the first index instead of the last.** When the same word appears twice, the later index wins; overwrite as you insert.
- **Intersecting two lists per query.** It works, but it's the slow part of the problem in disguise.

## Related

- The other exercise in this category: [the letter grid](word-search-ii.md) (LeetCode 212).
- Concept pages: [tries](../../dsa/tries.md), [hash tables](../../dsa/hash-tables.md), [B-trees](../../dsa/b-trees.md), [growth](../../dsa/growth.md).
- More practice of the same shape: an autocomplete system that suggests the most frequent past searches for a prefix.
