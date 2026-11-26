#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n;
    cin >> n;
    vector<vector<int>> buildings(n, vector<int>(3));
    for (auto& b : buildings) cin >> b[0] >> b[1] >> b[2];
    for (auto& p : Solution().getSkyline(buildings)) cout << p[0] << " " << p[1] << "\n";
}
