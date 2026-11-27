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
