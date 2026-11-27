import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import WordFilter

data = sys.stdin.read().split()
n = int(data[0])
search = WordFilter(data[1:1 + n])
q = int(data[1 + n])
out = []
for i in range(q):
    pref, suff = data[2 + n + 2 * i], data[3 + n + 2 * i]
    out.append(str(search.f(pref, suff)))
print("\n".join(out))
