import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

lines = sys.stdin.read().split("\n")
print("true" if Solution().isMatch(lines[0], lines[1]) else "false")
