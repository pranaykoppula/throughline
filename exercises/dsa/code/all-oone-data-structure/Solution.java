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
