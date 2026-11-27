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
