#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    string s;
    getline(cin, s);
    cout << (Solution().isNumber(s) ? "true" : "false") << "\n";
}
