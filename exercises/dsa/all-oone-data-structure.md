# The leaderboard's ends

An exercise in the category **build a structure for the pattern**. It's LeetCode 432, [All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/), rated Hard.

## The situation

A video service shows two lines on its live dashboard: the show being watched by the most people right now, and the show being watched by the fewest of those that anyone's watching at all. Every time someone starts a show, its count goes up by one; every time someone stops, it goes down by one, and a show with nobody watching drops off. There are thousands of starts and stops a second, and the dashboard asks for both ends constantly. Each update and each question has to take the same small amount of time, however many shows are on.

## The problem

Build a structure that counts strings, with four operations, each in constant time on average:

- `inc(key)`: add one to the key's count, starting it at 1 if it's new.
- `dec(key)`: take one from the key's count; at zero, the key is removed. The key is always there when this is called.
- `getMaxKey()`: return any key with the largest count, or `""` if there are none.
- `getMinKey()`: return any key with the smallest count, or `""` if there are none.

After `inc("hello")` twice, both ends are `hello`. After `inc("leet")`, the maximum is still `hello` and the minimum is `leet`.

## The question it asks

"What's at each end, right now?", with the ends moving one step at a time. A [heap](../../dsa/heaps.md) answers one end, and only in logarithmic time per change. The pattern that makes constant time possible is that counts only ever change by one. See [choosing a data structure](../../dsa/choosing.md): the answer is built from simpler structures, arranged to fit that pattern.

## The tempting first answer

Keep the counts in a [hash table](../../dsa/hash-tables.md) and scan it for the largest and smallest whenever the dashboard asks. Updates are instant; every question looks at every show ([growth](../../dsa/growth.md)).

The next idea is a sorted structure, a balanced tree or two heaps of (count, key). Both ends come out quickly, but every update has to find the key and move it, which is logarithmic, and with heaps, removing a key that isn't on top needs the lazy-deletion tricks from [the city's outline](the-skyline-problem.md).

## Hints

<details markdown="1"><summary>Hint 1</summary>

When a count goes up by one, the key moves to the group of keys with exactly one more. If you kept groups of keys by count, in order, how far would a key ever have to move?

</details>

<details markdown="1"><summary>Hint 2</summary>

Only to the next group up or down. Keep the groups in a doubly linked list, ordered by count, with only counts that some key actually has. The ends of the list are the answers.

</details>

<details markdown="1"><summary>Hint 3</summary>

When a key moves up and the next group doesn't hold exactly one more, make a new group right there. When a group empties, unlink it. A hash table from each key to its group makes finding it instant.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

Keep:

- a doubly linked list of **buckets**, each holding a count and the set of keys with that count, in increasing order of count, with an empty marker bucket at each end;
- a hash table from each key to its bucket.

**`inc(key)`:** find the key's bucket, or the front marker if the key is new. If the bucket after it doesn't hold exactly one more, insert a new bucket there for that count. Move the key into it. If its old bucket is now empty, unlink it.

**`dec(key)`:** find the key's bucket. If its count is 1, forget the key. Otherwise, if the bucket before it doesn't hold exactly one less, insert one. Move the key into it. If its old bucket is now empty, unlink it.

**`getMaxKey()` and `getMinKey()`:** any key from the bucket next to the back marker, or the front one.

**Why it stays in order without sorting:** a key only ever moves to a neighbouring bucket, and a new bucket is only ever made next to the one the key came from, with a count between its neighbours'. So the list is always in order, and nothing ever has to be compared with anything far away.

**Why the markers:** with an empty bucket at each end, every real bucket always has neighbours, and new keys are just keys moving up from count 0. The code has no special cases for an empty list.

**Time:** constant on average for every operation. **Memory:** proportional to the number of keys.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
class Bucket:
    # Every key with the same count, in a list of buckets kept in order of count.
    def __init__(self, count: int):
        self.count = count
        self.keys = set()
        self.prev = self.next = None


