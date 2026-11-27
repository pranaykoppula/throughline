package main

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
