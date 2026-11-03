# Error detection and correction

Last reviewed: 2026-11-03

A concept page in the information family: adding redundancy in a structured way, so a damaged message can tell you it's damaged, and sometimes how to fix itself.

## Problem

Every disk, cable, radio link and memory chip occasionally flips a bit. Most of the time nobody notices, because the damage lands somewhere that doesn't matter, or nobody looks. Keeping a second copy seems like protection, but two copies that disagree don't say which one is right, and a copy made from damaged data is just as damaged. Protection that works has to be designed: redundancy arranged so that errors are detected, located, and corrected.

## The story

In 2004 Felipe Ortega ran the research data archive at a university: twenty years of measurements from labs across the campus, on a row of cheap disks. Disks failed now and then, so every file was stored twice, on two different disks. When one disk died, the other still had everything, and Felipe copied it onto a new disk. Mirroring was simple, it had saved the archive several times, and it was what everyone did.

In 2009 a climate researcher opened a dataset from 2003 and found nonsense in a few hundred rows: temperatures of minus four thousand degrees, dates in the year 2600. Felipe checked the two copies. They disagreed with each other, in different places. Somewhere over six years, a few bits had flipped on each disk, silently, in files nobody had opened. Now he had two versions of the file and no way to know which bytes were right. Neither copy recorded what it was supposed to contain.

Worse, he found other files where both copies were damaged identically. When a disk had died years before, the rebuild had copied the surviving disk's files onto the new one. Some of those files had already decayed, so the mirror had faithfully duplicated the damage. Two copies had protected the archive from losing a disk. They hadn't protected it from slowly losing its contents.

*Before reading on: two copies could say "something differs" but not what was right, and could copy the damage too. What would you have added?*

Felipe added three things. First, a checksum for every block of every file, computed when the data was first written and stored separately from it. Whenever a block was read, its checksum was recomputed and compared. Now a mismatch didn't just say "these copies differ"; it said which copy was wrong, and the good copy could repair the bad one immediately. Second, the system read every block of the archive once a month, checking every checksum, whether anyone needed the data or not, so decay was found and repaired while a good copy still existed. Third, for the bulk of the archive, he replaced mirroring with erasure coding. Each file was split into, say, ten pieces, and four extra pieces were computed from them, so that any four of the fourteen could be lost and the file rebuilt from the rest. It survived more failures than two copies did, and used 40% extra space instead of 100%.

The archive was never perfectly safe. But from then on, errors were found by the system, on a schedule, not by a researcher, years later.

Looking back, Felipe thought he'd learned that redundancy only works if it's structured. A second copy can tell you something might be wrong. A checksum tells you which part is wrong. A correcting code tells you what it should have been. And none of them help with data nobody ever checks.

## Where it shows up

| Page | The redundancy | What it could do |
| --- | --- | --- |
| [Information](information.md) | Code words differing in at least two letters | Detect a single garbled letter, though not fix it. Thomas's telegraph code. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Numbered blocks, confirmations and checksums on every packet | Detect loss, duplication and damage, then resend. |
| [Replication](../data/replication.md) | Replicas of a database | Survive a machine dying, and faithfully copy a mistake. |
| [Storage tiers](../cost/storage-tiers.md) | Facebook's warm storage using erasure coding | Survive failures with less space than full copies. |
| [Merkle DAGs](../dsa/merkle-dags.md) | Hashes of blocks, then of hashes | Find exactly which blocks differ between two copies. |

It shows up elsewhere too: memory chips that correct their own errors, CDs and QR codes that still work when scratched or smudged, check digits on card numbers and book ISBNs, and the parity in RAID storage.

What these share is a ladder of protection, each rung costing more redundancy. A copy can show that something differs. A check can show which part is wrong. A correcting code can repair it without asking anyone. Thomas's telegraph rule was the first rung, and Felipe's archive needed all three.

## It really happened

Felipe is fictional. Richard Hamming, a mathematician at Bell Labs in the late 1940s, could only use the lab's relay computer at weekends. The machine could detect some of its own errors, and when it did, it simply abandoned the job, so Hamming would come in on Monday to find nothing done. He asked, in effect, why a machine that could detect an error couldn't work out where the error was and fix it. His answer, published in 1950, was the first family of error-correcting codes: extra bits arranged so that the pattern of failed checks points directly at the flipped bit ([IEEE Computer Society](https://history.computer.org/pioneers/hamming.html)).

In 1960 Irving Reed and Gustave Solomon published codes that could repair whole runs of damaged symbols. Reed–Solomon codes went into deep-space probes, CDs and DVDs. They're also why a QR code can still be read with up to about 30% of its data damaged at its highest correction level, at the cost of holding less. Hans Peter Luhn, who wrote the first memo on hashing ([hashing](../dsa/hashing.md)), also devised the check digit still used on payment card numbers, which catches any single mistyped digit. In 2005 Sun's ZFS file system made Felipe's first two fixes standard for ordinary storage: a checksum on every block, verified on every read, and regular scrubs of the whole disk.

## What it is

Error detection adds redundancy, such as parity bits, checksums or check digits, so that damaged data can be recognised. Error correction adds enough structured redundancy that the original can be reconstructed: Hamming codes for single flipped bits, Reed–Solomon and other erasure codes for missing or damaged pieces. Shannon proved that reliable communication over a noisy channel is possible if redundancy is added in the right way. In storage, protection also needs end-to-end checksums, stored apart from the data, and regular scrubbing, because errors in data nobody reads go unnoticed until it's too late.

## Where it gets misapplied

- **Copies without checks.** Two copies can't say which one is right, and a rebuild copies whatever damage exists.
- **Never reading the data.** Errors accumulate silently in files nobody opens; scrub on a schedule.
- **Checksums stored next to the data they protect.** If one corruption can damage both, the check proves nothing.
- **The mirror:** heavy correction on data that's cheap to fetch again. A cache or a downloaded file can just be fetched again when its checksum fails.

## Connections

- Learning this is also learning [information](information.md), because error correction is redundancy put back on purpose, after compression took it out.
- Learning this is also learning [hashing](../dsa/hashing.md), because a checksum is a hash used for detection rather than lookup.
- Learning this is also learning [Merkle DAGs](../dsa/merkle-dags.md), because a tree of checksums finds exactly where two copies differ.
- Learning this is also learning [replication](../data/replication.md), because replicas protect against losing a machine, not against slowly corrupting data.
- Learning this is also learning [storage tiers](../cost/storage-tiers.md), because erasure coding trades computation for space, and changes what each tier costs.

## Resources

1. Richard Hamming, *The Art of Doing Science and Engineering* (1997), the chapters on coding theory (start here: his own account, in his own voice).
2. Richard Hamming, "Error Detecting and Error Correcting Codes" (*Bell System Technical Journal*, 1950) (go deeper).
3. Your storage system's documentation on checksums, scrubbing and erasure coding (reference).

## Names you'll hear

- **Parity bit:** one extra bit making the count of ones even or odd, which detects a single flipped bit.
- **Checksum, CRC:** a short value computed from data to detect damage.
- **Hamming code:** a code that can locate and fix a single flipped bit.
- **Reed–Solomon, erasure coding:** codes that rebuild missing or damaged pieces from the rest.
- **Bit rot:** silent decay of stored data over time.
- **Scrubbing:** reading all stored data on a schedule to find and repair errors.
- **ECC memory:** memory that corrects its own single-bit errors.

## Go and look

Find out what happens if one bit flips in a file in the storage you use most: would anything notice, and when? Then find out when that storage last read every block it holds.
