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
