class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        // Fill each day greedily; start a new day when the next job won't fit.
        auto daysNeeded = [&](long long limit) {
            int days = 1;
            long long load = 0;
            for (int x : nums) {
                if (load + x > limit) {
                    days++;
                    load = 0;
                }
                load += x;
            }
            return days;
        };
        // The answer is at least the biggest single job and at most everything in one day.
        long long lo = *max_element(nums.begin(), nums.end());
        long long hi = accumulate(nums.begin(), nums.end(), 0LL);
        while (lo < hi) {
            long long mid = lo + (hi - lo) / 2;
            if (daysNeeded(mid) <= k) {
                hi = mid;      // this limit works; try a smaller one
            } else {
                lo = mid + 1;  // too tight; the answer is bigger
            }
        }
        return (int)lo;
    }
};
