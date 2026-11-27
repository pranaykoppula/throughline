#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n;
    cin >> n;
    vector<vector<int>> grid(n, vector<int>(n));
    for (auto& row : grid)
        for (auto& x : row) cin >> x;
    cout << Solution().swimInWater(grid) << "\n";
}
