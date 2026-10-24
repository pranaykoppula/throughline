# Password storage

Last reviewed: 2026-10-24

A concept page: storing something you can check but never read, and keeping it that way as attackers get faster.

## Problem

A system needs to check passwords without being able to reveal them if its database leaks. That means storing a slow, salted one-way hash, never the password itself. But hashing standards age: what was strong ten years ago is weak now, and you can't simply re-hash passwords you don't have.

## The story

In 2013 Elif Yilmaz joined a company that ran an online game with eleven million accounts, many of them created years earlier. On her second day she looked at how passwords were stored. They were hashed, but with a fast, unsalted function from the early 2000s. She knew that a leaked copy of that table could be cracked, most of it in days, on a few gaming graphics cards.

The fix seemed clear. Use a modern password hash: slow on purpose, salted per user. The catch was that she couldn't compute the new hash without the password, and the company didn't have the passwords. Only their old hashes. So she did what most teams did. Each time a user logged in, the server checked the password against the old hash; if it matched, it computed the new hash from the password the user had just typed, stored that, and deleted the old one. Within a month, most active players were upgraded. It was a clean, standard approach, and she moved on to other work.

Two years later the company was breached, and the attacker copied the user table. Elif checked it with a sinking feeling. Active players were safe, on the new hash. But more than six million accounts belonged to people who hadn't logged in since before the upgrade, and their passwords were still under the old fast hash. Many of those people had used the same password for their email. Their accounts had been dormant in the game. Their passwords weren't dormant anywhere else.

*Before reading on: the upgrade waited for each user to log in, and most never did. How could Elif have protected everyone at once, without their passwords?*

The answer, which she wished she'd seen in 2013, was to wrap the old hashes rather than wait to replace them. On the first day, she could have run the modern slow hash over every existing old hash, storing the result and throwing the old hash away. Checking a password would mean computing the old fast hash of what the user typed, then the slow hash of that. Every account, active or not, would have been behind the slow hash immediately. Users who logged in could still be moved to a clean new hash later. She did exactly that after the breach, for the accounts that remained, and wrote it into the company's security guide so the next upgrade wouldn't wait for anyone.

Looking back, Elif thought she'd solved the problem for the people she could see, the active players, and left it unsolved for the people she couldn't. A leak doesn't care whether an account is active.

## Where it shows up

| Page | The passwords | What protected them |
| --- | --- | --- |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | Marcus's customers, first in plain text, then hashed, then salted and slowed | Each step fixed one attack: reading, then looking up, then guessing at scale. |
| [Hashing](../dsa/hashing.md) | The secrecy job | It needs a hash that's hard to reverse and slow to compute, the opposite of what lookup needs. |
| [Sessions and tokens](sessions-and-tokens.md) | What stands in for the password after login | Once the password is checked, the token needs the same care. |
| [Migrations](../data/migrations.md) | Moving data to a new format without stopping | Elif's upgrade was a migration, and her first version only migrated the rows that happened to be touched. |

It shows up elsewhere too: API keys, password reset tokens, and recovery codes, which all need the same one-way treatment.

What these share is that a stored secret should be useless to whoever steals it, and that "useless" has to be kept up to date as attackers' hardware improves.

## It really happened

Elif is fictional; layering hashes is how careful teams handle it. In 2016 Dropbox described its approach: each password is first hashed with SHA-512, then with bcrypt using a per-user salt, and the result is encrypted with a key stored separately from the database, so a stolen table alone isn't enough ([Dropbox, "How Dropbox securely stores your passwords"](https://dropbox.tech/security/how-dropbox-securely-stores-your-passwords)). The failure Elif feared is on [page 7](../07-strangers-on-the-network.md): LinkedIn's unsalted hashes, posted in 2012, with hundreds of thousands cracked quickly and a far larger set from the same breach surfacing in 2016.

## What it is

Passwords should be stored using a dedicated password-hashing function, such as bcrypt, scrypt or Argon2. These are slow on purpose, with a tunable cost, and use a unique random salt per user. Optionally, the result is encrypted with a secret kept outside the database, called a pepper. The cost should be raised as hardware gets faster. Upgrading an old scheme is done by wrapping old hashes in the new function immediately, not by waiting for users to log in.

## Where it gets misapplied

- **Upgrading only on login.** Elif's first approach: dormant accounts stay weak indefinitely.
- **A fast hash, even salted.** Salting stops lookup tables; only slowness stops guessing at scale.
- **Never raising the cost.** A cost chosen in 2012 is cheap for 2026 hardware.
- **The mirror:** inventing your own scheme. Use a well-reviewed password-hashing library, or avoid storing passwords at all with passkeys or a trusted identity provider.

## Connections

- Learning this is also learning [hashing](../dsa/hashing.md), because password storage is the secrecy job, which needs a different kind of hash from lookup.
- Learning this is also learning [sessions and tokens](sessions-and-tokens.md), because the password is checked once and the token carries the trust from then on.
- Learning this is also learning [migrations](../data/migrations.md), because upgrading a hashing scheme is a migration that must cover every row.
- Learning this is also learning [least privilege](least-privilege.md), because keeping the pepper away from the database means one stolen system isn't enough.
- Learning this is also learning [TLS](tls.md), because the password has to arrive safely before it can be stored safely.

## Resources

1. [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) (start here: current recommendations). <!-- verify -->
2. Dropbox, ["How Dropbox securely stores your passwords"](https://dropbox.tech/security/how-dropbox-securely-stores-your-passwords) (2016) (go deeper: layering, explained).
3. Morris and Thompson, ["Password Security: A Case History"](https://www.profsandhu.com/cs6393_s20/p594-morris.pdf) (1979) (reference: salt and slowness, forty-five years ago).

## Names you'll hear

- **bcrypt, scrypt, Argon2:** password-hashing functions, slow on purpose.
- **Salt:** a random value per user, mixed into the hash.
- **Pepper:** a secret key applied to all hashes, kept outside the database.
- **Work factor, cost:** how slow the hash is, tunable over time.
- **Credential stuffing:** trying leaked passwords on other sites, which is why one leak harms people elsewhere.
- **Passkeys:** a newer way to log in without a password, using a key held on the user's device.

## Go and look

Find out how a system you work on stores passwords: which function, what cost, and when that was last reviewed. Then check whether any accounts are still on an older scheme.
