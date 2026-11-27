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
