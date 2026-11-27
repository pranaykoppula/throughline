from typing import List


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        counts = [0] * len(nums)
        order = list(range(len(nums)))   # positions, to be sorted by value

        def sort(lo: int, hi: int) -> None:
            # Sort order[lo:hi] by value, counting for each position
            # how many smaller values from its right cross to its left.
            if hi - lo <= 1:
                return
            mid = (lo + hi) // 2
            sort(lo, mid)
            sort(mid, hi)
            merged = []
            j = mid
            for i in range(lo, mid):
                # Every right-half value placed before this one is smaller and was to its right.
                while j < hi and nums[order[j]] < nums[order[i]]:
                    merged.append(order[j])
                    j += 1
                counts[order[i]] += j - mid
                merged.append(order[i])
            merged.extend(order[j:hi])
            order[lo:hi] = merged

        sort(0, len(nums))
        return counts
