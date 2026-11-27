import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

data = sys.stdin.read().split()
rows, cols = int(data[0]), int(data[1])
board = [list(data[2 + r]) for r in range(rows)]
k = int(data[2 + rows])
words = data[3 + rows:3 + rows + k]
print("\n".join(sorted(Solution().findWords(board, words))))
