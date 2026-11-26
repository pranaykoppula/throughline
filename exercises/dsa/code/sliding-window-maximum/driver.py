import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
nums = [int(x) for x in data[2:2 + n]]
print(" ".join(map(str, Solution().maxSlidingWindow(nums, k))))
