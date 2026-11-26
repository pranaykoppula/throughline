# The waiting-room screen

An exercise in the category **the most urgent next**. It's LeetCode 295, [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/), rated Hard.

## The situation

A hospital's emergency department shows patients, on a screen in the waiting room, the median waiting time for everyone seen so far today. The median, not the average, because one patient who waited nine hours would drag the average far above what anyone typically waits. Every time a patient is seen, their wait is added, and the screen updates. On a busy day that's several hundred patients, and the same software runs a network-wide dashboard that handles tens of thousands of waits an hour.

## The problem

Build a structure that accepts numbers one at a time and can report, at any moment, the median of all the numbers so far: the middle one if there's an odd count, or the average of the two middle ones if there's an even count.

After adding 1 and 2, the median is 1.5. After adding 3 as well, it's 2.

## The question it asks

"What's the most urgent value now?", asked about two values at once: the largest of the smaller half and the smallest of the larger half. Each is the kind of question a [heap](../../dsa/heaps.md) answers. See the row for the most urgent next in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Keep every wait in a list, and when the screen asks for the median, sort the list and read the middle. Sorting every time costs *n* log *n* for each query ([sorting](../../dsa/sorting.md)), and the screen asks after every patient.

The next idea is to keep the list sorted as you go, inserting each new wait in its place. Then the median is one look, but each insertion shifts on average half the list along, so adding becomes linear. For a few hundred patients that's fine. For tens of thousands of waits an hour, it's the most expensive part of the system.

## Hints

<details markdown="1"><summary>Hint 1</summary>

To report the median you never need the whole list in order. You only need the one or two values in the middle. What would you need to know about the values on each side of the middle?

</details>

<details markdown="1"><summary>Hint 2</summary>

Split the waits into a smaller half and a larger half. The median is the largest of the smaller half, or the average of that and the smallest of the larger half. Which structure gives you "the largest" or "the smallest" cheaply, and lets you keep adding?

</details>

<details markdown="1"><summary>Hint 3</summary>

When a new wait arrives, it might belong in either half, and the halves might become unequal in size. How can you put it in the right half and rebalance, using only each half's top value?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Keep two heaps:

- **`low`**, a max-heap holding the smaller half of the waits, so its top is the largest of the small ones;
- **`high`**, a min-heap holding the larger half, so its top is the smallest of the large ones.

Keep `low` the same size as `high`, or one bigger.

**Adding a wait:**

1. Push it onto `low`.
2. Move `low`'s top (now the largest of the small values, which might be the new one) onto `high`. This guarantees every value in `low` is no bigger than every value in `high`.
3. If `high` is now bigger than `low`, move `high`'s top back onto `low`.

**Reporting the median:** if `low` has one more value, the median is `low`'s top. Otherwise it's the average of the two tops.

Passing every new value through `low` and then `high` is what keeps the halves correctly ordered, without ever comparing the new value with the median directly.

**Why it's fast:** each addition does at most three heap pushes and pops, each taking time in proportion to log *n*, and reporting the median is a look at two tops. Most languages' heaps are min-heaps, so the code stores `low` negated, or with a reversed ordering.

**Time:** log *n* per addition, constant per median. **Memory:** proportional to *n*.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
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
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
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
```

</details>

<details markdown="1"><summary>Java</summary>

```java
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
```

</details>

<details markdown="1"><summary>Go</summary>

```go
import "container/heap"

// A min-heap of ints; the low half stores negated values to act as a max-heap.
type intHeap []int

func (h intHeap) Len() int           { return len(h) }
func (h intHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h intHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *intHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *intHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type MedianFinder struct {
	// The smaller half (negated) and the larger half.
	// The smaller half holds the same number of values, or one more.
	low, high *intHeap
}

func Constructor() MedianFinder {
	return MedianFinder{low: &intHeap{}, high: &intHeap{}}
}

func (this *MedianFinder) AddNum(num int) {
	// Pass the new value through the low half, so the biggest of the low half moves up.
	heap.Push(this.low, -num)
	heap.Push(this.high, -heap.Pop(this.low).(int))
	// Keep the low half the same size as the high half, or one bigger.
	if this.high.Len() > this.low.Len() {
		heap.Push(this.low, -heap.Pop(this.high).(int))
	}
}

func (this *MedianFinder) FindMedian() float64 {
	if this.low.Len() > this.high.Len() {
		return float64(-(*this.low)[0])
	}
	return float64(-(*this.low)[0]+(*this.high)[0]) / 2
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
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
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Inserting into the "obvious" half.** Comparing the new value with the current median and choosing a heap works, but it's easy to get the ties and the empty case wrong. Passing every value through both heaps avoids that.
- **Letting the sizes drift apart.** After every addition, rebalance so `low` has the same count or one more.
- **Integer division.** The average of two middle waits can be a half.
- **Forgetting that Java's and Python's heaps are min-heaps.** The low half needs a reversed comparator or negated values.

## Related

- The other exercise in this category: [the city's outline](the-skyline-problem.md) (LeetCode 218).
- Concept pages: [heaps and priority queues](../../dsa/heaps.md), [distributions and percentiles](../../math/percentiles.md), [sorting](../../dsa/sorting.md), [exact or approximate](../../dsa/exact-or-approximate.md).
- More practice of the same shape: problems tagged "two heaps", such as a sliding-window median.
