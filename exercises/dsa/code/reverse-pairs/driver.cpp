#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (auto& x : nums) cin >> x;
    cout << Solution().reversePairs(nums) << "\n";
}
