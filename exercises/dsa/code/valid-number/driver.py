import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

s = sys.stdin.readline().rstrip("\n")
print("true" if Solution().isNumber(s) else "false")
