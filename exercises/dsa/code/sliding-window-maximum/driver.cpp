#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> nums(n);
    for (auto& x : nums) cin >> x;
    vector<int> r = Solution().maxSlidingWindow(nums, k);
    for (size_t i = 0; i < r.size(); i++) cout << (i ? " " : "") << r[i];
    cout << "\n";
}
