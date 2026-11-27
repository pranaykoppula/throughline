#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    AllOne counts;
    string op, key, out;
    while (cin >> op) {
        if (op == "inc") {
            cin >> key;
            counts.inc(key);
        } else if (op == "dec") {
            cin >> key;
            counts.dec(key);
        } else if (op == "max") {
            out += "\"" + counts.getMaxKey() + "\"\n";
        } else {
            out += "\"" + counts.getMinKey() + "\"\n";
        }
    }
    cout << out;
}
