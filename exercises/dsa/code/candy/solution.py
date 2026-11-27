from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        give = [1] * n   # everyone gets at least one
        # Left to right: anyone rated above their left neighbour gets one more than them.
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                give[i] = give[i - 1] + 1
        # Right to left: the same for right neighbours, without undoing the first pass.
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                give[i] = max(give[i], give[i + 1] + 1)
        return sum(give)
