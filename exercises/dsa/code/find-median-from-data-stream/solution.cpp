class MedianFinder {
    // The smaller half as a max-heap, the larger half as a min-heap.
    // The smaller half holds the same number of values, or one more.
    priority_queue<int> low;
    priority_queue<int, vector<int>, greater<int>> high;

public:
    MedianFinder() {}

    void addNum(int num) {
        // Pass the new value through the low half, so the biggest of the low half moves up.
        low.push(num);
        high.push(low.top());
        low.pop();
        // Keep the low half the same size as the high half, or one bigger.
        if (high.size() > low.size()) {
            low.push(high.top());
            high.pop();
        }
    }

    double findMedian() {
        if (low.size() > high.size()) return low.top();
        return ((double)low.top() + high.top()) / 2.0;
    }
};
