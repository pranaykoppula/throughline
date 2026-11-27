import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import LFUCache

lines = sys.stdin.read().split("\n")
cache = LFUCache(int(lines[0]))
out = []
for line in lines[1:]:
    parts = line.split()
    if not parts:
        continue
    if parts[0] == "get":
        out.append(str(cache.get(int(parts[1]))))
    else:
        cache.put(int(parts[1]), int(parts[2]))
print("\n".join(out))
