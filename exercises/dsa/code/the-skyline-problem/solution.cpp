class Solution {
public:
    vector<vector<int>> getSkyline(vector<vector<int>>& buildings) {
        // Every place the outline can change: a building's left or right edge.
        vector<int> edges;
        for (auto& b : buildings) {
            edges.push_back(b[0]);
            edges.push_back(b[1]);
        }
        sort(edges.begin(), edges.end());
        edges.erase(unique(edges.begin(), edges.end()), edges.end());

        vector<vector<int>> skyline;
        priority_queue<pair<int, int>> standing;  // (height, right edge); tallest on top
        size_t i = 0;
        for (int x : edges) {
            // Buildings that start here join the heap (the input is sorted by left edge).
            while (i < buildings.size() && buildings[i][0] <= x) {
                standing.push({buildings[i][2], buildings[i][1]});
                i++;
            }
            // The tallest might have ended already; drop it only when it's on top.
            while (!standing.empty() && standing.top().second <= x) {
                standing.pop();
            }
            int height = standing.empty() ? 0 : standing.top().first;
            if (skyline.empty() || skyline.back()[1] != height) {
                skyline.push_back({x, height});
            }
        }
        return skyline;
    }
};
