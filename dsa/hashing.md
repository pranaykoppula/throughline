# Hashing

Last reviewed: 2026-10-24

A concept page. It's shorter than a spine page, and its main job is the section called **Where it shows up**: the same idea doing different jobs in different stories.

## Problem

You have a key, such as a freight car number, a password, a file, or a user ID, and you need to do something with it fast: find its record, decide which machine holds it, check it hasn't changed, or prove it's the same as before. Comparing the key against everything you already have is too slow. You need a short, fixed-size stand-in for the key, computed from the key itself.

## The story

In 1955 Dorothy Kemp was a programmer at a railway freight office in Chicago. The office tracked twenty thousand freight cars. Every few seconds a clerk typed a car number and waited for its record: where the car was, what it carried, who owed what for it. The records were stored in number order on a magnetic drum, and Dorothy's program found a car by halving the search each time, the way you'd find a word in a dictionary. That was fast enough to read. It was terrible to write. Adding one new car meant shuffling every record after it along by one, to keep the order.

She wanted to skip the searching altogether. What if the car number itself said where to put the record? She tried the simplest version: use the last three digits as the slot number, a thousand slots, about twenty cars in each. Finding a car meant computing its slot and looking through twenty records instead of twenty thousand. Adding one meant dropping it into its slot. It worked beautifully in testing.

In use, it didn't. Railways numbered their cars in blocks, and a great many numbers ended in 000, 500 or 100. Those slots overflowed with hundreds of cars while most others sat nearly empty. The search was fast for some cars and slower than before for others. Dorothy had assumed car numbers were spread evenly, and they weren't. Real keys almost never are.

*Before reading on: the last three digits were too predictable. How would you turn a car number into a slot so that similar numbers land far apart?*

Her fix was to stop using any part of the number directly and to mix all of it. She combined the digits, multiplied, took the remainder after dividing by the number of slots, and chose that number with care. Cars whose numbers differed by one digit now landed in unrelated slots, and the slots filled evenly. When two cars did land in the same slot, which was certain to happen sometimes, the second went in the next free one. She learned to keep the table no more than about two thirds full, because past that point, chains of displaced cars grew quickly.

Looking back, Dorothy thought the idea was strange when you first met it and obvious ever after. Take any key, however long or awkward, and boil it down to a small number that looks random but is always the same for the same key. Once you have that, you can use it to decide where things go.

## Where it shows up

The same fingerprint does a different job in each story:

| Page | Job | What the hash does there |
| --- | --- | --- |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | **Lookup** | Elena's catalogue finds a part by its number without searching: Dorothy's idea, inside a module. |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | **Secrecy** | Marcus stores a hash of each password, so a leak doesn't reveal the password. This needs a hash that's hard to reverse, and slow and salted, so it's hard to guess. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | **Placement** | When data is split across machines, hashing each key decides which machine holds it, the way Dorothy's slots decided where each car went. |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | **Identity** | git names every commit by the hash of its contents, so the same content always has the same name and any change gives a new one. |

It shows up elsewhere too: checksums that catch data corrupted on a disk or on the wire, cache keys, and deduplication, where two identical files are stored once.

Lookup and placement need a hash that's *fast* and *spreads keys evenly*. Secrecy and identity need one that's *hard to reverse* and *hard to fool*. These are different families of function, and most mistakes with hashing come from using one where the other was needed.

## It really happened

Dorothy is fictional. In January 1953 Hans Peter Luhn, at IBM, wrote an internal memo proposing to put records into "buckets" chosen by computing on their keys, combining adjacent digits; it's the earliest known description of hashing. Others at IBM came up with storing collisions in the next free slot independently, and hashing first appeared in print in 1956 ([IEEE Spectrum](https://spectrum.ieee.org/tech-history/silicon-revolution/hans-peter-luhn-and-the-birth-of-the-hashing-algorithm)).

