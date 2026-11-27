import java.util.ArrayList;
import java.util.List;

class Solution {
    private int[] counts, order, merged;

    public List<Integer> countSmaller(int[] nums) {
        int n = nums.length;
        counts = new int[n];
        merged = new int[n];
        order = new int[n];  // positions, to be sorted by value
        for (int i = 0; i < n; i++) order[i] = i;
        sortRange(nums, 0, n);
        List<Integer> result = new ArrayList<>();
        for (int c : counts) result.add(c);
        return result;
    }

    // Sort order[lo, hi) by value, counting for each position
    // how many smaller values from its right cross to its left.
    private void sortRange(int[] nums, int lo, int hi) {
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
        System.arraycopy(merged, lo, order, lo, hi - lo);
    }
}
