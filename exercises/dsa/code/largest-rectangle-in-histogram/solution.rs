impl Solution {
    pub fn largest_rectangle_area(heights: Vec<i32>) -> i32 {
        let n = heights.len();
        let mut best = 0;
        // Positions of bars still waiting to learn how far right they reach,
        // with heights increasing from bottom to top.
        let mut stack: Vec<usize> = Vec::new();
        for i in 0..=n {
            let h = if i < n { heights[i] } else { 0 }; // a zero at the end settles every bar
            // A shorter bar ends every taller bar still waiting.
            while let Some(&top) = stack.last() {
                if heights[top] < h {
                    break;
                }
                stack.pop();
                // It stretched left to just after the bar now below it in the stack.
                let left = stack.last().map_or(0, |&below| below + 1);
                best = best.max(heights[top] * (i - left) as i32);
            }
            stack.push(i);
        }
        best
    }
}
