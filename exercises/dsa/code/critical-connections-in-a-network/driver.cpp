#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> edges(m, vector<int>(2));
    for (auto& e : edges) cin >> e[0] >> e[1];
    vector<pair<int, int>> out;
    for (auto& e : Solution().criticalConnections(n, edges)) out.push_back({min(e[0], e[1]), max(e[0], e[1])});
    sort(out.begin(), out.end());
    for (auto& [a, b] : out) cout << a << " " << b << "\n";
}
