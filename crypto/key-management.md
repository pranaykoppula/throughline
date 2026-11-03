# Key management

Last reviewed: 2026-11-03

A concept page in the cryptography family: where keys live, who and what can use them, how they're replaced, and what you do on the day one leaks. It's where most real cryptographic systems actually fail.

## Problem

Ciphers are strong, so attackers don't attack them; they go after the keys. Every key has a life: it's made, stored, used, copied, rotated and eventually retired. At each step it can leak, and a leaked key gives an attacker everything it protects, often silently. The motive is simple: assume a key will leak someday, and design so that day is survivable.

## The story

In 2015 Bram de Vries was the second engineer at a payments startup in Amsterdam. When a customer logged in, the backend gave their app a token, signed with a secret key, which proved who they were on every later request. One signing key, created on launch day, was used everywhere. It lived in a configuration file that every server read. Bram had copied it to his laptop to debug a login problem, and so had two other developers. Nobody ever changed it, for a good reason: changing it would invalidate every token and log out every customer at once.

In 2017 a contractor who'd left the company months earlier still had a copy of an old configuration backup on a personal cloud drive, which was public. Someone found it. With the signing key, they could make tokens for any customer, and the backend would accept them as genuine, because they were. They emptied three accounts before the fraud team noticed odd transfers.

Bram's team now had to change the key, and found they couldn't do it quickly. The key was written into the configuration of nine services, two of which were owned by a partner. The new key had to reach all of them at the same moment, or customers would be logged in on some services and rejected by others. It took three days of carefully ordered deploys. And because the forged tokens were perfect, they couldn't tell from the logs which past logins had been real.

*Before reading on: the key had been stable for two years because changing it was so disruptive, and that's exactly what made the leak so bad. How would you have arranged things so that changing a key was routine?*

Bram rebuilt the company's handling of keys around one assumption: every key will eventually leak, so make replacing one boring. Signing keys moved into a managed key service, backed by hardware, which applications could ask to sign or check a token but which never handed the key itself to anyone, so no file, laptop or backup could ever contain it. Every token now said which key had signed it, by a short key ID, and services accepted any of a small published set of current keys. That meant a new key could be introduced, used for new tokens, and the old one retired a day later, with nobody logged out. Rotation then became automatic, every month, so the procedure was exercised constantly instead of being a three-day emergency. Tokens became short-lived, so a stolen one stopped working within the hour. Keys were split by purpose: one for customer tokens, another for partner messages, another for backups, so one leak exposed one thing. Every use of a key was logged. And twice a year, the team rehearsed the bad day: declare a key compromised, replace it, and time how long it took.

Looking back, Bram thought the original key hadn't failed because it was weak. It failed because it was everywhere, lived forever, and couldn't be changed without hurting everyone. Good key management was mostly making the key nowhere, short-lived, and easy to replace.

## Where it shows up

| Page | The key | Where it went wrong, or right |
| --- | --- | --- |
| [Symmetric encryption](symmetric-encryption.md) | Seun's database encryption key | Kept on the same server as the data, until it moved to a separate key service. |
| [Public-key cryptography](public-key.md) | Arvind's offline company key | Kept offline, used only to sign employees' keys: one well-guarded key vouching for the rest. |
| [Code signing](../auth/code-signing.md) | Harriet's release-signing key | Moved to an offline machine, which then signed whatever a compromised build gave it. |
| [Cloud IAM](../auth/cloud-iam.md) | Leila's one administrator access key | Used everywhere and never expiring, until it was pushed to a public repository. |
| [Sessions and tokens](../auth/sessions-and-tokens.md) | Signed tokens that can't be cancelled early | Why they should be short-lived. |
| [Password storage](../auth/password-storage.md) | Dropbox's pepper | Kept apart from the database, so stealing one isn't enough. |

It shows up elsewhere too: API keys for third-party services, SSH keys on old laptops, TLS certificates that expire on a weekend, database passwords in environment variables, and the key that encrypts every backup.

