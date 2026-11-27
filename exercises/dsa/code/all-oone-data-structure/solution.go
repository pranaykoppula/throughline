package main

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
