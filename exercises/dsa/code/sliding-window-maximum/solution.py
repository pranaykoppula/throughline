from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # Indices of readings that could still be a window's maximum,
        # with their values in decreasing order from front to back.
        candidates = deque()
        result = []
        for i, x in enumerate(nums):
            # A new reading outlives every smaller one before it,
            # so those can never be the maximum again.
            while candidates and nums[candidates[-1]] <= x:
                candidates.pop()
            candidates.append(i)
            # The front has slid out of the window.
            if candidates[0] <= i - k:
                candidates.popleft()
            if i >= k - 1:
                result.append(nums[candidates[0]])
        return result
