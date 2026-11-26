impl Solution {
    pub fn split_array(nums: Vec<i32>, k: i32) -> i32 {
        // Fill each day greedily; start a new day when the next job won't fit.
        let days_needed = |limit: i64| -> i32 {
            let (mut days, mut load) = (1, 0i64);
            for &x in &nums {
                if load + x as i64 > limit {
                    days += 1;
                    load = 0;
                }
                load += x as i64;
            }
            days
        };
        // The answer is at least the biggest single job and at most everything in one day.
        let mut lo = *nums.iter().max().unwrap() as i64;
        let mut hi: i64 = nums.iter().map(|&x| x as i64).sum();
        while lo < hi {
            let mid = lo + (hi - lo) / 2;
            if days_needed(mid) <= k {
                hi = mid; // this limit works; try a smaller one
            } else {
                lo = mid + 1; // too tight; the answer is bigger
            }
        }
        lo as i32
    }
}
