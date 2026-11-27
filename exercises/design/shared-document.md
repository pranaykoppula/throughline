# Two cursors, one sentence

A design case in the category **real-time messaging**. It draws on [time and ordering](../../design/time-and-ordering.md), [consistency](../../data/consistency.md), [replication](../../data/replication.md) and [append-only logs](../../dsa/append-only-logs.md).

## The situation

A company makes a writing tool for legal teams. Several lawyers often edit the same contract at once, and they expect to see each other's typing within a moment, with a coloured cursor for each person. They also work on trains and planes, and expect to keep editing offline and have their changes merge when they reconnect. The first version saved the whole document every few seconds and kept whichever version arrived last. Lawyers lost paragraphs, silently, whenever two of them edited at the same time.

## Requirements and numbers

- Each person's typing appears for everyone else within about a quarter of a second.
- Concurrent edits are merged, never lost. Everyone ends up with the same document.
- Editing works offline, and changes merge on reconnecting, even after hours.
- Full history: who changed what, and the ability to go back.
- Documents of up to a few hundred pages, usually 2 to 10 editors at a time, occasionally 50. About a million documents edited each day.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** A stream of tiny edits, each made against the version of the document its author could see, which may not be the latest.
- **How does it fail?** Two people change the same place at the same moment; someone edits offline for hours.
- **What must always work?** Nobody's change disappears, and everyone ends up looking at the same text.

## The tempting first design

Save the whole document on every change, and keep the latest save. Or, a little better, send each edit as "insert 'not ' at position 120" and apply edits in the order the server receives them.

Saving whole documents loses every change except the last. Sending positions fails more subtly. If Ana deletes the first sentence while Ben inserts a word at position 120, then by the time Ben's edit arrives, position 120 is somewhere else, and his word lands in the middle of the wrong sentence. Each person's edit was right for the document they saw, and wrong for the one it was applied to.

## Hints

<details markdown="1"><summary>Hint 1</summary>

An edit says "at position 120" because that's where the author saw it. What would you need to know to work out where that place is now, after other people's edits?

</details>

<details markdown="1"><summary>Hint 2</summary>

One approach is to adjust each incoming edit for the edits it didn't know about. Another is to stop using positions altogether. What could identify a place in the text that doesn't move when text is inserted before it?

</details>

<details markdown="1"><summary>Hint 3</summary>

For offline editing, there's no server to decide the order while you're away. What would let two copies that each saw different edits merge to the same result, whatever order they combine in?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

Fast typists make about five edits a second. Ten editors on one document is about 50 edits a second, each a few dozen bytes; across a million documents a day, most of them idle at any moment, the total is modest. The difficulty isn't volume. It's that edits made at the same moment against different versions must be combined correctly ([estimates](../../design/estimates.md)).

### Design A: a server orders edits and transforms them

- **One owner per document.** While a document is being edited, one server process owns it, chosen by hashing the document's ID. Every editor's connection goes to that owner ([partitioning](../../data/partitioning.md)).
- **Edits carry the version they were made against.** Each edit says "insert 'not ' at 120, made against version 341". The owner keeps a log of applied edits numbered in order ([append-only logs](../../dsa/append-only-logs.md), [time and ordering](../../design/time-and-ordering.md)).
- **Transform before applying.** If the document is now at version 344, the owner adjusts the incoming edit for edits 342 to 344: if one of them inserted five characters before position 120, the new edit's position becomes 125. This adjustment, *operational transformation*, has rules for every pair of edit types. The transformed edit is applied, numbered 345, and sent to everyone.
- **Each editor does the same locally,** so their own typing appears instantly and is adjusted when others' edits arrive.
- **Snapshots and history.** Every few hundred edits, the owner saves a snapshot; history is the log between snapshots.

**What it costs:** the transformation rules are notoriously hard to get right for rich text, and correctness depends on the server ordering everything, so long offline editing is awkward: hours of edits must be transformed against hours of others' edits when the editor reconnects.

### Design B: edits that merge themselves

Each character gets a permanent identity, such as the editor's ID and a counter, and an insertion says "after character (Ana, 1,042)", not "at position 120". Deletions mark characters as removed rather than erasing them. Ties, two insertions after the same character, are broken by a fixed rule, such as comparing the editors' IDs. Structures built like this, called *CRDTs* (conflict-free replicated data types), have the property that any two copies that have seen the same set of edits are identical, whatever order the edits arrived in ([consistency](../../data/consistency.md)).

**What it gives:** no need for a central order. Offline editing works naturally, editors can even sync directly with each other, and the server becomes a relay and a store.

**What it costs:** every character carries an identity and removed characters linger, so documents use more memory and need periodic compaction. Merges are always consistent but not always what a person would have chosen: two people retyping the same word at the same moment can produce both words.

</details>

## What breaks at ten times the size

- **Fifty editors on one document.** One owner process per document becomes a hot spot; split very large documents into sections that are owned separately.
- **Memory.** History and the identities of removed characters grow; compact them, while keeping enough to merge with editors who've been offline a long time.
- **Cursors and presence.** Showing where everyone is typing is more traffic than the edits themselves; send it less often, and never store it.

## Where people slip

- **Keeping the last save.** It's last write wins, and it loses everything else.
- **Applying positions without adjusting them.** Each edit was right for the document its author saw, not the one it's applied to.
- **Ordering edits by timestamp.** Editors' clocks disagree, and the order of edits has to come from the document, not from the clocks ([time and ordering](../../design/time-and-ordering.md)).
- **Promising the merge is what people meant.** It's guaranteed to be the same for everyone, not to be sensible; show who changed what so people can fix it.

## Related

- The other case in this category: [the school's messages](group-chat.md), group chat with receipts.
- Design pages: [time and ordering](../../design/time-and-ordering.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [consistency](../../data/consistency.md), [replication](../../data/replication.md), [append-only logs](../../dsa/append-only-logs.md), [partitioning](../../data/partitioning.md), [10, Many people, one codebase](../../10-many-people-one-codebase.md), where merging edits made apart is version control's job.
