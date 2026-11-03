# Randomness

Last reviewed: 2026-11-03

A concept page, and the last of the cryptography family: every key, nonce and token is only as secret as the randomness it came from, and a computer is a machine built not to be random.

## Problem

Cryptography needs numbers nobody can guess: keys, nonces, session tokens, password-reset links. Computers are deterministic: given the same state, they do the same thing. So random numbers have to be gathered from unpredictable events, such as timings, hardware noise and network jitter, and stretched into many with a careful algorithm. When that gathering is weak, or skipped, every key looks random and is guessable, and nothing else in the system can tell.

## The story

In 2011 Leon Baptiste led the firmware team at a company that made small office routers. Each router needed its own private key, so that customers could manage it securely over the network. Rather than generate keys in the factory and keep a database of them, a list that would itself be a target, the team had each router generate its own key the first time it was switched on. Unique keys, made on the device, never seen by the factory. It was the textbook recommendation, and Leon was pleased with it.

In 2012 a group of university researchers scanned the entire internet, collected millions of public keys from devices like routers, and looked for keys that shouldn't have anything in common. Leon's company was on their list. Thousands of its routers had exactly the same key as other routers. Thousands more had keys that shared one of their two secret prime numbers with another router's, which let the researchers work out both private keys with a single quick calculation.

Leon took a router out of its box and watched it boot. It had no disk, no keyboard, no mouse, and no network traffic yet. Every unit ran identical firmware, started in an identical state, and reached the key-generation step after almost exactly the same number of clock ticks. The operating system's random-number source had had almost nothing unpredictable to draw on. It didn't refuse; it returned numbers that looked random. But on a thousand identical routers, booted the same way, they were the same numbers, or close enough to share a prime.

*Before reading on: generating keys on each device was the right idea, and thousands of devices made the same key. What would you have changed?*

The team made three changes. First, each router was given a unique random seed in the factory, from a proper hardware source, written into its storage and mixed with whatever the device gathered itself. Factory and device each contributed, and neither alone determined the key. Second, the newer hardware model got a dedicated random-number generator on its chip, which produced genuinely unpredictable bits from electronic noise. Third, and most important, key generation stopped happening at the first moment of the first boot. The firmware now waited until the operating system reported that its random source had been properly seeded, which on older routers meant some minutes of network traffic and timing measurements, and only then made the key. A software update regenerated the keys on routers already sold, and the company published the affected models.

Leon also found a smaller bug of the same kind in the router's web interface. Password-reset codes were made with the programming language's ordinary random function, which was designed for simulations and games, not secrets, and whose next value could be predicted from a few earlier ones. It was switched to the operating system's cryptographic random source.

Looking back, Leon thought randomness was the one ingredient nobody could check by looking at it. A bad key looked exactly like a good one. The only way to know was to know where the randomness came from, and whether there had been enough of it at the moment it was used.

## Where it shows up

| Page | The random value | What went wrong, or right |
| --- | --- | --- |
| [TLS](../auth/tls.md) | Netscape's session keys in 1995 | Seeded from the time and process numbers, so an attacker could guess them. |
| [Symmetric encryption](symmetric-encryption.md) | Seun's per-value nonces | Fresh randomness was what made identical drugs encrypt differently. |
| [Public-key cryptography](public-key.md) | Every key pair | Generated from random numbers; if someone else can reproduce them, they have your key. |
| [Sessions and tokens](../auth/sessions-and-tokens.md) | Ana Lucía's random session IDs | Unguessable, which is the whole point; generated with a predictable function, they wouldn't be. |
| [Communication with adversaries](../info/secrecy.md) | Lionel's key list, and the Soviet one-time pads | A key used twice stops being random to anyone who sees both uses. |
| [Hashing](../dsa/hashing.md) | The random secret mixed into hash tables since 2011 | Randomness used defensively, so strangers can't choose colliding keys. |

It shows up elsewhere too: salts, password-reset links, API keys, lottery and gaming systems, cryptocurrency wallets, and the shuffling in every online card game.