What these share is a set of questions that matter more than the choice of cipher. Where does the key live, and who or what can use it? How long does it last? How is it replaced, and has anyone practised that? What does it protect, and is that the only thing it protects? And what happens on the day it leaks?

## It really happened

Bram is fictional. In 2023 a group Microsoft calls Storm-0558 used a Microsoft consumer-account signing key, created in 2016, to forge tokens and read the email of about two dozen organisations, including US government agencies. A flaw in token validation meant tokens signed with a consumer key were accepted by enterprise email systems. The US Cyber Safety Review Board's 2024 report called the intrusion preventable and described a cascade of security failures. Microsoft still had not determined how the key was stolen. Its earlier theory, that the key had leaked through a crash dump, was later revised ([Help Net Security](https://www.helpnetsecurity.com/2024/04/03/microsoft-storm-0558-key/)). Both the board and Microsoft pointed to the same lessons as Bram's: automate rotation, retire old keys, and keep keys out of places they can be copied from.

In 2011 attackers broke into DigiNotar, a Dutch certificate authority, and used its signing keys to issue hundreds of fraudulent certificates, including one for google.com that was used to intercept users in Iran. Browsers removed DigiNotar from their trusted lists within weeks, and the company was declared bankrupt that September ([The Register](https://www.theregister.com/2011/09/20/diginotar_bankrupt/)). For a certificate authority, the keys are the business.

## What it is

Key management covers a key's whole life: generating it from good randomness, storing it, controlling access to it, using it, rotating it, revoking it when compromised, and retiring it. Good practice keeps keys in dedicated key services or hardware security modules that perform operations without exposing the key, separates keys by purpose, labels each key with an ID so several can be valid at once, rotates automatically, prefers short-lived credentials, logs every use, and rehearses compromise. The aim isn't a key that never leaks. It's a leak that's contained, noticed and quickly fixed.

## Where it gets misapplied

- **One key, forever, everywhere.** Bram's 2015 setup: stable, convenient, and catastrophic to replace.
- **Keys in files.** Configuration files, environment variables and source code get copied, backed up and leaked.
- **Rotation that's never practised.** A procedure run once a year, or never, fails on the day it's needed.
- **One key for many purposes.** A leak in one place exposes everything else it protects.
- **The mirror:** so much ceremony around keys that teams avoid encryption, or share one key to get around the process. Make the safe way the easy way.

## Connections

- Learning this is also learning [cloud IAM](../auth/cloud-iam.md), because cloud credentials are keys, with the same life cycle.
- Learning this is also learning [least privilege](../auth/least-privilege.md), because a key service that signs without revealing the key is least privilege for secrets.
- Learning this is also learning [randomness](randomness.md), because a key is only as strong as the randomness it was generated from.
- Learning this is also learning [VM provisioning](../cloud/vm-provisioning.md), because servers built from code need to get keys without anyone copying them in by hand.
- Learning this is also learning [the cost of reliability](../cost/reliability.md), because rehearsing the bad day is what makes recovery fast, for keys as for outages.

## Resources

1. [OWASP Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html) (start here). <!-- verify -->
2. The US Cyber Safety Review Board's report on the 2023 Exchange Online intrusion (2024) (go deeper: a frank account of key management failing at very large scale).
3. Your cloud provider's key management service documentation, on rotation and key IDs (reference).

## Names you'll hear

- **KMS, HSM:** a key management service, and a hardware security module that holds keys and uses them without letting them out.
- **Rotation:** replacing a key on a schedule.
- **Revocation:** declaring a key no longer trustworthy before it expires.
- **Key ID (kid):** a label on a signature or ciphertext saying which key made it.
- **Envelope encryption:** encrypting data with a data key, and the data key with a key held in a key service.
- **Secret sprawl:** copies of keys and credentials scattered across files, laptops and logs.

## Go and look

Pick one important key or secret in something you run and answer: where does it live, how many copies exist, when was it last changed, and how long would replacing it take today? If you don't know the last one, that's the drill to run.
