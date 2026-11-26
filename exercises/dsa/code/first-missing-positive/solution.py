from typing import List


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        # Use the list itself as the table: number v belongs at position v - 1.
        for i in range(n):
            # Keep swapping until this slot holds something that can't be placed,
            # or already sits where it belongs.
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                home = nums[i] - 1
                nums[i], nums[home] = nums[home], nums[i]
        # The first slot not holding its own number marks the gap.
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