Dorothy's lesson that real keys aren't evenly spread came back as an attack. In 2011 Alexander Klink and Julian Wälde showed that web frameworks in PHP, Python, Java and Ruby put submitted form fields into hash tables using hash functions anyone could predict. An attacker could send one request full of keys that all landed in the same slot and keep a server busy for minutes. Languages responded by mixing a random secret into their hash functions at startup ([LWN](https://lwn.net/Articles/474912/); [Python's record](https://python-security.readthedocs.io/vuln/hash-dos.html)). Once strangers can choose your keys, a predictable hash is a weakness ([page 7](../07-strangers-on-the-network.md)).

Hashes meant to be hard to fool can still break. In 2017 researchers at Google and CWI Amsterdam produced two different PDF files with the same SHA-1 hash, the function git had used to name commits since 2005 ([SHAttered](https://shattered.io/) <!-- verify -->). git has been adding support for a stronger hash since. Identity is only as strong as the hash behind it.

## What it is

A hash function turns any input into a fixed-size value. The same input always gives the same value, and good functions spread similar inputs far apart. Two inputs can give the same value, called a collision, and every use has to decide what happens then. Fast, evenly spreading hashes serve lookup and placement. Cryptographic hashes, which are hard to reverse and hard to find collisions for, serve secrecy and identity. Passwords need a cryptographic hash that is also deliberately slow, and salted.

## Where it gets misapplied

- **A fast hash for passwords.** Fast is exactly what an attacker guessing billions of passwords wants ([page 7](../07-strangers-on-the-network.md)).
- **Assuming collisions never happen.** They always can. Hash tables plan for them; systems that use a hash as a name have to plan for the day the function is broken.
- **Placing data with `hash(key) mod N`.** It spreads data evenly, until you add a machine and almost every key moves. Consistent hashing exists to move only a small share.
- **The mirror:** inventing your own hash function. The standard ones have decades of attacks behind them; a new one has none, which doesn't mean it's safe.

## Connections

- Learning this is also learning [hash tables](hash-tables.md), because they're the lookup job done well: hashing plus a plan for collisions and a rule for when to grow.
- Learning this is also learning [Merkle DAGs](merkle-dags.md), because naming things by the hash of their contents is what lets git, and much else, check a whole history by checking one value.
- Learning this is also learning [consistent hashing](../data/partitioning.md), because placement has to survive machines being added and removed.
- Learning this is also learning [caching](../latency/caching.md), because a cache is a hash table that's allowed to forget.
- Learning this is also learning [password storage](../auth/password-storage.md), because secrecy needs the slow, salted kind.
- Learning this is also learning [input validation](../auth/input-validation.md), because hash flooding is strangers choosing your keys.

## Resources

1. Thomas Cormen et al., *Introduction to Algorithms*, the chapter on hash tables (start here, for the lookup job).
2. Donald Knuth, *The Art of Computer Programming*, volume 3, section 6.4 (go deeper; the history at the end of the section is where Luhn's memo is recorded).
3. Karger et al., ["Consistent Hashing and Random Trees"](https://courses.e-ce.uth.gr/CE623/STOC_1997_Consistent_hashing.pdf) (1997; the placement job, done so machines can come and go).
4. [SHAttered](https://shattered.io/) (reference: what it took to break SHA-1, and what that means for systems named by it). <!-- verify -->

## Names you'll hear

- **Collision:** two keys with the same hash.
- **Chaining, open addressing, linear probing:** ways to store colliding keys: a list per slot, or the next free slot.
- **Load factor:** how full the table is. Dorothy's two thirds.
- **MD5, SHA-1, SHA-256:** cryptographic hashes; the first two are broken for anything that needs to resist an attacker.
- **bcrypt, scrypt, Argon2:** password hashes, slow on purpose.
- **SipHash:** a fast hash with a secret key, used in hash tables since the hash-flooding attacks.

## Go and look

Find one place in something you've built where a hash is used, and decide which job it's doing: lookup, placement, secrecy, or identity. Then check that it's the right family of function for that job.
