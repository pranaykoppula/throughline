class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        # ways[j]: in how many ways the part of s read so far contains t[:j] as a subsequence.
        ways = [1] + [0] * len(t)   # the empty prefix of t, in exactly one way
        for ch in s:
            # Go right to left, so each character of s is used at most once per way.
            for j in range(len(t), 0, -1):
                if t[j - 1] == ch:
                    ways[j] += ways[j - 1]   # every way to make t[:j-1], finished with this ch
        return ways[len(t)]
