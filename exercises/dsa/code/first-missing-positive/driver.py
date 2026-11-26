import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = sys.stdin.read().split()
n = int(data[0])
print(Solution().firstMissingPositive([int(x) for x in data[1:1 + n]]))
