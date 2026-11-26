#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int m, n;
    cin >> m;
    vector<int> a(m);
    for (auto& x : a) cin >> x;
    cin >> n;
    vector<int> b(n);
    for (auto& x : b) cin >> x;
    printf("%.5f\n", Solution().findMedianSortedArrays(a, b));
}
