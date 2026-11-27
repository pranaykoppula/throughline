#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int capacity;
    cin >> capacity;
    LFUCache cache(capacity);
    string op;
    string out;
    while (cin >> op) {
        if (op == "get") {
            int k;
            cin >> k;
            out += to_string(cache.get(k)) + "\n";
        } else {
            int k, v;
            cin >> k >> v;
            cache.put(k, v);
        }
    }
    cout << out;
}
