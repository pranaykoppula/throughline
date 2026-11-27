import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

print(Solution().calculate(sys.stdin.read().rstrip("\n")))
