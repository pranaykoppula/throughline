from typing import List


class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        links = [[] for _ in range(n)]
        for a, b in connections:
            links[a].append(b)
            links[b].append(a)
        found = [-1] * n   # when each server was first reached in the walk
        low = [0] * n      # the earliest server reachable from its subtree by a back route
        bridges = []
        clock = 0
        # A depth-first walk, written with an explicit stack because Python limits recursion.
        for root in range(n):
            if found[root] != -1:
                continue
            found[root] = low[root] = clock
            clock += 1
            stack = [(root, -1, 0)]   # (server, the server we came from, next link to try)
            while stack:
                u, parent, i = stack[-1]
                if i < len(links[u]):
                    stack[-1] = (u, parent, i + 1)
                    v = links[u][i]
                    if v == parent:
                        continue
                    if found[v] == -1:
                        found[v] = low[v] = clock
                        clock += 1
                        stack.append((v, u, 0))
                    else:
                        low[u] = min(low[u], found[v])   # a back route to an earlier server
                else:
                    stack.pop()
                    if parent != -1:
                        low[parent] = min(low[parent], low[u])
                        # Nothing below u reaches back above it: the link is critical.
                        if low[u] > found[parent]:
                            bridges.append([parent, u])
        return bridges
