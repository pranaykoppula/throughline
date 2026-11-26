import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        // Indices of readings that could still be a window's maximum,
        // with their values in decreasing order from front to back.
        Deque<Integer> candidates = new ArrayDeque<>();
        int[] result = new int[nums.length - k + 1];
        for (int i = 0; i < nums.length; i++) {
            // A new reading outlives every smaller one before it.
            while (!candidates.isEmpty() && nums[candidates.peekLast()] <= nums[i]) {
                candidates.pollLast();
            }
            candidates.addLast(i);
            // The front has slid out of the window.
            if (candidates.peekFirst() <= i - k) {
                candidates.pollFirst();
            }
            if (i >= k - 1) {
                result[i - k + 1] = nums[candidates.peekFirst()];
            }
        }
        return result;
    }
}
