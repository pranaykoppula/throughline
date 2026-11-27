impl Solution {
    pub fn count_smaller(nums: Vec<i32>) -> Vec<i32> {
        let n = nums.len();
        let mut counts = vec![0; n];
        let mut order: Vec<usize> = (0..n).collect(); // positions, to be sorted by value
        let mut merged = vec![0usize; n];
        Self::sort_range(&nums, 0, n, &mut order, &mut merged, &mut counts);
        counts
    }

    // Sort order[lo..hi] by value, counting for each position
    // how many smaller values from its right cross to its left.
    fn sort_range(nums: &[i32], lo: usize, hi: usize, order: &mut Vec<usize>, merged: &mut Vec<usize>, counts: &mut Vec<i32>) {
        if hi - lo <= 1 {
            return;
        }
        let mid = (lo + hi) / 2;
        Self::sort_range(nums, lo, mid, order, merged, counts);
        Self::sort_range(nums, mid, hi, order, merged, counts);
        let (mut j, mut k) = (mid, lo);
        for i in lo..mid {
            // Every right-half value placed before this one is smaller and was to its right.
            while j < hi && nums[order[j]] < nums[order[i]] {
                merged[k] = order[j];
                k += 1;
                j += 1;
            }
            counts[order[i]] += (j - mid) as i32;
            merged[k] = order[i];
            k += 1;
        }
        while j < hi {
            merged[k] = order[j];
            k += 1;
            j += 1;
        }
        order[lo..hi].copy_from_slice(&merged[lo..hi]);
    }
}
