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
