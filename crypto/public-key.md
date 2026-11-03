# Public-key cryptography

Last reviewed: 2026-11-03

A concept page in the cryptography family: how two parties who have never met can agree on a secret over a channel anyone can read, and how anyone can check who signed something, without either side ever sending a secret.

## Problem

Symmetric encryption needs both sides to hold the same key ([symmetric encryption](symmetric-encryption.md)). Getting it there is the hard part. Every pair of parties needs its own key, the number of pairs grows much faster than the number of parties, and each key has to travel by some route an adversary can't watch. Public-key cryptography removes the need to share a secret in advance. It doesn't remove the need to know whose key you're using.

## The story

In 1990 Arvind Rao looked after the computers for an engineering consultancy with forty offices, which exchanged drawings and contract files that clients insisted were kept confidential. Each pair of offices that worked together had its own encryption key, delivered on a floppy disk by courier and kept in a locked drawer. With forty offices, that could mean seven hundred and eighty keys. Every new office meant couriers to all the others. Every lost disk meant replacing keys across the country. Arvind spent more of his time arranging couriers than doing anything else.

His first fix was a central key server at head office. Each office shared a single key with the server, and when two offices needed to talk, the server made up a fresh key for them and sent it to each, encrypted with that office's key. Forty keys instead of seven hundred and eighty. It was a well-known design and it worked. But the server now knew every key in the company, and it had to be reachable for any two offices to talk. When head office lost its network connection for a day, nobody could exchange anything. And when an auditor asked who could read every confidential file in the firm, the honest answer was: whoever controlled one machine.

*Before reading on: every scheme so far needed a secret to travel from one party to another before they could talk. Is there any way to agree on a secret with someone without sending one?*

In 1994 the firm started using a newer kind of software, based on an idea that had seemed impossible to Arvind when he first read about it. Each person had two keys that worked as a pair. One was *public*: they could give it to anyone, publish it, and print it on a business card. The other was *private* and never left their computer. Anything encrypted with someone's public key could only be decrypted with their private key. To send a file to the Glasgow office, you encrypted it to Glasgow's public key; nobody who saw the public key, the file or the network could read it. In practice the software used the slow public-key step only to protect a fresh symmetric key for each file, then encrypted the file itself quickly with that. No couriers. No central server holding everything. Each new office published one public key and could talk to everyone.

The pair also worked the other way round. Something processed with a private key could be checked by anyone with the public key, which proved who had produced it and that it hadn't changed since. That was a *signature*, and the firm started signing contract files, so clients could check they hadn't been altered.

Six months later a junior engineer in Leeds received an email from a senior partner, or so it said: *I've had to set up a new key, please use this one for the payroll file from now on*, with a public key attached. He did. The key belonged to someone outside the firm. Nothing in the mathematics had failed. The engineer had encrypted perfectly securely, to the wrong person.

Arvind realised the problem hadn't gone away; it had moved. Public keys didn't have to be kept secret, but they did have to be *authentic*. He set up a rule: before using anyone's public key, check its fingerprint, a short summary of it, with its owner over the phone or in person. Then he went further. The firm created one key of its own, kept offline, whose only job was to sign the public keys of its employees once each had been checked in person. Software would accept a colleague's key only if the firm's key had signed it. Checking one key, the firm's, meant you could trust all of them.

Looking back, Arvind thought public-key cryptography had felt like magic and was really a trade. It turned the problem of keeping shared secrets into the problem of knowing whose public key was whose. That second problem was easier, but it didn't solve itself.

## Where it shows up

| Page | The public key | What it solved, and what it left |
| --- | --- | --- |
| [TLS](../auth/tls.md) | Dev's bookshop's server key | Agreeing on a fresh secret with every browser, and proving which shop you'd reached, through a certificate. |
| [Code signing](../auth/code-signing.md) | Harriet's release key | Proving an update came from her, unchanged. Not that her build was clean. |
| [Communication with adversaries](../info/secrecy.md) | Lionel's couriers carrying key lists | The problem public keys replaced: secrets that had to travel by a trusted route. |
| [Symmetric encryption](symmetric-encryption.md) | The session keys inside every public-key system | Public keys are slow, so they protect a symmetric key, which protects the data. |
| [Merkle DAGs](../dsa/merkle-dags.md) | A signed git tag | One signature on a root hash vouches for a whole history. |

