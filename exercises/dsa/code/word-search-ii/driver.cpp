#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int rows, cols, k;
    cin >> rows >> cols;
    vector<vector<char>> board(rows);
    for (auto& row : board) {
        string line;
        cin >> line;
        row.assign(line.begin(), line.end());
    }
    cin >> k;
    vector<string> words(k);
    for (auto& w : words) cin >> w;
    vector<string> out = Solution().findWords(board, words);
    sort(out.begin(), out.end());
    for (auto& w : out) cout << w << "\n";
}
