import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution import AllOne

counts = AllOne()
out = []
for line in sys.stdin.read().split("\n"):
    parts = line.split()
    if not parts:
        continue
    if parts[0] == "inc":
        counts.inc(parts[1])
    elif parts[0] == "dec":
        counts.dec(parts[1])
    elif parts[0] == "max":
        out.append('"' + counts.getMaxKey() + '"')
    else:
        out.append('"' + counts.getMinKey() + '"')
print("\n".join(out))