class AllOne:
    def __init__(self):
        # Two empty buckets mark the ends, so no bucket ever lacks a neighbour.
        self.head, self.tail = Bucket(0), Bucket(0)
        self.head.next, self.tail.prev = self.tail, self.head
        self.where = {}   # key -> its bucket

    def _insert_after(self, b: Bucket, count: int) -> Bucket:
        new = Bucket(count)
        new.prev, new.next = b, b.next
        b.next.prev = new
        b.next = new
        return new

    def _remove_key(self, b: Bucket, key: str) -> None:
        b.keys.discard(key)
        if not b.keys:   # an empty bucket leaves the list
            b.prev.next, b.next.prev = b.next, b.prev

    def inc(self, key: str) -> None:
        b = self.where.get(key, self.head)
        # The next bucket up must hold count + 1; make it if it doesn't exist.
        up = b.next
        if up is self.tail or up.count != b.count + 1:
            up = self._insert_after(b, b.count + 1)
        up.keys.add(key)
        self.where[key] = up
        if b is not self.head:
            self._remove_key(b, key)

    def dec(self, key: str) -> None:
        b = self.where[key]
        if b.count == 1:
            del self.where[key]   # a count of zero means the key is gone
        else:
            down = b.prev
            if down is self.head or down.count != b.count - 1:
                down = self._insert_after(b.prev, b.count - 1)
            down.keys.add(key)
            self.where[key] = down
        self._remove_key(b, key)

    def getMaxKey(self) -> str:
        return next(iter(self.tail.prev.keys)) if self.tail.prev is not self.head else ""

    def getMinKey(self) -> str:
        return next(iter(self.head.next.keys)) if self.head.next is not self.tail else ""
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class AllOne {
    // Every key with the same count, in a list of buckets kept in order of count.
    struct Bucket {
        int count;
        unordered_set<string> keys;
    };
    list<Bucket> buckets;                                  // lowest count at the front
    unordered_map<string, list<Bucket>::iterator> where;  // key -> its bucket

    void removeKey(list<Bucket>::iterator b, const string& key) {
        b->keys.erase(key);
        if (b->keys.empty()) buckets.erase(b);  // an empty bucket leaves the list
    }

public:
    AllOne() {}

    void inc(string key) {
        auto found = where.find(key);
        if (found == where.end()) {
            // A new key: it belongs in a bucket of count 1 at the front.
            if (buckets.empty() || buckets.front().count != 1) buckets.push_front({1, {}});
            buckets.front().keys.insert(key);
            where[key] = buckets.begin();
            return;
        }
        auto b = found->second;
        // The next bucket up must hold count + 1; make it if it doesn't exist.
        auto up = next(b);
        if (up == buckets.end() || up->count != b->count + 1) up = buckets.insert(up, {b->count + 1, {}});
        up->keys.insert(key);
        where[key] = up;
        removeKey(b, key);
    }

    void dec(string key) {
        auto b = where[key];
        if (b->count == 1) {
            where.erase(key);  // a count of zero means the key is gone
        } else {
            auto down = b;
            if (b == buckets.begin() || prev(b)->count != b->count - 1) {
                down = buckets.insert(b, {b->count - 1, {}});
            } else {
                down = prev(b);
            }
            down->keys.insert(key);
            where[key] = down;
        }
        removeKey(b, key);
    }

    string getMaxKey() {
        return buckets.empty() ? "" : *buckets.back().keys.begin();
    }

    string getMinKey() {
        return buckets.empty() ? "" : *buckets.front().keys.begin();
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

class AllOne {
    // Every key with the same count, in a list of buckets kept in order of count.
    private static class Bucket {
        int count;
        Set<String> keys = new HashSet<>();
        Bucket prev, next;

        Bucket(int count) {
            this.count = count;
        }
    }

    // Two empty buckets mark the ends, so no bucket ever lacks a neighbour.
    private final Bucket head = new Bucket(0), tail = new Bucket(0);
    private final Map<String, Bucket> where = new HashMap<>();  // key -> its bucket

    public AllOne() {
        head.next = tail;
        tail.prev = head;
    }

    private Bucket insertAfter(Bucket b, int count) {
        Bucket fresh = new Bucket(count);
        fresh.prev = b;
        fresh.next = b.next;
        b.next.prev = fresh;
        b.next = fresh;
        return fresh;
    }

    private void removeKey(Bucket b, String key) {
        b.keys.remove(key);
        if (b.keys.isEmpty()) {  // an empty bucket leaves the list
            b.prev.next = b.next;
            b.next.prev = b.prev;
        }
    }

    public void inc(String key) {
        Bucket b = where.getOrDefault(key, head);
        // The next bucket up must hold count + 1; make it if it doesn't exist.
        Bucket up = b.next;
        if (up == tail || up.count != b.count + 1) up = insertAfter(b, b.count + 1);
        up.keys.add(key);
        where.put(key, up);
        if (b != head) removeKey(b, key);
    }

    public void dec(String key) {
        Bucket b = where.get(key);
        if (b.count == 1) {
            where.remove(key);  // a count of zero means the key is gone
        } else {
            Bucket down = b.prev;
            if (down == head || down.count != b.count - 1) down = insertAfter(b.prev, b.count - 1);
            down.keys.add(key);
            where.put(key, down);
        }
        removeKey(b, key);
    }

    public String getMaxKey() {
        return tail.prev == head ? "" : tail.prev.keys.iterator().next();
    }

    public String getMinKey() {
        return head.next == tail ? "" : head.next.keys.iterator().next();
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
// Every key with the same count, in a list of buckets kept in order of count.
type bucket struct {
	count      int
	keys       map[string]bool
	prev, next *bucket
}

type AllOne struct {
	head, tail *bucket // two empty buckets mark the ends
	where      map[string]*bucket
}

func Constructor() AllOne {
	head, tail := &bucket{}, &bucket{}
	head.next, tail.prev = tail, head
	return AllOne{head: head, tail: tail, where: map[string]*bucket{}}
}

func (this *AllOne) insertAfter(b *bucket, count int) *bucket {
	fresh := &bucket{count: count, keys: map[string]bool{}, prev: b, next: b.next}
	b.next.prev = fresh
	b.next = fresh
	return fresh
}

func (this *AllOne) removeKey(b *bucket, key string) {
	delete(b.keys, key)
	if len(b.keys) == 0 { // an empty bucket leaves the list
		b.prev.next, b.next.prev = b.next, b.prev
	}
}

func (this *AllOne) Inc(key string) {
	b, ok := this.where[key]
	if !ok {
		b = this.head
	}
	// The next bucket up must hold count + 1; make it if it doesn't exist.
	up := b.next
	if up == this.tail || up.count != b.count+1 {
		up = this.insertAfter(b, b.count+1)
	}
	up.keys[key] = true
	this.where[key] = up
	if b != this.head {
		this.removeKey(b, key)
	}
}

func (this *AllOne) Dec(key string) {
	b := this.where[key]
	if b.count == 1 {
		delete(this.where, key) // a count of zero means the key is gone
	} else {
		down := b.prev
		if down == this.head || down.count != b.count-1 {
			down = this.insertAfter(b.prev, b.count-1)
		}
		down.keys[key] = true
		this.where[key] = down
	}
	this.removeKey(b, key)
}

func anyKey(b *bucket) string {
	for k := range b.keys {
		return k
	}
	return ""
}

func (this *AllOne) GetMaxKey() string {
	if this.tail.prev == this.head {
		return ""
	}
	return anyKey(this.tail.prev)
}

func (this *AllOne) GetMinKey() string {
	if this.head.next == this.tail {
		return ""
	}
	return anyKey(this.head.next)
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
use std::collections::{HashMap, HashSet};

// Every key with the same count, in a list of buckets kept in order of count.
// The buckets live in a vector and point at each other by position;
// positions 0 and 1 are empty buckets that mark the two ends.
const HEAD: usize = 0;
const TAIL: usize = 1;

struct Bucket {
    count: i32,
    keys: HashSet<String>,
    prev: usize,
    next: usize,
}

struct AllOne {
    buckets: Vec<Bucket>,
    free: Vec<usize>,              // positions of removed buckets, to reuse
    place: HashMap<String, usize>, // key -> its bucket
}

impl AllOne {
    fn new() -> Self {
        let head = Bucket { count: 0, keys: HashSet::new(), prev: HEAD, next: TAIL };
        let tail = Bucket { count: 0, keys: HashSet::new(), prev: HEAD, next: TAIL };
        AllOne { buckets: vec![head, tail], free: Vec::new(), place: HashMap::new() }
    }

    fn insert_after(&mut self, b: usize, count: i32) -> usize {
        let next = self.buckets[b].next;
        let fresh = Bucket { count, keys: HashSet::new(), prev: b, next };
        let i = match self.free.pop() {
            Some(i) => {
                self.buckets[i] = fresh;
                i
            }
            None => {
                self.buckets.push(fresh);
                self.buckets.len() - 1
            }
        };
        self.buckets[next].prev = i;
        self.buckets[b].next = i;
        i
    }

    fn remove_key(&mut self, b: usize, key: &str) {
        self.buckets[b].keys.remove(key);
        if self.buckets[b].keys.is_empty() {
            // An empty bucket leaves the list.
            let (prev, next) = (self.buckets[b].prev, self.buckets[b].next);
            self.buckets[prev].next = next;
            self.buckets[next].prev = prev;
            self.free.push(b);
        }
    }

    fn inc(&mut self, key: String) {
        let b = *self.place.get(&key).unwrap_or(&HEAD);
        let count = self.buckets[b].count;
        // The next bucket up must hold count + 1; make it if it doesn't exist.
        let mut up = self.buckets[b].next;
        if up == TAIL || self.buckets[up].count != count + 1 {
            up = self.insert_after(b, count + 1);
        }
        self.buckets[up].keys.insert(key.clone());
        self.place.insert(key.clone(), up);
        if b != HEAD {
            self.remove_key(b, &key);
        }
    }

    fn dec(&mut self, key: String) {
        let b = self.place[&key];
        let count = self.buckets[b].count;
        if count == 1 {
            self.place.remove(&key); // a count of zero means the key is gone
        } else {
            let mut down = self.buckets[b].prev;
            if down == HEAD || self.buckets[down].count != count - 1 {
                down = self.insert_after(self.buckets[b].prev, count - 1);
            }
            self.buckets[down].keys.insert(key.clone());
            self.place.insert(key.clone(), down);
        }
        self.remove_key(b, &key);
    }

    fn get_max_key(&self) -> String {
        let b = self.buckets[TAIL].prev;
        if b == HEAD { String::new() } else { self.buckets[b].keys.iter().next().unwrap().clone() }
    }

    fn get_min_key(&self) -> String {
        let b = self.buckets[HEAD].next;
        if b == TAIL { String::new() } else { self.buckets[b].keys.iter().next().unwrap().clone() }
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Keeping a bucket for every count from 1 up.** Only counts that some key holds get a bucket, or the list grows with the largest count instead of the number of keys.
- **Forgetting to unlink an empty bucket.** Then the ends of the list point at buckets with no keys in them.
- **Inserting a new bucket on the wrong side.** Going up, the new bucket goes after the old one; going down, before it.
- **Moving the key before checking the neighbour.** Check whether the next bucket has the right count first, then create, then move, then clean up.

## Related

- The other exercise in this category: [the least-asked question](lfu-cache.md) (LeetCode 460).
- Concept pages: [hash tables](../../dsa/hash-tables.md), [arrays and linked lists](../../dsa/arrays-and-linked-lists.md), [heaps and priority queues](../../dsa/heaps.md), [choosing a data structure](../../dsa/choosing.md).
- More practice of the same shape: a structure that inserts, deletes and returns a random element, all in constant time, by pairing a hash table with an array.