It shows up elsewhere too: SSH keys, signed emails, cryptocurrency wallets, passkeys, and the certificates in every browser.

What these share is the same two-part bargain. Public-key cryptography lets strangers agree on secrets and lets anyone check a signature, without sharing a secret first. In exchange, everything depends on knowing whose public key you hold, which is why certificates, signatures on keys, and in-person fingerprint checks exist.

## It really happened

Arvind is fictional. Whitfield Diffie and Martin Hellman published "New Directions in Cryptography" in 1976, showing how two parties could agree on a shared secret over a public channel. In 1977 Ron Rivest, Adi Shamir and Leonard Adleman found RSA, a practical way to encrypt and sign with public and private keys. Honestly, they weren't first. At Britain's GCHQ, James Ellis, Clifford Cocks and Malcolm Williamson had found the same ideas between 1970 and 1974, but the work was classified, and it wasn't made public until 1997. The publicly published versions are the ones that changed the world.

In 1991 Phil Zimmermann released PGP, putting public-key encryption into ordinary people's hands for free. US export rules then treated strong cryptography like weapons, and he was the subject of a government investigation for three years before it was dropped in 1996. PGP's answer to Arvind's impostor problem was a "web of trust", where people signed each other's keys. The web settled instead on certificate authorities, organisations that browsers trust to vouch for which key belongs to which domain ([TLS](../auth/tls.md)).

## What it is

Public-key, or asymmetric, cryptography uses a key pair: a public key that can be shared freely and a private key that's kept secret. Key agreement, such as Diffie–Hellman, lets two parties derive a shared secret over an open channel. Encryption to a public key can only be undone with the matching private key. A signature made with a private key can be verified by anyone with the public key. Because it's slow, it's used to establish or protect symmetric keys, not to encrypt bulk data. Its central remaining problem is authenticity: binding a public key to its real owner, through certificates, signatures on keys, or verified fingerprints.

## Where it gets misapplied

- **Trusting a public key because it arrived.** Arvind's impostor: encryption to the wrong key is secure and useless.
- **Encrypting bulk data with public-key operations directly.** Slow, and easy to get wrong; protect a symmetric key instead.
- **Treating a signature as approval.** It proves who signed, not that what they signed is good ([code signing](../auth/code-signing.md)).
- **The mirror:** a central server holding everyone's keys "for simplicity". Sometimes right inside one organisation, but it gives up what public keys are for.

## Connections

- Learning this is also learning [symmetric encryption](symmetric-encryption.md), because public keys exist to deliver the symmetric key that does the real work.
- Learning this is also learning [TLS](../auth/tls.md), because every secure web connection starts with public-key key agreement and a certificate.
- Learning this is also learning [code signing](../auth/code-signing.md), because signatures are public-key cryptography run backwards.
- Learning this is also learning [key management](key-management.md), because a private key that leaks undoes everything, and knowing whose public key is whose is a management problem.
- Learning this is also learning [randomness](randomness.md), because key pairs must be generated from unpredictable numbers, or someone else can generate them too.

## Resources

1. Simon Singh, *The Code Book* (1999), the chapters on public keys (start here: the discovery, including GCHQ's, as a story).
2. Whitfield Diffie and Martin Hellman, "New Directions in Cryptography" (1976) (go deeper: readable, and the opening paragraph is a famous statement of the motive).
3. Jean-Philippe Aumasson, *Serious Cryptography*, the chapters on RSA, Diffie–Hellman and elliptic curves (reference).

## Names you'll hear

- **Public key, private key, key pair:** the shareable half, the secret half, and the two together.
- **Diffie–Hellman:** agreeing on a shared secret over an open channel.
- **RSA, elliptic curves:** the two main families of public-key mathematics in use.
- **Digital signature:** proof that the holder of a private key produced or approved some data.
- **Fingerprint:** a short hash of a public key, for checking it by eye or voice.
- **Certificate authority, web of trust:** two ways to vouch for whose key is whose.
- **Hybrid encryption:** public keys to protect a symmetric key, and the symmetric key to protect the data.

## Go and look

Run `ssh-keygen -lf` on a public key you use, or look at the certificate fingerprint of a site you trust. Then ask how you know that key really belongs to who you think, and what you'd do if you got a message saying it had changed.
