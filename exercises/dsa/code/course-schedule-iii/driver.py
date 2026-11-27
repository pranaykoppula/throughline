import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = [int(x) for x in sys.stdin.read().split()]
n = data[0]
courses = [[data[1 + 2 * i], data[2 + 2 * i]] for i in range(n)]
print(Solution().scheduleCourse(courses))
