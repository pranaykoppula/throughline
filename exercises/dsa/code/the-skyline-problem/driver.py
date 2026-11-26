import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = [int(x) for x in sys.stdin.read().split()]
n = data[0]
buildings = [data[1 + 3 * i:4 + 3 * i] for i in range(n)]
print("\n".join(f"{x} {h}" for x, h in Solution().getSkyline(buildings)))
