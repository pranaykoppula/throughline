class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        // Squares we can reach, by the water level needed to reach them; lowest first.
        priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>, greater<>> frontier;
        vector<vector<bool>> seen(n, vector<bool>(n, false));
        frontier.push({grid[0][0], 0, 0});
        seen[0][0] = true;
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!frontier.empty()) {
            auto [level, r, c] = frontier.top();
            frontier.pop();
            if (r == n - 1 && c == n - 1) return level;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc]) {
                    seen[nr][nc] = true;
                    // Reaching the neighbour needs the higher of the two levels.
                    frontier.push({max(level, grid[nr][nc]), nr, nc});
                }
            }
        }
        return -1;
    }
};
