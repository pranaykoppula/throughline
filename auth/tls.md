# TLS

Last reviewed: 2026-10-24

A concept page: how two machines that have never met agree on a secret, and prove who they are, over a network anyone can read.

## Problem

Data crossing a network passes through machines you don't control, and any of them can read it or change it. Encryption hides it, but encryption needs a key both sides know, and they can't safely agree on one over the same network. And even with a secret channel, you need to know you're talking to the right party, not an impostor in the middle.

## The story

In 1995 Dev Malhotra was the only programmer at a small online bookshop. Customers typed their card numbers into a web form, and the form sent them across the internet as plain text. Dev knew that every machine along the way, at the customer's internet provider and every hop after, could read them. He also knew most of his customers didn't.

His first fix was to encrypt the card number in the customer's browser before sending it, using a small program the site downloaded. The program and the server shared a secret key, built into both, so the server could decrypt what the browser encrypted. It was simple, and from the outside the card numbers now looked like noise.

A month later a customer who happened to be a programmer emailed him, politely. He'd opened the downloaded program, found the key inside it in about ten minutes, and could now decrypt any card number sent by any customer, if he could see their traffic. Every copy of the program carried the same key. Hiding it better would only slow the next person down. And there was a second problem the customer pointed out: nothing told a browser it was really talking to Dev's server. Someone in the middle could pretend to be the bookshop, and the browser would happily encrypt card numbers for them.

*Before reading on: a shared key built into the software could be found by anyone who looked, and nothing proved who was on the other end. What would you need instead?*

The answer Dev adopted wasn't his own. The new version of the browser most of his customers used supported a protocol that solved both problems. For the key, it used public-key cryptography. The server had a pair of keys: a public one it gave to anyone, and a private one it never sent. A browser could use the public key to agree on a fresh secret for that one conversation, which only the server could take part in. No shared key was built into anything, and each conversation's key was different. For identity, the server's public key came in a certificate signed by a company the browser already trusted, vouching that this key belonged to this domain. An impostor could copy the certificate but not the private key that matched it.

Dev bought a certificate, which was expensive and took two weeks of paperwork, and the little padlock appeared in his customers' browsers. Card numbers now crossed the internet encrypted with a key nobody else had, to a server the browser had checked.

Looking back, Dev thought his first fix had failed for a reason that went beyond cryptography. A secret shared by every copy of a program isn't a secret. And encryption without identity just means you're having a private conversation with whoever answered.

## Where it shows up

| Page | The boundary | What TLS provides |
| --- | --- | --- |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | A network you can't see into | Confidence about who is on the other end, and that nobody along the way read or changed the data. |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | Passwords and session tokens crossing the internet | They travel encrypted, so the hops in between can't steal them. |
| [Round trips](../latency/round-trips.md) | The handshake before any data | A secure connection costs extra round trips to set up, which newer versions work to reduce. |
| [Input validation](input-validation.md) | Knowing who sent something | A separate question from whether what they sent is safe; TLS answers the first, not the second. |

It shows up elsewhere too: email between servers, connections between services inside a company, phone apps talking to their backends, and software updates checked by signature.

What these share is the split Dev learned: confidentiality, nobody else can read it, and authentication, it really is who it claims to be. You need both, and neither guarantees the content is harmless.

## It really happened

Dev is fictional; the browser was Netscape Navigator, whose SSL protocol, the predecessor of TLS, launched in 1995. Its first versions had their own failure of exactly Dev's kind. In 1995 Ian Goldberg and David Wagner showed that Netscape generated its session keys from a seed built from the time and process numbers, which an attacker could often guess, so the "fresh secret" wasn't secret at all ([Goldberg and Wagner](https://people.eecs.berkeley.edu/~daw/papers/ddj-netscape.html)). The public-key ideas underneath went back to Whitfield Diffie and Martin Hellman in 1976 and to RSA in 1977. Certificates stayed expensive and fiddly until Let's Encrypt began issuing them free and automatically in 2015, and most web traffic is now encrypted.

## What it is

TLS (Transport Layer Security, the successor to SSL) creates an encrypted, authenticated connection between two parties over an untrusted network. A handshake uses public-key cryptography to agree on fresh session keys and uses certificates, signed by authorities the client trusts, to prove the server's identity. After that, data is encrypted and protected against tampering. TLS protects data in transit; it says nothing about whether the server, or the data, can be trusted.

## Where it gets misapplied

- **Turning off certificate checks.** Code that skips verification "just for now" gets encryption to an unknown party, Dev's second problem.
- **Treating the padlock as trust.** It proves you reached the domain you typed, not that the site is honest. Scam sites have valid certificates too.
- **Encrypting only the login page.** Session tokens sent in plain text afterwards are as good as the password.
- **The mirror:** skipping encryption inside your own network because it's "internal". Attackers who get in once can then read everything.

## Connections

- Learning this is also learning [sessions and tokens](sessions-and-tokens.md), because TLS protects tokens in transit, and they need protecting.
- Learning this is also learning [round trips](../latency/round-trips.md), because the handshake costs round trips before any data moves.
- Learning this is also learning [code signing](code-signing.md), because certificates and signatures use the same public-key idea to prove who made something.
- Learning this is also learning [input validation](input-validation.md), because knowing who sent something and knowing it's safe are separate questions.
- Learning this is also learning [hashing](../dsa/hashing.md), because TLS uses cryptographic hashes to detect tampering.

## Resources

1. Julia Evans, ["How HTTPS works"](https://wizardzines.com/comics/how-https-works/) or similar short illustrated explanations (start here). <!-- verify -->
2. Ilya Grigorik, [*High Performance Browser Networking*](https://hpbn.co/), the TLS chapter (go deeper: what the handshake costs). <!-- verify -->
3. Goldberg and Wagner, ["Randomness and the Netscape Browser"](https://people.eecs.berkeley.edu/~daw/papers/ddj-netscape.html) (1996) (reference: short, and a lesson in where secrets come from).

## Names you'll hear

- **SSL, TLS, HTTPS:** the old name, the current protocol, and the web over it.
- **Certificate, certificate authority:** a signed statement that a public key belongs to a domain, and the organisation that signs it.
- **Public and private key:** a pair where one can be shared and the other never leaves its owner.
- **Handshake:** the setup exchange before encrypted data flows.
- **Man-in-the-middle:** an attacker who sits between two parties and pretends to each to be the other.
- **Forward secrecy:** fresh keys per session, so stealing a server's private key later doesn't unlock past conversations.

## Go and look

Click the padlock on a site you use and look at its certificate: who issued it, for which names, and when it expires. Then find out how a service you run renews its own.
