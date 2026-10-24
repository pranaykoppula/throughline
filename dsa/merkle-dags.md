# Merkle DAGs

Last reviewed: 2026-10-24

A concept page: naming data by the hash of its contents, and building trees of those names, so one short value can vouch for everything beneath it.

## Problem

You have two copies of something large, a backup, a database, a project's history, and you need to know whether they're the same, and if not, exactly where they differ. Comparing every byte is slow, especially over a network. One checksum of the whole thing tells you *whether* they differ, but not *where*.

## The story

In 2003 Ingrid Solberg wrote backup software for a company with offices in Oslo and Tromsø. Every night each office's file server copied itself to the other, two terabytes over a link that managed a few megabytes a second. Copying everything each night was impossible, so the software copied only files whose modification date had changed.

Then a disk controller in Tromsø started silently corrupting data: files whose dates said nothing had changed, but whose contents had. Ingrid's first fix was a checksum. Each night, each side computed a single hash of every byte it held and compared them. That worked, in a way. For three nights running the two hashes differed, and nobody knew which of millions of files was to blame. The only option the software had was to copy everything again, which would take most of a week.

*Before reading on: one hash said "something is different" and nothing more. How would you have found exactly what?*

Ingrid hashed at every level instead of only the top. Each file was split into blocks, and each block got its own hash. Each file's hash was the hash of its block hashes in order. Each folder's hash was the hash of its files' and subfolders' names and hashes. At the top, one hash for the whole server stood for everything beneath it.

Now the nightly comparison started at the top. If the two top hashes matched, everything matched: one comparison, done. If not, the software compared the next level down, found which folders differed, went into only those, and so on, down to the exact blocks. Finding three corrupted blocks among two terabytes took a few hundred comparisons and a few seconds. Only those blocks crossed the link.

There was a bonus she hadn't planned. Because each block was named by the hash of its contents, two identical blocks anywhere had the same name, and needed storing only once. Copies of the same presentation in twenty people's folders took the space of one.

Looking back, Ingrid thought the idea was simple once seen: if every piece is named by what it contains, and every group by the names of its pieces, then the name at the top tells you everything, and the names below tell you where to look.

## Where it shows up

| Page | The tree of hashes | What it gives |
| --- | --- | --- |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | git: files named by content, folders by their files, commits by their folder and their parents | Any change anywhere gives a new commit name, and two clones can find exactly what differs between them. |
| [Hashing](hashing.md) | The identity job | The same fingerprint used for naming, not lookup or secrecy. |
| [Graphs](graphs.md) | History as a directed graph with no cycles | Each commit points to its parents, and because names come from content, no commit can point to its own future. |
| [Consistency](../data/consistency.md) | Replicas comparing their contents | Copies can find where they disagree without sending everything. |

It shows up elsewhere too: deduplicating storage and backup systems, file-sharing networks, blockchains, and the public logs browsers use to check that certificates haven't been issued in secret.

What these share is that a name derived from content can't lie about the content. Building names from names makes one value at the top vouch for everything below, and makes differences cheap to find.

## It really happened

Ingrid is fictional; the tree is Ralph Merkle's, who described it in 1979 for signing many messages efficiently. Amazon's Dynamo (2007) used Merkle trees so that replicas could find where they disagreed by exchanging a few hashes instead of all their data ([page 8](../08-too-many-users-too-much-data.md)). git, released in 2005, names every file, folder and commit this way, which is why a commit ID identifies an entire history ([page 10](../10-many-people-one-codebase.md)). Certificate Transparency, standardised in 2013, puts every issued web certificate into public Merkle-tree logs, so anyone can check that a certificate for their domain wasn't issued without their knowledge.

## What it is

A Merkle tree is a tree in which each leaf is labelled with the hash of a block of data and each parent with the hash of its children's labels. The root's hash commits to all the data. Two trees can be compared by walking down only where hashes differ, and any single block can be proved to belong by giving the hashes along its path. A Merkle DAG generalises this to graphs where nodes can share children and point to several parents, as git's commits do.

## Where it gets misapplied

- **One checksum for everything.** Ingrid's first fix: it detects a difference and can't locate it.
- **A weak hash for identity.** The whole structure is only as trustworthy as the hash function; git's move away from SHA-1 is about exactly this ([hashing](hashing.md)).
- **Assuming content-addressing means immutable everything is free.** Every change makes new nodes; old ones need garbage collection.
- **The mirror:** building a hash tree to compare two small files that could simply be compared.

## Connections

- Learning this is also learning [hashing](hashing.md), because every name in the tree is a hash.
- Learning this is also learning [graphs](graphs.md), because git's history is a directed graph with no cycles.
- Learning this is also learning [replication](../data/replication.md), because replicas use hash trees to find and repair differences.
- Learning this is also learning [code signing](../auth/code-signing.md), because signing a root hash signs everything beneath it.
- Learning this is also learning [storage tiers](../cost/storage-tiers.md), because naming blocks by content lets identical blocks be stored once.

## Resources

1. Scott Chacon and Ben Straub, [*Pro Git*](https://git-scm.com/book/en/v2), chapter 10, "Git Internals" (start here: the structure, by poking at it). <!-- verify -->
2. DeCandia et al., [the Dynamo paper](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html), on anti-entropy with Merkle trees (go deeper).
3. Ralph Merkle, "A Digital Signature Based on a Conventional Encryption Function" (1987, from 1979 work) (reference).

## Names you'll hear

- **Merkle tree, hash tree:** a tree of hashes with one root.
- **Content-addressed storage:** finding data by the hash of its contents rather than by location.
- **DAG:** directed acyclic graph.
- **Deduplication:** storing identical content once.
- **Anti-entropy:** replicas comparing and repairing their differences in the background.
- **Inclusion proof:** the hashes along a path that prove one item is in the tree.

## Go and look

In a git repository, run `git cat-file -p HEAD`, then follow the tree hash it shows with `git cat-file -p` again. You're walking down a Merkle DAG by hand.
