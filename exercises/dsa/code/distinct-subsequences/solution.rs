impl Solution {
    pub fn num_distinct(s: String, t: String) -> i32 {
        let (s, t) = (s.as_bytes(), t.as_bytes());
        let m = t.len();
        // ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
        // Wrapping addition can't panic; the final answer fits in 32 bits, and wrapping keeps
        // every count correct modulo 2^64, so the answer comes out right.
        let mut ways = vec![0u64; m + 1];
        ways[0] = 1; // the empty prefix of t, in exactly one way
        for &ch in s {
            // Go right to left, so each character of s is used at most once per way.
            for j in (1..=m).rev() {
                if t[j - 1] == ch {
                    ways[j] = ways[j].wrapping_add(ways[j - 1]);
                }
            }
        }
        ways[m] as i32
    }
}
