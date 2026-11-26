use std::collections::VecDeque;

impl Solution {
    pub fn max_sliding_window(nums: Vec<i32>, k: i32) -> Vec<i32> {
        let k = k as usize;
        // Indices of readings that could still be a window's maximum,
        // with their values in decreasing order from front to back.
        let mut candidates: VecDeque<usize> = VecDeque::new();
        let mut result = Vec::with_capacity(nums.len() + 1 - k);
        for i in 0..nums.len() {
            // A new reading outlives every smaller one before it.
            while let Some(&last) = candidates.back() {
                if nums[last] <= nums[i] {
                    candidates.pop_back();
                } else {
                    break;
                }
            }
            candidates.push_back(i);
            // The front has slid out of the window.
            if candidates[0] + k <= i {
                candidates.pop_front();
            }
            if i + 1 >= k {
                result.push(nums[candidates[0]]);
            }
        }
        result
    }
}
