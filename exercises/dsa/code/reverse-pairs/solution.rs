impl Solution {
    pub fn reverse_pairs(nums: Vec<i32>) -> i32 {
        let mut a: Vec<i64> = nums.iter().map(|&x| x as i64).collect(); // 64 bits: 2 * x can overflow i32
        let mut merged = vec![0i64; a.len()];
        let n = a.len();
        Self::sort_range(&mut a, &mut merged, 0, n) as i32
    }

    // Sort a[lo..hi], and return how many pairs i < j in it have a[i] > 2 * a[j].
    fn sort_range(a: &mut Vec<i64>, merged: &mut Vec<i64>, lo: usize, hi: usize) -> i64 {
        if hi - lo <= 1 {
            return 0;
        }
        let mid = (lo + hi) / 2;
        let mut count = Self::sort_range(a, merged, lo, mid) + Self::sort_range(a, merged, mid, hi);
        // Both halves are sorted: count the pairs that cross from left to right.
        let mut j = mid;
        for i in lo..mid {
            while j < hi && a[i] > 2 * a[j] {
                j += 1;
            }
            count += (j - mid) as i64;
        }
        // Then merge, as merge sort does.
        let (mut i, mut r, mut k) = (lo, mid, lo);
        while i < mid || r < hi {
            if r == hi || (i < mid && a[i] <= a[r]) {
                merged[k] = a[i];
                i += 1;
            } else {
                merged[k] = a[r];
                r += 1;
            }
            k += 1;
        }
        a[lo..hi].copy_from_slice(&merged[lo..hi]);
        count
    }
}
