import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length, best = 0;
        // Positions of bars still waiting to learn how far right they reach,
        // with heights increasing from bottom to top.
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i <= n; i++) {
            int h = i < n ? heights[i] : 0;  // a zero at the end settles every bar
            // A shorter bar ends every taller bar still waiting.
            while (!stack.isEmpty() && heights[stack.peek()] >= h) {
                int height = heights[stack.pop()];
                // It stretched left to just after the bar now below it in the stack.
                int left = stack.isEmpty() ? 0 : stack.peek() + 1;
                best = Math.max(best, height * (i - left));
            }
            stack.push(i);
        }
        return best;
    }
}
