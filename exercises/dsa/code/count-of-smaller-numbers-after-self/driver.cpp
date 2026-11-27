#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (auto& x : nums) cin >> x;
    vector<int> out = Solution().countSmaller(nums);
    string text;
    for (int i = 0; i < n; i++) text += (i ? " " : "") + to_string(out[i]);
    cout << text << "\n";
}
