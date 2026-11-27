import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = [int(x) for x in sys.stdin.read().split()]
print(Solution().candy(data[1:1 + data[0]]))
