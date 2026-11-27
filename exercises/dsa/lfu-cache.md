# The least-asked question

An exercise in the category **build a structure for the pattern**. It's LeetCode 460, [LFU Cache](https://leetcode.com/problems/lfu-cache/), rated Hard.

## The situation

A weather service answers forecast requests for millions of places. Working out a forecast is expensive, so recent answers are kept in memory, but memory only holds so many. When it's full and a new place is asked about, one stored answer has to go. Throwing out the answer used longest ago works badly here: a burst of requests for a one-off event pushes out the big cities that are asked about all day. So the service throws out the answer asked for the fewest times, and among those, the one asked for longest ago. Every request has to be answered in a fixed, small amount of time, however full memory is.

## The problem

Build a cache with a fixed capacity, holding keys and values, with two operations:

- `get(key)`: return the key's value, or −1 if it isn't there. This counts as a use of the key.
- `put(key, value)`: store or update the key's value, which also counts as a use. If a new key arrives when the cache is full, first remove the key with the fewest uses; if several are tied, remove the one used longest ago.

Both must run in constant time on average.

## The question it asks

There's no single structure for this. The cache needs three answers instantly: where's this key? which keys have the fewest uses? which of those was used longest ago? Each has a structure that answers it, and the work is building one thing out of them that keeps all three answers right on every operation. See [choosing a data structure](../../dsa/choosing.md), whose advice "real systems combine them" is the whole problem here, and [caching](../../performance/caching.md) for why the eviction rule matters.

## The tempting first answer

Keep each key's value, its use count and the time of its last use in a [hash table](../../dsa/hash-tables.md). To evict, scan every key for the fewest uses and the oldest time. Lookups are instant, but every eviction looks at the whole cache ([growth](../../dsa/growth.md)), and in a full cache nearly every new place is an eviction.

The next idea is a [heap](../../dsa/heaps.md) ordered by (uses, last use). Eviction becomes a pop, but every `get` changes a key's count, which means finding it in the heap and moving it: logarithmic, not constant, and fiddly.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Group the keys by their use count. Within one group, you need the one used longest ago, and you need to move any key out of its group quickly. What structure keeps things in order of arrival and lets you remove any item in one step?

</details>

<details markdown="1"><summary>Hint 2</summary>

A doubly linked list, with a hash table from key to its node, does both. Keep one such list for each use count. When a key is used, it moves from the list for *n* uses to the end of the list for *n* + 1.

</details>

<details markdown="1"><summary>Hint 3</summary>

To evict, you need the list with the smallest count. You can't search for it, but you can keep track of it. When does the smallest count change, and to what?

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Keep:

- a hash table from each key to its value, its use count and its place in a list;
- for each use count, an ordered list of the keys with that count, oldest use at the front;
- `fewest`, the smallest use count of any key in the cache.

