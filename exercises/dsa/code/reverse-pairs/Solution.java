class Solution {
    private int[] merged;

    public int reversePairs(int[] nums) {
        int[] a = nums.clone();
        merged = new int[a.length];
        return (int) sortRange(a, 0, a.length);
    }

    // Sort a[lo, hi), and return how many pairs i < j in it have a[i] > 2 * a[j].
    private long sortRange(int[] a, int lo, int hi) {
        if (hi - lo <= 1) return 0;
        int mid = (lo + hi) / 2;
        long count = sortRange(a, lo, mid) + sortRange(a, mid, hi);
        // Both halves are sorted: count the pairs that cross from left to right.
        int j = mid;
        for (int i = lo; i < mid; i++) {
            while (j < hi && (long) a[i] > 2L * a[j]) j++;  // 64 bits: 2 * a[j] can overflow
            count += j - mid;
        }
        // Then merge, as merge sort does.
        int i = lo, r = mid, k = lo;
        while (i < mid || r < hi) {
            if (r == hi || (i < mid && a[i] <= a[r])) merged[k++] = a[i++];
            else merged[k++] = a[r++];
        }
        System.arraycopy(merged, lo, a, lo, hi - lo);
        return count;
    }
}
