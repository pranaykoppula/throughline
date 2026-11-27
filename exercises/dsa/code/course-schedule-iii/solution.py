import heapq
from typing import List


class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        taken = []   # durations of the courses kept so far, longest on top (stored negated)
        day = 0      # the day the kept courses finish, taken one after another
        # Consider courses in order of deadline: the earliest deadline first.
        for duration, last_day in sorted(courses, key=lambda c: c[1]):
            heapq.heappush(taken, -duration)
            day += duration
            if day > last_day:
                # Too late: drop the longest course kept so far. It frees the most time,
                # and the rest still finish in time because their deadlines are earlier.
                day += heapq.heappop(taken)
        return len(taken)
