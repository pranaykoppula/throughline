#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    MedianFinder finder;
    string op;
    while (cin >> op) {
        if (op == "add") {
            int x;
            cin >> x;
            finder.addNum(x);
        } else {
            printf("%.5f\n", finder.findMedian());
        }
    }
}
