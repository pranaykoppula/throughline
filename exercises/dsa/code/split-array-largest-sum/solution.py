from typing import List


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def days_needed(limit: int) -> int:
            # Fill each day greedily; start a new day when the next job won't fit.
            days, load = 1, 0
            for x in nums:
                if load + x > limit:
                    days += 1
                    load = 0
                load += x
            return days

        # The answer is at least the biggest single job and at most everything in one day.
        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= k:
                hi = mid          # this limit works; try a smaller one
            else:
                lo = mid + 1      # too tight; the answer is bigger
        return lo
