use std::collections::VecDeque;

impl Solution {
    pub fn shortest_subarray(nums: Vec<i32>, k: i32) -> i32 {
        let n = nums.len();
        // prefix[j] - prefix[i] is the total of days i .. j-1.
        let mut prefix = vec![0i64; n + 1];
        for i in 0..n {
            prefix[i + 1] = prefix[i] + nums[i] as i64;
        }
        let k = k as i64;
        let mut best = n + 1;
        // Start points worth keeping, with prefix totals increasing from front to back.
        let mut starts: VecDeque<usize> = VecDeque::new();
        for j in 0..=n {
            // The oldest start that already reaches k gives its best answer now.
            while let Some(&first) = starts.front() {
                if prefix[j] - prefix[first] >= k {
                    best = best.min(j - first);
                    starts.pop_front();
                } else {
                    break;
                }
            }
            // A start with a total at least as high as this one is never better.
            while let Some(&last) = starts.back() {
                if prefix[last] >= prefix[j] {
                    starts.pop_back();
                } else {
                    break;
                }
            }
            starts.push_back(j);
        }
        if best <= n { best as i32 } else { -1 }
    }
}
