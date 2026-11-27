impl Solution {
    pub fn candy(ratings: Vec<i32>) -> i32 {
        let n = ratings.len();
        let mut give = vec![1; n]; // everyone gets at least one
        // Left to right: anyone rated above their left neighbour gets one more than them.
        for i in 1..n {
            if ratings[i] > ratings[i - 1] {
                give[i] = give[i - 1] + 1;
            }
        }
        // Right to left: the same for right neighbours, without undoing the first pass.
        for i in (0..n.saturating_sub(1)).rev() {
            if ratings[i] > ratings[i + 1] {
                give[i] = give[i].max(give[i + 1] + 1);
            }
        }
        give.iter().sum()
    }
}
