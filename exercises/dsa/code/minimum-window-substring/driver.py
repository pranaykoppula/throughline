import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

s, t = sys.stdin.read().split()
print(Solution().minWindow(s, t))
