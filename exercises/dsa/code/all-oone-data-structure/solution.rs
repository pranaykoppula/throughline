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
