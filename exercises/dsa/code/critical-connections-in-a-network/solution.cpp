class Solution {
    vector<vector<int>> links, bridges;
    vector<int> found, low;  // when each server was first reached; earliest reachable by a back route
    int clock = 0;

    void walk(int u, int parent) {
        found[u] = low[u] = clock++;
        for (int v : links[u]) {
            if (v == parent) continue;
            if (found[v] == -1) {
                walk(v, u);
                low[u] = min(low[u], low[v]);
                // Nothing below v reaches back above it: the link is critical.
                if (low[v] > found[u]) bridges.push_back({u, v});
            } else {
                low[u] = min(low[u], found[v]);  // a back route to an earlier server
            }
        }
    }

public:
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        links.assign(n, {});
        for (auto& e : connections) {
            links[e[0]].push_back(e[1]);
            links[e[1]].push_back(e[0]);
        }
        found.assign(n, -1);
        low.assign(n, 0);
        for (int i = 0; i < n; i++)
            if (found[i] == -1) walk(i, -1);
        return bridges;
    }
};
