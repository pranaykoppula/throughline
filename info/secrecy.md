# Communication with adversaries

Last reviewed: 2026-11-03

A concept page, and the last of the information family: what changes when someone on the channel is working against you. Noise doesn't try to read, change or forge a message. An adversary does, and that motive is what cryptography exists to answer.

## Problem

Everything else in this family assumed a channel that was careless but indifferent: it dropped letters and flipped bits at random. An adversary is different. They read what isn't meant for them, change what's sent, or send messages pretending to be someone else, and they learn from everything you do. The features that made communication reliable, such as redundancy, patterns and predictability, become the things they use against you.

## The story

In 1912 Lionel Ashby ran the private telegraph code of a cotton broker in Liverpool. The firm cabled its buyers in New Orleans and Bombay every day, and those cables passed through the hands of clerks at several telegraph offices. Rival brokers would pay well to know what the firm was buying, so the firm's code wasn't only for saving money, as Thomas's had been. It was for keeping secrets. The codebook, a few hundred numbered code words for the firm's instructions, lived in the partners' safe, and only three copies existed.

That winter the firm noticed that a rival seemed to be a step ahead: buying the day before the firm did, selling just before it sold. The partners suspected someone had seen the codebook. Lionel checked the safe, the copies and the people who'd held them, and found nothing wrong. The book had never left.

The leak turned out to be a clerk at a cable office, who'd been passing copies of the firm's cables to the rival for months. The rival had never seen the codebook, and hadn't needed it. Before every large purchase, the same two code words appeared in the firm's cables. Prices were code words too, and they changed in a pattern that followed the market. After a few weeks of comparing cables with what the firm did the next day, the rival's clerk had worked out the meaning of the forty most common words. That was enough to read most of what mattered.

*Before reading on: the codebook stayed in the safe, and the secret leaked anyway. What would you have changed?*

Lionel started from a harder assumption: that the rival could see every cable the firm sent, and might one day get the codebook too. So secrecy couldn't depend on the book. Each code word was now looked up as a number, and a second number from a key list was added to it. Each page of the key list was used for one day only, and then destroyed. Both offices held identical key lists, sent by trusted courier. The same instruction now looked completely different every day, so its frequency told the rival nothing, and having the codebook alone was useless without that day's key. He also added a check group to each cable, computed from its contents with the day's key. When a forged cable arrived in New Orleans a few months later, telling the buyers to sell, it failed the check and wasn't acted on.

It was slower and more expensive, and the couriers carrying key lists became the most trusted people in the firm. Lionel came to think that was exactly right. The secret had moved from the codebook, which could be studied, copied or stolen, into a small, changing key, which could be protected.

Looking back, Lionel thought he'd learned that an adversary changes every question. Noise doesn't care what a message says; an enemy reads it, changes it, or writes their own. Patterns that helped the receiver helped them too. And the firm hadn't needed cryptography because it was clever. It needed cryptography because someone wanted what it was sending.

## Where it shows up

| Page | The adversary | What they wanted |
| --- | --- | --- |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | Whoever leaked Marcus's database | To read passwords, which is why they're stored so they can't be read. |
| [TLS](../auth/tls.md) | Anyone on the path between browser and server | To read card numbers, or to pretend to be the shop. |
| [Code signing](../auth/code-signing.md) | Whoever replaced Harriet's installer | To change what customers installed, and have it look genuine. |
| [Information](information.md) | Nobody, yet | Thomas's code had the same structure as Lionel's, but its only enemy was noise. |
| [Hashing](../dsa/hashing.md) | Strangers choosing keys for a hash table | To make a predictable hash slow everything down. |

It shows up elsewhere too: in session tokens, password resets, payment systems, messaging apps, and anywhere a message is worth reading, changing or forging to someone other than its sender and receiver.

What these share are the three things an adversary wants: to read what isn't theirs (confidentiality), to change it without being noticed (integrity), and to pretend to be someone else (authenticity). Every cryptographic method answers one or more of them. Which ones matter, against whom, and for how long, is the motive that should decide which methods to use. Without a motive, cryptography is just ceremony.

## It really happened

