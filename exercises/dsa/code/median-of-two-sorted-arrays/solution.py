from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Search the shorter list, so the halving takes the fewest steps.
        a, b = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)
        m, n = len(a), len(b)
        half = (m + n + 1) // 2
        lo, hi = 0, m
        while lo <= hi:
            # Take i from a and the rest of the left half from b.
            i = (lo + hi) // 2
            j = half - i
            a_left = a[i - 1] if i > 0 else float("-inf")
            a_right = a[i] if i < m else float("inf")
            b_left = b[j - 1] if j > 0 else float("-inf")
            b_right = b[j] if j < n else float("inf")
            if a_left > b_right:
                hi = i - 1        # took too many from a
            elif b_left > a_right:
                lo = i + 1        # took too few from a
            else:
                # Every left value is no bigger than every right value.
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
        raise ValueError("inputs must be sorted")
