import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int shortestSubarray(int[] nums, int k) {
        int n = nums.length;
        // prefix[j] - prefix[i] is the total of days i .. j-1.
        long[] prefix = new long[n + 1];
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
        int best = n + 1;
        // Start points worth keeping, with prefix totals increasing from front to back.
        Deque<Integer> starts = new ArrayDeque<>();
        for (int j = 0; j <= n; j++) {
            // The oldest start that already reaches k gives its best answer now.
            while (!starts.isEmpty() && prefix[j] - prefix[starts.peekFirst()] >= k) {
                best = Math.min(best, j - starts.pollFirst());
            }
            // A start with a total at least as high as this one is never better.
            while (!starts.isEmpty() && prefix[starts.peekLast()] >= prefix[j]) {
                starts.pollLast();
            }
            starts.addLast(j);
        }
        return best <= n ? best : -1;
    }
}