What these share is that randomness is invisible. A predictable value and a truly random one look the same; the difference is only in where they came from, how much unpredictability went in, and whether any of it was ever used twice.

## It really happened

Leon is fictional; the researchers' scan is real. In 2012 Nadia Heninger, Zakir Durumeric, Eric Wustrow and J. Alex Halderman collected keys from across the internet and recovered the private RSA keys of about 0.5% of TLS hosts, mostly routers, firewalls and other embedded devices that had generated keys at first boot with too little randomness ([Mining Your Ps and Qs](https://factorable.net/paper.html)). The same year, a separate team led by Arjen Lenstra reached similar findings.

In 2006 a Debian developer removed two lines from OpenSSL's random-number code to silence warnings from a memory-checking tool. One of them was what mixed unpredictable data into the generator. For almost two years, keys made with Debian's OpenSSL depended only on the process ID, so there were about 32,767 possible keys of each type and size. Every one could be generated in advance. It was disclosed in May 2008, and affected keys had to be replaced worldwide ([Debian wiki](https://wiki.debian.org/SSLkeys)). In 2010 the group fail0verflow showed that Sony had signed PlayStation 3 software using the same supposedly random value in every signature, which let them calculate Sony's private signing key with simple algebra. And Netscape's 1995 seeding mistake, found by Ian Goldberg and David Wagner, is on the [TLS](../auth/tls.md) page.

## What it is

Cryptographic randomness comes from a cryptographically secure pseudorandom number generator, or CSPRNG, seeded with enough entropy: unpredictable input from hardware noise, timing variations and similar sources. Once properly seeded, it can produce effectively unlimited unpredictable output. Operating systems provide one, and it's the right source for keys, nonces, salts and tokens. General-purpose random functions in programming languages are predictable and must never be used for secrets. The dangerous moments are early boot, cloned virtual machines and identical devices, when little entropy exists yet; good systems wait until the generator is seeded rather than proceeding with whatever they have.

## Where it gets misapplied

- **The language's ordinary random function for secrets.** Fine for games and simulations; predictable to an attacker.
- **Generating keys before there's any entropy.** Leon's first boot, and every cloned virtual machine that starts from the same snapshot.
- **"Fixing" randomness code you don't understand.** Debian's two lines.
- **Reusing a nonce.** Sony's signatures, and the Soviet pads: once is a secret, twice is a leak.
- **The mirror:** building your own random generator because the system one "might not be random enough". Use the operating system's; it's been studied far more than yours will be.

## Connections

- Learning this is also learning [key management](key-management.md), because a key's life begins at generation, and a badly generated key can't be rescued later.
- Learning this is also learning [information](../info/information.md), because entropy, the measure of unpredictability, is exactly what a random source must supply.
- Learning this is also learning [observation](../info/observation.md), because a random value can't be checked by looking at it; you can only know where it came from.
- Learning this is also learning [VM provisioning](../cloud/vm-provisioning.md), because machines started from identical images begin with identical state, including their random generators.
- Learning this is also learning [computability](../dsa/computability.md), because no test can prove a sequence is random; it can only fail to find a pattern.

## Resources

1. Heninger et al., ["Mining Your Ps and Qs: Detection of Widespread Weak Keys in Network Devices"](https://factorable.net/paper.html) (2012) (start here: readable, and alarming).
2. Jean-Philippe Aumasson, *Serious Cryptography*, the chapter on randomness (go deeper).
3. Your operating system's documentation for its cryptographic random source, such as `getrandom` on Linux (reference).

## Names you'll hear

- **Entropy:** unpredictability, measured in bits; what a random source must gather.
- **CSPRNG:** a cryptographically secure pseudorandom number generator.
- **Seed:** the starting input to a generator; predictable seed, predictable output.
- **TRNG, hardware RNG:** a generator that draws on physical noise.
- **Nonce:** a number used once.
- **`/dev/urandom`, `getrandom`:** the usual ways to ask an operating system for cryptographic randomness.

## Go and look

Find where something you build makes a token, key or reset code, and trace which random function it calls. If it's the language's general-purpose one, you've found a bug.
