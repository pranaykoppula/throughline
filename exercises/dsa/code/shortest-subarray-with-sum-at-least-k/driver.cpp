#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> nums(n);
    for (auto& x : nums) cin >> x;
    cout << Solution().shortestSubarray(nums, k) << "\n";
}
