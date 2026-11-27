#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n, q;
    cin >> n;
    vector<string> words(n);
    for (auto& w : words) cin >> w;
    WordFilter search(words);
    cin >> q;
    string out;
    for (int i = 0; i < q; i++) {
        string pref, suff;
        cin >> pref >> suff;
        out += to_string(search.f(pref, suff)) + "\n";
    }
    cout << out;
}
