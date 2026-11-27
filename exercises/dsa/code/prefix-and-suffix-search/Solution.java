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
