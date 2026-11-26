import java.util.PriorityQueue;

class Solution {
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        // Squares we can reach, by the water level needed to reach them; lowest first.
        PriorityQueue<int[]> frontier = new PriorityQueue<>((p, q) -> Integer.compare(p[0], q[0]));
        boolean[][] seen = new boolean[n][n];
        frontier.add(new int[] {grid[0][0], 0, 0});
        seen[0][0] = true;
        int[][] steps = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!frontier.isEmpty()) {
            int[] top = frontier.poll();
            int level = top[0], r = top[1], c = top[2];
            if (r == n - 1 && c == n - 1) return level;
            for (int[] s : steps) {
                int nr = r + s[0], nc = c + s[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc]) {
                    seen[nr][nc] = true;
                    // Reaching the neighbour needs the higher of the two levels.
                    frontier.add(new int[] {Math.max(level, grid[nr][nc]), nr, nc});
                }
            }
        }
        return -1;
    }
}
