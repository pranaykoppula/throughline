import java.util.Collections;
import java.util.PriorityQueue;

class MedianFinder {
    // The smaller half as a max-heap, the larger half as a min-heap.
    // The smaller half holds the same number of values, or one more.
    private final PriorityQueue<Integer> low = new PriorityQueue<>(Collections.reverseOrder());
    private final PriorityQueue<Integer> high = new PriorityQueue<>();

    public MedianFinder() {}

    public void addNum(int num) {
        // Pass the new value through the low half, so the biggest of the low half moves up.
        low.add(num);
        high.add(low.poll());
        // Keep the low half the same size as the high half, or one bigger.
        if (high.size() > low.size()) {
            low.add(high.poll());
        }
    }

    public double findMedian() {
        if (low.size() > high.size()) return low.peek();
        return ((double) low.peek() + high.peek()) / 2.0;
    }
}
