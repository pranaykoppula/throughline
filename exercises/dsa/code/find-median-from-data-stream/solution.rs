use std::cmp::Reverse;
use std::collections::BinaryHeap;

struct MedianFinder {
    // The smaller half as a max-heap, the larger half as a min-heap.
    // The smaller half holds the same number of values, or one more.
    low: BinaryHeap<i32>,
    high: BinaryHeap<Reverse<i32>>,
}

impl MedianFinder {
    fn new() -> Self {
        MedianFinder { low: BinaryHeap::new(), high: BinaryHeap::new() }
    }

    fn add_num(&mut self, num: i32) {
        // Pass the new value through the low half, so the biggest of the low half moves up.
        self.low.push(num);
        let top = self.low.pop().unwrap();
        self.high.push(Reverse(top));
        // Keep the low half the same size as the high half, or one bigger.
        if self.high.len() > self.low.len() {
            let Reverse(x) = self.high.pop().unwrap();
            self.low.push(x);
        }
    }

    fn find_median(&self) -> f64 {
        let lo = *self.low.peek().unwrap() as f64;
        if self.low.len() > self.high.len() {
            return lo;
        }
        let Reverse(hi) = *self.high.peek().unwrap();
        (lo + hi as f64) / 2.0
    }
}
