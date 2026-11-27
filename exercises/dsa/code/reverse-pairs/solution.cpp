class Solution {
    vector<int> merged;

    // Sort a[lo, hi), and return how many pairs i < j in it have a[i] > 2 * a[j].
    long long sortRange(vector<int>& a, int lo, int hi) {
        if (hi - lo <= 1) return 0;
        int mid = (lo + hi) / 2;
        long long count = sortRange(a, lo, mid) + sortRange(a, mid, hi);
        // Both halves are sorted: count the pairs that cross from left to right.
        int j = mid;
        for (int i = lo; i < mid; i++) {
            while (j < hi && (long long)a[i] > 2LL * a[j]) j++;  // 64 bits: 2 * a[j] can overflow
            count += j - mid;
        }
        // Then merge, as merge sort does.
        merge(a.begin() + lo, a.begin() + mid, a.begin() + mid, a.begin() + hi, merged.begin() + lo);
        copy(merged.begin() + lo, merged.begin() + hi, a.begin() + lo);
        return count;
    }

public:
    int reversePairs(vector<int>& nums) {
        vector<int> a = nums;
        merged.assign(a.size(), 0);
        return (int)sortRange(a, 0, a.size());
    }
};
