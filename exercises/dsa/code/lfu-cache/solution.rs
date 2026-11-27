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
