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
