# Symmetric encryption

Last reviewed: 2026-11-03

A concept page, and the first of the cryptography family: one shared key that locks and unlocks, the fastest way to **protect** data from someone who can see it, and the easiest to use in a way that quietly gives the secret away.

## Problem

The motive is confidentiality: someone will see the data, a stolen backup, a leaked database, a tapped connection, and they mustn't be able to read it ([communication with adversaries](../info/secrecy.md)). Symmetric encryption does that with one key shared by everyone allowed to read. The ciphers themselves are now very strong. Almost every failure comes from how they're used: patterns that survive encryption, changes nobody can detect, and keys kept next to the data they protect.

## The story

In 2009 Seun Adebayo built the backend for a company that ran an online pharmacy. Prescriptions were sensitive, so when the company's lawyers asked for patient medication data to be "encrypted at rest", Seun did it properly, he thought. He used AES, the government-standard cipher that nobody had broken, through the database library's simplest encryption function. Each value went in, an unreadable string came out, and the key went into the application's configuration. A stolen copy of the database would show columns of noise. It took two days, the lawyers were satisfied, and it was a sound decision.

A year later a security consultant, hired for an audit, was given a copy of the database with no key, to see what she could learn. She came back within a day with a list of every patient taking HIV medication. She hadn't broken AES. She'd noticed that the encrypted medication column contained only a few hundred distinct values, repeated across hundreds of thousands of rows. The same drug always encrypted to the same string. So she counted. The most common encrypted value appeared on a fifth of all prescriptions; it was almost certainly the commonest drug, which she could guess from public prescribing data. A few known pairings like that, and the frequencies of everything else, were enough to match most of the strings to drugs. Lionel's rival had done the same thing with telegrams in 1912 ([communication with adversaries](../info/secrecy.md)).

She had two more findings. She showed that she could swap one encrypted value for another in a row, so that a patient's record now said a different drug, and the application decrypted it without complaint. Nothing checked that the ciphertext hadn't been changed. And the key that would decrypt everything was in a configuration file on the same server as the database, so anyone who stole one would very likely have the other.

*Before reading on: the cipher was unbroken, and a copy of the database still revealed who took what, and could be altered without detection. What would you have changed?*

Seun's fix had three parts, and none of them involved a stronger cipher. First, every value was encrypted with a fresh, random *nonce*, a number used once, mixed in, so the same drug encrypted to a different string every time. Counting told the consultant nothing. Second, he switched to *authenticated encryption*, a mode that adds a tag computed with the key: any change to the ciphertext made decryption fail loudly instead of returning a different drug. Third, the key moved off the database server, into a separate key service that the application asked to decrypt, which a database thief couldn't reach. He chose all of this through a well-reviewed library whose one function did the right things by default, rather than assembling the pieces himself.

Looking back, Seun thought "encrypted" had been treated as a yes-or-no property, and it wasn't. The question was what an adversary holding the encrypted data could still learn, change, or reach, and his first answer had been: quite a lot.

## Where it shows up

| Page | The encryption | What it taught |
| --- | --- | --- |
| [Communication with adversaries](../info/secrecy.md) | Lionel's daily key list added to code numbers | The same message must look different every time, or frequencies give it away. |
| [TLS](../auth/tls.md) | The session keys after the handshake | Public-key methods agree on a key; symmetric encryption then protects everything sent, because it's fast. |
| [Password storage](../auth/password-storage.md) | Passwords that should have been hashed | Encryption can be undone by whoever holds the key; passwords should be stored so nobody can undo it. |
| [Error detection and correction](../info/error-correction.md) | A checksum against noise | An adversary can recompute a checksum; integrity against an adversary needs a tag made with a key. |
| [Multi-tenancy](../auth/multi-tenancy.md) | Each customer's data | Encryption with separate keys per tenant is one more wall between them. |

It shows up elsewhere too: encrypted disks and phones, encrypted backups, cloud storage encrypted at rest, messaging apps, and every VPN.

