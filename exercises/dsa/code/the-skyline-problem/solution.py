import heapq
from typing import List


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # Every place the outline can change: a building's left or right edge.
        edges = sorted({x for left, right, _ in buildings for x in (left, right)})
        skyline = []
        standing = []   # (-height, right edge) of buildings that have started; tallest on top
        i, n = 0, len(buildings)
        for x in edges:
            # Buildings that start here join the heap (the input is sorted by left edge).
            while i < n and buildings[i][0] <= x:
                left, right, height = buildings[i]
                heapq.heappush(standing, (-height, right))
                i += 1
            # The tallest might have ended already; drop it only when it's on top.
            while standing and standing[0][1] <= x:
                heapq.heappop(standing)
            height = -standing[0][0] if standing else 0
            if not skyline or skyline[-1][1] != height:
                skyline.append([x, height])
        return skyline
