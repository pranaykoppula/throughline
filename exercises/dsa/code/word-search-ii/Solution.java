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
