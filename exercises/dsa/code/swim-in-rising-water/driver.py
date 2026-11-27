import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = [int(x) for x in sys.stdin.read().split()]
n = data[0]
grid = [data[1 + r * n:1 + (r + 1) * n] for r in range(n)]
print(Solution().swimInWater(grid))