Lionel is fictional; his rival's method is the oldest in codebreaking. Commercial codebooks were used partly to keep business secret from telegraph clerks and competitors, and their predictable structure made them readable to anyone patient enough ([Bellovin, on commercial codes](https://www.cs.columbia.edu/~smb/papers/codebooks.pdf) <!-- verify -->). In 1917 British codebreakers read the Zimmermann telegram, Germany's secret proposal of an alliance with Mexico, and its publication helped bring the United States into the First World War. At Bletchley Park in the Second World War, codebreakers attacking the Enigma cipher relied heavily on *cribs*: phrases like weather reports and routine formulas that they could guess would appear in a message. Predictability was the weakness.

The key list Lionel adopted, used once and destroyed, is the idea behind the one-time pad, and in 1949 Claude Shannon proved what it requires. In "Communication Theory of Secrecy Systems", based on his wartime work, he showed that perfect secrecy is possible only if the key is truly random, at least as long as the message, and never reused. The Soviet Union learned what reuse costs. Under wartime pressure in 1942, its pad factory produced tens of thousands of duplicate pages. American codebreakers in the Venona project noticed number sequences that should never have repeated, and over the following decades read parts of thousands of Soviet messages. They never broke the pads; they exploited the reuse ([Venona project](https://en.wikipedia.org/wiki/Venona_project)). Auguste Kerckhoffs had stated Lionel's starting assumption in 1883: a system should stay secure even if everything about it except the key is known to the enemy.

## What it is

Communication with adversaries is communication over a channel where someone deliberately reads, alters or forges messages. Cryptography addresses three goals against them: confidentiality, so only intended receivers can read; integrity, so changes are detected; and authenticity, so the sender is who they claim. Kerckhoffs's principle puts all the secrecy in the key, not the method. Redundancy and predictability, which help against noise, help the adversary too, which is why good ciphers make output look random and keys must not be reused. The right methods depend on the motive: what's being protected, from whom, and for how long.

## Where it gets misapplied

- **Secrecy that depends on the method staying secret.** The firm's codebook. Methods leak; keys can be changed.
- **Reusing keys.** The Venona pads: a single reuse can unravel everything sent with them.
- **Confidentiality without integrity.** An encrypted message an attacker can change or forge undetected isn't safe.
- **The mirror:** cryptography with no threat in mind. Encrypting everything with no idea who it's protecting against, or for how long, adds cost and false confidence.

## Connections

- Learning this is also learning [information](information.md), because the redundancy that protects against noise is a gift to an adversary.
- Learning this is also learning [TLS](../auth/tls.md), because it's this page's three goals, applied to every connection on the web.
- Learning this is also learning [code signing](../auth/code-signing.md), because it answers integrity and authenticity, without confidentiality.
- Learning this is also learning [password storage](../auth/password-storage.md), because storing secrets assumes the adversary will one day read the database.
- Learning this is also learning [error detection and correction](error-correction.md), because a checksum stops noise and an adversary can simply recompute it; integrity against an adversary needs a key.
- Learning this is also learning [symmetric encryption](../crypto/symmetric-encryption.md), because Lionel's daily key list is its ancestor, and frequency analysis still works on encryption that lets identical messages look identical.

## Resources

1. Simon Singh, *The Code Book* (1999) (start here: the history of secret writing, from codebooks to public keys, as stories).
2. David Kahn, *The Codebreakers* (1967) (go deeper: the definitive history).
3. Claude Shannon, "Communication Theory of Secrecy Systems" (*Bell System Technical Journal*, 1949) (reference).

## Names you'll hear

- **Confidentiality, integrity, authenticity:** the three things an adversary attacks.
- **Kerckhoffs's principle:** only the key should be secret.
- **One-time pad:** a key as long as the message, used once; perfectly secret, and very hard to manage.
- **Crib:** a piece of a message a codebreaker can guess, used to break the rest.
- **Threat model:** a description of who the adversary is, what they want, and what they can do.
- **Frequency analysis:** reading a code by noticing which symbols appear most often.

## Go and look

Pick one thing you send or store that you'd call "secure", and write its threat model in three lines: who would want to read, change or forge it, and what they could already see. Then check that the protection matches the threat.
