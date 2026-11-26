class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        // Search the shorter array, so the halving takes the fewest steps.
        if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
        int[] a = nums1, b = nums2;
        int m = a.length, n = b.length;
        int half = (m + n + 1) / 2;
        int lo = 0, hi = m;
        while (lo <= hi) {
            // Take i from a and the rest of the left half from b.
            int i = (lo + hi) / 2;
            int j = half - i;
            long aLeft = i > 0 ? a[i - 1] : Long.MIN_VALUE;
            long aRight = i < m ? a[i] : Long.MAX_VALUE;
            long bLeft = j > 0 ? b[j - 1] : Long.MIN_VALUE;
            long bRight = j < n ? b[j] : Long.MAX_VALUE;
            if (aLeft > bRight) {
                hi = i - 1;  // took too many from a
            } else if (bLeft > aRight) {
                lo = i + 1;  // took too few from a
            } else {
                // Every left value is no bigger than every right value.
                if ((m + n) % 2 == 1) return Math.max(aLeft, bLeft);
                return (Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2.0;
            }
        }
        return 0.0;  // not reached for sorted inputs
    }
}
