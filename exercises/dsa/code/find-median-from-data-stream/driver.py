import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import MedianFinder

finder = MedianFinder()
out = []
for line in sys.stdin.read().splitlines():
    parts = line.split()
    if not parts:
        continue
    if parts[0] == "add":
        finder.addNum(int(parts[1]))
    else:
        out.append(f"{finder.findMedian():.5f}")
print("\n".join(out))
