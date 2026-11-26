import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # Squares we can reach, by the water level needed to reach them; lowest first.
        frontier = [(grid[0][0], 0, 0)]
        seen = {(0, 0)}
        while frontier:
            level, r, c = heapq.heappop(frontier)
            if (r, c) == (n - 1, n - 1):
                return level
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    # Reaching the neighbour needs the higher of the two levels.
                    heapq.heappush(frontier, (max(level, grid[nr][nc]), nr, nc))
        return -1
