class Solution {
    public int maxCoins(int[] nums) {
        // Pretend there's a balloon worth 1 at each end that can't be burst.
        int n = nums.length + 2;
        int[] v = new int[n];
        v[0] = v[n - 1] = 1;
        System.arraycopy(nums, 0, v, 1, nums.length);
        // best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
        // while lo and hi themselves are still standing.
        int[][] best = new int[n][n];
        for (int width = 2; width < n; width++) {
            for (int lo = 0; lo + width < n; lo++) {
                int hi = lo + width;
                // Choose the balloon k to burst LAST in this stretch: by then its
                // neighbours are lo and hi, and the two sides were settled independently.
                for (int k = lo + 1; k < hi; k++) {
                    best[lo][hi] = Math.max(best[lo][hi], best[lo][k] + v[lo] * v[k] * v[hi] + best[k][hi]);
                }
            }
        }
        return best[0][n - 1];
    }
}
