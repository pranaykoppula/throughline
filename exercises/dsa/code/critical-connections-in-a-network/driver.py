import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = [int(x) for x in sys.stdin.read().split()]
n, m = data[0], data[1]
edges = [[data[2 + 2 * i], data[3 + 2 * i]] for i in range(m)]
result = sorted(tuple(sorted(e)) for e in Solution().criticalConnections(n, edges))
print("\n".join(f"{a} {b}" for a, b in result))
