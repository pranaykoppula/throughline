class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        // Search the shorter list, so the halving takes the fewest steps.
        if (nums1.size() > nums2.size()) return findMedianSortedArrays(nums2, nums1);
        const vector<int>& a = nums1;
        const vector<int>& b = nums2;
        int m = a.size(), n = b.size();
        int half = (m + n + 1) / 2;
        int lo = 0, hi = m;
        while (lo <= hi) {
            // Take i from a and the rest of the left half from b.
            int i = (lo + hi) / 2;
            int j = half - i;
            long long aLeft = i > 0 ? a[i - 1] : LLONG_MIN;
            long long aRight = i < m ? a[i] : LLONG_MAX;
            long long bLeft = j > 0 ? b[j - 1] : LLONG_MIN;
            long long bRight = j < n ? b[j] : LLONG_MAX;
            if (aLeft > bRight) {
                hi = i - 1;  // took too many from a
            } else if (bLeft > aRight) {
                lo = i + 1;  // took too few from a
            } else {
                // Every left value is no bigger than every right value.
                if ((m + n) % 2) return (double)max(aLeft, bLeft);
                return (max(aLeft, bLeft) + min(aRight, bRight)) / 2.0;
            }
        }
        return 0.0;  // not reached for sorted inputs
    }
};
