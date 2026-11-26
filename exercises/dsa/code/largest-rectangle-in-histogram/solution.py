from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        best = 0
        # Positions of bars still waiting to learn how far right they reach,
        # with heights increasing from bottom to top.
        stack = []
        for i, h in enumerate(heights + [0]):    # a zero at the end settles every bar
            # A shorter bar ends every taller bar still waiting.
            while stack and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                # It stretched left to just after the bar now below it in the stack.
                left = stack[-1] + 1 if stack else 0
                best = max(best, height * (i - left))
            stack.append(i)
        return best
