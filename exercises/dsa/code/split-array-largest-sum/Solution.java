class Solution {
    public int splitArray(int[] nums, int k) {
        // The answer is at least the biggest single job and at most everything in one day.
        long lo = 0, hi = 0;
        for (int x : nums) {
            lo = Math.max(lo, x);
            hi += x;
        }
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (daysNeeded(nums, mid) <= k) {
                hi = mid;      // this limit works; try a smaller one
            } else {
                lo = mid + 1;  // too tight; the answer is bigger
            }
        }
        return (int) lo;
    }

    // Fill each day greedily; start a new day when the next job won't fit.
    private int daysNeeded(int[] nums, long limit) {
        int days = 1;
        long load = 0;
        for (int x : nums) {
            if (load + x > limit) {
                days++;
                load = 0;
            }
            load += x;
        }
        return days;
    }
}
