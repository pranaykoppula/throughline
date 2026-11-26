from collections import deque
from typing import List


class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        # prefix[j] - prefix[i] is the total of days i .. j-1.
        prefix = [0]
        for x in nums:
            prefix.append(prefix[-1] + x)
        best = len(nums) + 1
        # Start points worth keeping, with prefix totals increasing from front to back.
        starts = deque()
        for j, total in enumerate(prefix):
            # The oldest start that already reaches k gives its best answer now.
            while starts and total - prefix[starts[0]] >= k:
                best = min(best, j - starts.popleft())
            # A start with a total at least as high as this one is never better.
            while starts and prefix[starts[-1]] >= total:
                starts.pop()
            starts.append(j)
        return best if best <= len(nums) else -1
