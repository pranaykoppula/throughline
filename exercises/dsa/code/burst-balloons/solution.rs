impl Solution {
    pub fn max_coins(nums: Vec<i32>) -> i32 {
        // Pretend there's a balloon worth 1 at each end that can't be burst.
        let mut v = vec![1];
        v.extend(nums);
        v.push(1);
        let n = v.len();
        // best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
        // while lo and hi themselves are still standing.
        let mut best = vec![vec![0i32; n]; n];
        for width in 2..n {
            for lo in 0..n - width {
                let hi = lo + width;
                // Choose the balloon k to burst LAST in this stretch: by then its
                // neighbours are lo and hi, and the two sides were settled independently.
                for k in lo + 1..hi {
                    best[lo][hi] = best[lo][hi].max(best[lo][k] + v[lo] * v[k] * v[hi] + best[k][hi]);
                }
            }
        }
        best[0][n - 1]
    }
}
