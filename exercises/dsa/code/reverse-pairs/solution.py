from typing import List


class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        def sort(a: List[int]) -> int:
            # Sort a, and return how many pairs i < j in it have a[i] > 2 * a[j].
            if len(a) <= 1:
                return 0
            mid = len(a) // 2
            left, right = a[:mid], a[mid:]
            count = sort(left) + sort(right)
            # Both halves are sorted: count the pairs that cross from left to right.
            j = 0
            for x in left:
                while j < len(right) and x > 2 * right[j]:
                    j += 1
                count += j   # right[0..j) are all small enough for x
            # Then merge, as merge sort does.
            i = j = k = 0
            while i < len(left) or j < len(right):
                if j == len(right) or (i < len(left) and left[i] <= right[j]):
                    a[k] = left[i]
                    i += 1
                else:
                    a[k] = right[j]
                    j += 1
                k += 1
            return count

        return sort(list(nums))
