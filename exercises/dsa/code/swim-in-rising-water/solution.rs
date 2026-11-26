use std::cmp::Reverse;
use std::collections::BinaryHeap;

impl Solution {
    pub fn swim_in_water(grid: Vec<Vec<i32>>) -> i32 {
        let n = grid.len();
        // Squares we can reach, by the water level needed to reach them; lowest first.
        let mut frontier = BinaryHeap::new();
        let mut seen = vec![vec![false; n]; n];
        frontier.push(Reverse((grid[0][0], 0usize, 0usize)));
        seen[0][0] = true;
        let steps: [(i32, i32); 4] = [(1, 0), (-1, 0), (0, 1), (0, -1)];
        while let Some(Reverse((level, r, c))) = frontier.pop() {
            if r == n - 1 && c == n - 1 {
                return level;
            }
            for (dr, dc) in steps {
                let (nr, nc) = (r as i32 + dr, c as i32 + dc);
                if nr < 0 || nc < 0 || nr >= n as i32 || nc >= n as i32 {
                    continue;
                }
                let (nr, nc) = (nr as usize, nc as usize);
                if !seen[nr][nc] {
                    seen[nr][nc] = true;
                    // Reaching the neighbour needs the higher of the two levels.
                    frontier.push(Reverse((level.max(grid[nr][nc]), nr, nc)));
                }
            }
        }
        -1
    }
}
