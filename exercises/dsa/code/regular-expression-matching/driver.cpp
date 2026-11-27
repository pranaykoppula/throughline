#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    string s, p;
    getline(cin, s);
    getline(cin, p);
    cout << (Solution().isMatch(s, p) ? "true" : "false") << "\n";
}
