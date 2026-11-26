use std::collections::BinaryHeap;

impl Solution {
    pub fn get_skyline(buildings: Vec<Vec<i32>>) -> Vec<Vec<i32>> {
        // Every place the outline can change: a building's left or right edge.
        let mut edges: Vec<i32> = buildings.iter().flat_map(|b| [b[0], b[1]]).collect();
        edges.sort_unstable();
        edges.dedup();

        let mut skyline: Vec<Vec<i32>> = Vec::new();
        // (height, right edge) of buildings that have started; tallest on top.
        let mut standing: BinaryHeap<(i32, i32)> = BinaryHeap::new();
        let mut i = 0;
        for x in edges {
            // Buildings that start here join the heap (the input is sorted by left edge).
            while i < buildings.len() && buildings[i][0] <= x {
                standing.push((buildings[i][2], buildings[i][1]));
                i += 1;
            }
            // The tallest might have ended already; drop it only when it's on top.
            while let Some(&(_, right)) = standing.peek() {
                if right <= x {
                    standing.pop();
                } else {
                    break;
                }
            }
            let height = standing.peek().map_or(0, |&(h, _)| h);
            if skyline.last().map_or(true, |p| p[1] != height) {
                skyline.push(vec![x, height]);
            }
        }
        skyline
    }
}
