import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = [int(x) for x in sys.stdin.read().split()]
m = data[0]
a = data[1:1 + m]
n = data[1 + m]
b = data[2 + m:2 + m + n]
print(f"{Solution().findMedianSortedArrays(a, b):.5f}")
