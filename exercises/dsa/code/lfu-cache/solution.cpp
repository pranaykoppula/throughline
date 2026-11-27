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