**Using a key** (`get` that finds it, or `put` on a key that's there): take it out of its count's list, add it to the end of the list for one more use, and if its old list is now empty and was the `fewest` one, add one to `fewest`.

**Adding a new key:** if the cache is full, remove the key at the front of the `fewest` list, from both the list and the hash table. Then add the new key to the end of the list for one use, and set `fewest` to 1.

**Why `fewest` never needs searching for:** it can only change in two ways. A key moving up from the smallest group can empty it, and then the smallest count is exactly one more, because that key is now there. A new key arriving always has one use, the fewest possible. Nothing else changes it.

**Why every step is constant:** each operation does a fixed number of hash-table lookups and list moves, and a list move only touches a node and its two neighbours. In Python an `OrderedDict` is this kind of list; in Java, a `LinkedHashSet`; in C++ and Go, a standard list with the node's position stored; the Rust version keeps its list nodes in a vector and links them by position.

**Time:** constant on average for both operations. **Memory:** proportional to the capacity.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.value = {}                          # key -> value
        self.uses = {}                           # key -> how many times it has been used
        self.by_uses = defaultdict(OrderedDict)  # uses -> keys with that count, oldest use first
        self.fewest = 0                          # the smallest use count of any key

    def _touch(self, key: int) -> None:
        # Move the key up one use count, to the newest end of the next group.
        n = self.uses[key]
        del self.by_uses[n][key]
        if not self.by_uses[n]:
            del self.by_uses[n]
            if self.fewest == n:
                self.fewest = n + 1
        self.uses[key] = n + 1
        self.by_uses[n + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.value:
            return -1
        self._touch(key)
        return self.value[key]

    def put(self, key: int, value: int) -> None:
        if key in self.value:
            self.value[key] = value
            self._touch(key)
            return
        if len(self.value) == self.capacity:
            # Evict the least used key, and among those, the one used longest ago.
            old, _ = self.by_uses[self.fewest].popitem(last=False)
            if not self.by_uses[self.fewest]:
                del self.by_uses[self.fewest]
            del self.value[old], self.uses[old]
        self.value[key] = value
        self.uses[key] = 1
        self.by_uses[1][key] = None
        self.fewest = 1   # a new key has the fewest uses there can be
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class LFUCache {
    int capacity, fewest = 0;  // fewest: the smallest use count of any key
    struct Entry {
        int value, uses;
        list<int>::iterator where;  // its place in the list for its use count
    };
    unordered_map<int, Entry> entries;
    unordered_map<int, list<int>> byUses;  // uses -> keys with that count, oldest use first

    // Move the key up one use count, to the newest end of the next group.
    void touch(int key) {
        Entry& e = entries[key];
        auto& group = byUses[e.uses];
        group.erase(e.where);
        if (group.empty()) {
            byUses.erase(e.uses);
            if (fewest == e.uses) fewest++;
        }
        e.uses++;
        auto& next = byUses[e.uses];
        e.where = next.insert(next.end(), key);
    }

public:
    LFUCache(int capacity) : capacity(capacity) {}

    int get(int key) {
        auto it = entries.find(key);
        if (it == entries.end()) return -1;
        touch(key);
        return it->second.value;
    }

    void put(int key, int value) {
        auto it = entries.find(key);
        if (it != entries.end()) {
            it->second.value = value;
            touch(key);
            return;
        }
        if ((int)entries.size() == capacity) {
            // Evict the least used key, and among those, the one used longest ago.
            auto& group = byUses[fewest];
            int old = group.front();
            group.pop_front();
            if (group.empty()) byUses.erase(fewest);
            entries.erase(old);
        }
        auto& ones = byUses[1];
        entries[key] = {value, 1, ones.insert(ones.end(), key)};
        fewest = 1;  // a new key has the fewest uses there can be
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.Map;

class LFUCache {
    private final int capacity;
    private int fewest = 0;                                    // the smallest use count of any key
    private final Map<Integer, Integer> value = new HashMap<>();
    private final Map<Integer, Integer> uses = new HashMap<>();
    // uses -> keys with that count, oldest use first
    private final Map<Integer, LinkedHashSet<Integer>> byUses = new HashMap<>();

    public LFUCache(int capacity) {
        this.capacity = capacity;
    }

    // Move the key up one use count, to the newest end of the next group.
    private void touch(int key) {
        int n = uses.get(key);
        LinkedHashSet<Integer> group = byUses.get(n);
        group.remove(key);
        if (group.isEmpty()) {
            byUses.remove(n);
            if (fewest == n) fewest = n + 1;
        }
        uses.put(key, n + 1);
        byUses.computeIfAbsent(n + 1, k -> new LinkedHashSet<>()).add(key);
    }

    public int get(int key) {
        if (!value.containsKey(key)) return -1;
        touch(key);
        return value.get(key);
    }

    public void put(int key, int val) {
        if (value.containsKey(key)) {
            value.put(key, val);
            touch(key);
            return;
        }
        if (value.size() == capacity) {
            // Evict the least used key, and among those, the one used longest ago.
            LinkedHashSet<Integer> group = byUses.get(fewest);
            Iterator<Integer> oldest = group.iterator();
            int old = oldest.next();
            oldest.remove();
            if (group.isEmpty()) byUses.remove(fewest);
            value.remove(old);
            uses.remove(old);
        }
        value.put(key, val);
        uses.put(key, 1);
        byUses.computeIfAbsent(1, k -> new LinkedHashSet<>()).add(key);
        fewest = 1;  // a new key has the fewest uses there can be
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
import "container/list"

type lfuEntry struct {
	value, uses int
	where       *list.Element // its place in the list for its use count
}

type LFUCache struct {
	capacity, fewest int // fewest: the smallest use count of any key
	entries          map[int]*lfuEntry
	byUses           map[int]*list.List // uses -> keys with that count, oldest use first
}

func Constructor(capacity int) LFUCache {
	return LFUCache{capacity: capacity, entries: map[int]*lfuEntry{}, byUses: map[int]*list.List{}}
}

// Move the key up one use count, to the newest end of the next group.
func (this *LFUCache) touch(key int) {
	e := this.entries[key]
	group := this.byUses[e.uses]
	group.Remove(e.where)
	if group.Len() == 0 {
		delete(this.byUses, e.uses)
		if this.fewest == e.uses {
			this.fewest++
		}
	}
	e.uses++
	e.where = this.group(e.uses).PushBack(key)
}

func (this *LFUCache) group(uses int) *list.List {
	if this.byUses[uses] == nil {
		this.byUses[uses] = list.New()
	}
	return this.byUses[uses]
}

func (this *LFUCache) Get(key int) int {
	e, ok := this.entries[key]
	if !ok {
		return -1
	}
	this.touch(key)
	return e.value
}

func (this *LFUCache) Put(key int, value int) {
	if e, ok := this.entries[key]; ok {
		e.value = value
		this.touch(key)
		return
	}
	if len(this.entries) == this.capacity {
		// Evict the least used key, and among those, the one used longest ago.
		group := this.byUses[this.fewest]
		old := group.Remove(group.Front()).(int)
		if group.Len() == 0 {
			delete(this.byUses, this.fewest)
		}
		delete(this.entries, old)
	}
	this.entries[key] = &lfuEntry{value: value, uses: 1, where: this.group(1).PushBack(key)}
	this.fewest = 1 // a new key has the fewest uses there can be
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
use std::collections::HashMap;

// Keys with the same use count form a doubly linked list, oldest use at the head.
// The list nodes live in a vector and point at each other by position.
const NONE: usize = usize::MAX;

struct Node {
    key: i32,
    value: i32,
    uses: i32,
    prev: usize,
    next: usize,
}

struct LFUCache {
    capacity: usize,
    fewest: i32,                          // the smallest use count of any key
    nodes: Vec<Node>,
    free: Vec<usize>,                     // positions of evicted nodes, to reuse
    slot: HashMap<i32, usize>,            // key -> its node
    by_uses: HashMap<i32, (usize, usize)>, // uses -> (head, tail) of its list
}

impl LFUCache {
    fn new(capacity: i32) -> Self {
        LFUCache { capacity: capacity as usize, fewest: 0, nodes: Vec::new(), free: Vec::new(), slot: HashMap::new(), by_uses: HashMap::new() }
    }

    fn unlink(&mut self, i: usize) {
        let (uses, prev, next) = (self.nodes[i].uses, self.nodes[i].prev, self.nodes[i].next);
        let ends = self.by_uses.get_mut(&uses).unwrap();
        if prev == NONE { ends.0 = next; } else { self.nodes[prev].next = next; }
        if next == NONE { ends.1 = prev; } else { self.nodes[next].prev = prev; }
        if ends.0 == NONE {
            self.by_uses.remove(&uses);
            if self.fewest == uses {
                self.fewest = uses + 1;
            }
        }
    }

    fn push_back(&mut self, i: usize) {
        let uses = self.nodes[i].uses;
        let ends = self.by_uses.entry(uses).or_insert((NONE, NONE));
        let tail = ends.1;
        if tail == NONE { ends.0 = i; } else { self.nodes[tail].next = i; }
        ends.1 = i;
        self.nodes[i].prev = tail;
        self.nodes[i].next = NONE;
    }

    // Move the key up one use count, to the newest end of the next group.
    fn touch(&mut self, i: usize) {
        self.unlink(i);
        self.nodes[i].uses += 1;
        self.push_back(i);
    }

    fn get(&mut self, key: i32) -> i32 {
        match self.slot.get(&key) {
            None => -1,
            Some(&i) => {
                self.touch(i);
                self.nodes[i].value
            }
        }
    }

    fn put(&mut self, key: i32, value: i32) {
        if let Some(&i) = self.slot.get(&key) {
            self.nodes[i].value = value;
            self.touch(i);
            return;
        }
        if self.slot.len() == self.capacity {
            // Evict the least used key, and among those, the one used longest ago.
            let oldest = self.by_uses[&self.fewest].0;
            self.unlink(oldest);
            self.slot.remove(&self.nodes[oldest].key);
            self.free.push(oldest);
        }
        let node = Node { key, value, uses: 1, prev: NONE, next: NONE };
        let i = match self.free.pop() {
            Some(i) => {
                self.nodes[i] = node;
                i
            }
            None => {
                self.nodes.push(node);
                self.nodes.len() - 1
            }
        };
        self.slot.insert(key, i);
        self.push_back(i);
        self.fewest = 1; // a new key has the fewest uses there can be
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Forgetting that `put` on an existing key is a use.** It updates the value and moves the key up a count.
- **Searching for the smallest count.** It's only ever 1 after an insert, or one more after the smallest group empties; track it.
- **Evicting before checking whether the key is already there.** Updating an existing key never evicts anything.
- **Breaking ties by insertion instead of last use.** Within a count, the key used longest ago goes first, so a used key goes to the end of its new list.

## Related

- The other exercise in this category: [the leaderboard's ends](all-oone-data-structure.md) (LeetCode 432).
- Concept pages: [caching](../../performance/caching.md), [hash tables](../../dsa/hash-tables.md), [arrays and linked lists](../../dsa/arrays-and-linked-lists.md), [choosing a data structure](../../dsa/choosing.md).
- More practice of the same shape: the LRU cache (LeetCode 146), the simpler version that evicts the key used longest ago.
