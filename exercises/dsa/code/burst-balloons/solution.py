from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        # Pretend there's a balloon worth 1 at each end that can't be burst.
        v = [1] + nums + [1]
        n = len(v)
        # best[lo][hi]: the most coins from bursting every balloon strictly between lo and hi,
        # while lo and hi themselves are still standing.
        best = [[0] * n for _ in range(n)]
        for width in range(2, n):
            for lo in range(n - width):
                hi = lo + width
                # Choose the balloon k to burst LAST in this stretch: by then its
                # neighbours are lo and hi, and the two sides were settled independently.
                best[lo][hi] = max(
                    best[lo][k] + v[lo] * v[k] * v[hi] + best[k][hi] for k in range(lo + 1, hi)
                )
        return best[0][n - 1]
