class Solution {
    vector<int> counts, order, merged;

    // Sort order[lo, hi) by value, counting for each position
    // how many smaller values from its right cross to its left.
    void sortRange(const vector<int>& nums, int lo, int hi) {
        if (hi - lo <= 1) return;
        int mid = (lo + hi) / 2;
        sortRange(nums, lo, mid);
        sortRange(nums, mid, hi);
        int j = mid, k = lo;
        for (int i = lo; i < mid; i++) {
            // Every right-half value placed before this one is smaller and was to its right.
            while (j < hi && nums[order[j]] < nums[order[i]]) merged[k++] = order[j++];
            counts[order[i]] += j - mid;
            merged[k++] = order[i];
        }
        while (j < hi) merged[k++] = order[j++];
        copy(merged.begin() + lo, merged.begin() + hi, order.begin() + lo);
    }

public:
    vector<int> countSmaller(vector<int>& nums) {
        int n = nums.size();
        counts.assign(n, 0);
        merged.assign(n, 0);
        order.resize(n);
        iota(order.begin(), order.end(), 0);  // positions, to be sorted by value
        sortRange(nums, 0, n);
        return counts;
    }
};
