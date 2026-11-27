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
