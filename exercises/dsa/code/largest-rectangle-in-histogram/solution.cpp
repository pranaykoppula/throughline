class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size(), best = 0;
        // Positions of bars still waiting to learn how far right they reach,
        // with heights increasing from bottom to top.
        vector<int> stack;
        for (int i = 0; i <= n; i++) {
            int h = i < n ? heights[i] : 0;  // a zero at the end settles every bar
            // A shorter bar ends every taller bar still waiting.
            while (!stack.empty() && heights[stack.back()] >= h) {
                int height = heights[stack.back()];
                stack.pop_back();
                // It stretched left to just after the bar now below it in the stack.
                int left = stack.empty() ? 0 : stack.back() + 1;
                best = max(best, height * (i - left));
            }
            stack.push_back(i);
        }
        return best;
    }
};
