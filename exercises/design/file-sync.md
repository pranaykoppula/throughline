# The three laptops

A design case in the category **large media**. It draws on [time and ordering](../../design/time-and-ordering.md), [Merkle DAGs](../../dsa/merkle-dags.md), [replication](../../data/replication.md) and [consistency](../../data/consistency.md).

## The situation

A small architecture practice keeps its project files in a shared folder that syncs to everyone's laptops. Drawings are large, from tens of megabytes to a few gigabytes, and architects often work offline on site visits or trains. The first sync tool uploaded a whole file whenever it changed, and decided which copy won by the time each laptop said the file was saved. When two architects edited the same drawing on a train and both synced that evening, one person's day of work vanished. And saving a small change to a two-gigabyte model sent all two gigabytes again over the office's connection.

## Requirements and numbers

- Each person's devices hold the same files, kept in step within seconds when online.
- Editing works offline, for days, and syncs on reconnecting.
- Conflicting edits are never silently lost.
- Small changes to large files sync quickly.
- History: any file can be restored to any version from the last 90 days.
- About 50 million users across many companies, 2 billion files, 20 petabytes stored.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** Many copies of the same files, each of which can change independently, sometimes for days.
- **How does it fail?** Two copies change the same file while apart; clocks on laptops disagree.
- **What's expensive?** Moving bytes, so move as few as possible.

## The tempting first design

Each laptop uploads a changed file in full to the server, with its modification time. The server keeps the newest one by time, and every other device downloads it.

Laptop clocks disagree, so "newest" can mean "on the laptop whose clock is fastest" ([time and ordering](../../design/time-and-ordering.md)). Two edits made offline to the same file are both "new", and one of them is thrown away. And re-sending two gigabytes for a one-megabyte change makes syncing over a site's mobile connection impossible.

## Hints

<details markdown="1"><summary>Hint 1</summary>

If a file were cut into blocks of a few megabytes, each named by a hash of its contents, what would a small change to a large file require sending?

</details>

<details markdown="1"><summary>Hint 2</summary>

Instead of timestamps, what could each copy of a file remember that would say whether one version descends from the other, or whether they were changed independently?

</details>

<details markdown="1"><summary>Hint 3</summary>

When two versions were changed independently and the files can't be merged automatically, what should the system do so that no work is lost?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

20 petabytes across 2 billion files is an average of 10 megabytes a file, but the distribution is lopsided: most files are small documents, and most bytes are in a few large ones. Many files are stored many times by different users, such as the same installer or the same shared drawing, so storing each distinct block once can save a large share of the space ([estimates](../../design/estimates.md)).

### Design A: content-addressed blocks and version histories

- **Blocks named by their contents.** Each file is split into blocks of a few megabytes, and each block is named by the hash of its contents. A file version is a list of block hashes. To upload a change, the client sends the new list and only the blocks the server doesn't already have. A small edit to a large file changes a few blocks, so it sends a few megabytes; a file someone else already uploaded sends nothing but its list ([Merkle DAGs](../../dsa/merkle-dags.md), [hashing](../../dsa/hashing.md)).
- **Splitting at content boundaries.** Cutting blocks at fixed positions means one inserted byte shifts every later block; cutting where a rolling hash of the contents hits a pattern keeps most blocks the same after an insertion.
- **Versions know their parents.** Each version of a file records which version it was based on. When a laptop syncs a change made on version 12, the server accepts it as version 13 only if the server's current version is still 12 ([time and ordering](../../design/time-and-ordering.md)).
- **Conflicts kept, not resolved.** If the server has moved on, both edits descend from version 12 independently. The server keeps both, saving the second as "drawing (Lena's conflicted copy)", and tells both users. Nothing is lost; a person decides ([consistency](../../data/consistency.md)).
- **A journal per user.** Every change to a user's files is an entry in an ordered journal on the server. A device syncs by asking for entries after the last one it saw, which also makes the 90-day history a matter of keeping old entries and blocks ([append-only logs](../../dsa/append-only-logs.md)).
- **Blocks stored once, many times over.** Blocks are stored in object storage, with copies in more than one data centre, and kept as long as any version refers to them ([replication](../../data/replication.md)).

**What it costs:** a metadata service that must be fast and consistent for each user, garbage collection of blocks nobody refers to, and conflicts that people must resolve by hand.

### Design B: operations instead of files

For formats the company understands, such as documents and spreadsheets, sync the edits themselves rather than the file, and merge them automatically, as a shared editor does ([two cursors, one sentence](shared-document.md)).

**What it gives:** no conflicted copies for those formats; two people's edits to different parts of a document both survive.

**What it costs:** it only works for formats whose structure the system understands. Architectural models from other vendors' software are opaque files, so they still need Design A. Most products combine them.

</details>

## What breaks at ten times the size

- **Metadata.** Ten times the files means ten times the journal entries and block lists; partition metadata by user or by shared folder, and keep each partition's operations ordered ([partitioning](../../data/partitioning.md)).
- **Shared folders across companies.** A folder shared by thousands of people has one journal that everyone reads; it becomes a hot partition.
- **Deduplication across users.** Storing a block once for everyone saves space, but whether a block exists leaks information about other users' files; deduplicate within a company, not across them, or encrypt blocks per customer.

## Where people slip

- **Newest timestamp wins.** Laptop clocks disagree, and offline edits are both "newest".
- **Silently picking one version.** Keep both, and say so.
- **Re-uploading whole files.** Split into blocks named by content, and send only what's new.
- **Fixed-size blocks.** An insertion near the start changes every block after it.
- **Deleting blocks too early.** A block may belong to an old version still within the history window.

## Related

- The other case in this category: [the lecture that buffered](video-streaming.md), video upload and streaming.
- Design pages: [time and ordering](../../design/time-and-ordering.md), [idempotency](../../design/idempotency.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [Merkle DAGs](../../dsa/merkle-dags.md), [hashing](../../dsa/hashing.md), [replication](../../data/replication.md), [consistency](../../data/consistency.md), [append-only logs](../../dsa/append-only-logs.md), [10, Many people, one codebase](../../10-many-people-one-codebase.md), where the same problem is merging branches.