What these share is that symmetric encryption is a strong lock with three common ways to leave the door open: identical inputs giving identical outputs, ciphertext that can be changed without detection, and a key stored next to what it protects. The next pages take up the two questions this one leaves open: how two parties get a shared key in the first place ([public-key cryptography](public-key.md)), and where keys should live ([key management](key-management.md)).

## It really happened

Seun is fictional. In 2013 attackers copied a database of about 150 million Adobe user records, around 130 million of them with passwords. The passwords hadn't been hashed; they'd been encrypted with Triple DES in its simplest mode, ECB, so identical passwords produced identical ciphertexts. Combined with the users' password hints, stored in plain text, that let researchers work out huge numbers of passwords without ever having the key. The most common, shared by nearly two million accounts, was 123456 ([Infosecurity Magazine](https://www.infosecurity-magazine.com/news/adobe-breach-is-far-far-worse-than-originally/) <!-- verify -->). An image encrypted in ECB mode famously still shows its outline: Wikipedia's picture of the Linux penguin, encrypted, is still recognisably a penguin.

The ciphers themselves have a history of strength meeting time. DES, the US standard from 1977, used a 56-bit key, and in 1998 the Electronic Frontier Foundation built a machine for under $250,000 that found a DES key in 56 hours. Its replacement, AES, was chosen through an open public competition, with every candidate published for anyone to attack, which is Kerckhoffs's principle as policy. NIST selected the Rijndael design in 2000 and published the standard in 2001.

## What it is

Symmetric encryption uses one secret key to turn plaintext into ciphertext and back. Modern ciphers like AES and ChaCha20 are not practically breakable by brute force. Safe use needs more than the cipher: a mode that uses a fresh nonce or random value per message, so identical plaintexts don't produce identical ciphertexts; authentication, through authenticated encryption such as AES-GCM or ChaCha20-Poly1305, so tampering is detected; and keys kept apart from the data. In practice that means a vetted library with safe defaults, never a hand-assembled combination of parts.

## Where it gets misapplied

- **Deterministic encryption of low-variety data.** Seun's medication column: frequencies survive encryption.
- **Encryption without authentication.** An attacker who can't read a value may still be able to change it usefully.
- **The key next to the data.** One theft takes both.
- **Encrypting what should be hashed.** Passwords need to be checkable, not recoverable ([password storage](../auth/password-storage.md)).
- **The mirror:** inventing your own cipher or mode because the standard ones feel too simple to trust. They've survived decades of attack; yours has survived none.

## Connections

- Learning this is also learning [communication with adversaries](../info/secrecy.md), because confidentiality is the motive, and frequency analysis is the oldest attack.
- Learning this is also learning [public-key cryptography](public-key.md), because symmetric encryption needs a shared key, and getting one to a stranger is the problem public keys solve.
- Learning this is also learning [key management](key-management.md), because a strong cipher with an exposed key protects nothing.
- Learning this is also learning [randomness](randomness.md), because nonces and keys must be unpredictable, or the encryption leaks.
- Learning this is also learning [password storage](../auth/password-storage.md), because Adobe's passwords show what goes wrong when encryption is used where hashing belongs.

## Resources

1. Jean-Philippe Aumasson, *Serious Cryptography* (2nd edition, 2024) (start here: modern cryptography for engineers, without the maths getting in the way).
2. Dan Boneh's free online cryptography course (go deeper: the reasoning behind modes and authenticated encryption).
3. Your language's recommended high-level cryptography library, such as libsodium or its bindings (reference: the safe default).

## Names you'll hear

- **Plaintext, ciphertext, key:** the readable data, the encrypted data, and the secret that turns one into the other.
- **AES, ChaCha20:** today's standard symmetric ciphers.
- **Block cipher, mode:** a cipher that encrypts fixed-size blocks, and the rules for using it on longer data.
- **ECB:** the simplest mode, where identical blocks encrypt identically; avoid it.
- **Nonce, IV:** a value used once per message so repeated plaintexts don't repeat.
- **Authenticated encryption, AEAD, MAC:** encryption that also detects tampering, and the tag that does it.

## Go and look

Find one place where something you work on is "encrypted at rest" and answer three questions: do identical values look identical, would a change to the ciphertext be detected, and where is the key?
