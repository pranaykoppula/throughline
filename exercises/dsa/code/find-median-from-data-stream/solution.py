import heapq


class MedianFinder:
    def __init__(self):
        # The smaller half, as a max-heap (stored negated), and the larger half, as a min-heap.
        # The smaller half holds the same number of values, or one more.
        self.low = []
        self.high = []

    def addNum(self, num: int) -> None:
        # Pass the new value through the low half, so the biggest of the low half moves up.
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # Keep the low half the same size as the high half, or one bigger.
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
