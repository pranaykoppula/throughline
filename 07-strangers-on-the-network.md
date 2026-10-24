# 7. Strangers on the network

Last reviewed: 2026-10-24

## Problem

Early networks connected people who knew each other, so systems trusted whoever was on the other end. Once anyone in the world could reach a system, some of them would try to break it, and every part of it had to be built for someone who means harm.

## The story

Marcus Bell built the website for a model-railway shop in Leicester in 2001. It sold kits and track, and it had a forum where customers swapped layout photos and argued about gauges. About three thousand people had accounts. Marcus knew some of them by name.

He stored their passwords in the database as they'd typed them. It seemed sensible: when someone forgot theirs, which happened every day, the site could simply email it back to them. Nobody could see the database except Marcus and the server. He'd never really thought of it as something to protect.

In 2003 a customer emailed him a link to a post on a forum Marcus had never heard of. It was a list of his shop's customers: names, email addresses, and passwords, all three thousand. Underneath, someone had written thanks, and below that, someone else said they'd already got into a few email accounts. Marcus read it at his kitchen table at eleven at night and felt sick.

It took him a day to work out how it had happened. The forum had a search box. His code took whatever was typed into it and pasted it straight into a database query. A stranger had typed not a search term but a fragment of database language, and the database had run it, and the query had returned the entire users table. Marcus had written the code to handle what his customers might type. He'd never imagined someone typing to attack it.

He fixed the hole that night. He rewrote every query so that what users typed was always passed to the database as data, never as part of the command. It was a simple rule once he saw it: anything that came from outside was not to be trusted to mean what it appeared to mean. The worse part was the emails he had to send. Many of his customers had used the same password for their email, and for their bank. The shop hadn't lost any money. Its customers had, and they'd never chosen to trust Marcus with anything more than a model-railway forum.

*Before reading on: Marcus had closed this hole, but he knew there would be others, and one day the database might leak again. What could he have stored so that a leak wouldn't matter?*

He read everything he could find, and the answer was older than he expected. Don't store the password at all. Store a *hash* of it: the result of running it through a one-way function, easy to compute and practically impossible to reverse. When someone logs in, hash what they type and compare the two hashes. A thief who steals the table gets the hashes, not the passwords. The site could no longer email anyone their forgotten password, so Marcus built a reset link instead. A few customers complained. He thought that was a price worth paying, and he was right.

For five years he was proud of it. Then, in 2008, another hobby site leaked its database, and a security researcher wrote about how quickly the hashed passwords had been cracked. Hashing gave the same output for the same input, every time, so attackers didn't need to reverse anything. They hashed millions of likely passwords in advance, kept the results in enormous lookup tables, and simply looked up every stolen hash. Out of curiosity, Marcus counted the hashes in his own table that appeared more than once. More than four hundred customers had exactly the same hash. He tried the obvious guess. It was `password1`.

His decision hadn't been wrong. Hashing really did stop anyone *reading* passwords from a leak. It did nothing to stop someone *guessing* them, at scale, with a machine built for it. He fixed it in two parts. First, a *salt*: a random value stored alongside each user's hash and mixed into it. The same password now produced a different hash for every customer, and no lookup table built in advance would match. Second, a hash function designed to be slow. A tiny fraction of a second meant nothing to a customer logging in once. It made each of an attacker's billions of guesses cost real time. He couldn't rehash passwords he didn't have, so he upgraded each one the next time its owner logged in.

While he was in there, he noticed something else. The account the website used to talk to the database could read every table, change any row, and delete the whole lot. It only ever needed to read products and write orders and posts. He gave it exactly that and nothing more. If someone got in again, they'd find a much smaller room.

Looking back, Marcus thought that everything he'd learned came from one shift. He had built the site for people he knew. Once strangers could reach it, every place where something crossed from outside to inside was a question: who is asking, and what should they be allowed to do? Trust nothing that has crossed a boundary. Give every part of the system the least it needs to do its job. And remember who actually gets hurt. When his database leaked, the harm fell on his customers, not on him. Years later, when the law started making companies pay for losing people's data, Marcus understood exactly why.

## It really happened

Marcus is fictional; his mistakes were common, and very old. In 1979 Robert Morris and Ken Thompson described how Unix stored passwords. Their paper covered the same attack Marcus found, guessing at scale, and the same defences: a salt, and a deliberately slow hash ([Morris and Thompson, "Password Security: A Case History"](https://www.profsandhu.com/cs6393_s20/p594-morris.pdf)). Nine years later Robert Morris's son, Robert Tappan Morris, released the Morris worm, which spread across the Internet partly by exploiting the trust machines extended to each other and partly by guessing weak passwords. It was a network built for colleagues meeting strangers for the first time.

In 2012 about 6.5 million LinkedIn password hashes were posted online. They were unsalted, and hundreds of thousands were cracked quickly; in 2016 a much larger set from the same breach turned up for sale ([TechCrunch, 2016](https://techcrunch.com/2016/05/18/117-million-linkedin-emails-and-passwords-from-a-2012-hack-just-got-posted-online/)). LinkedIn said it had since salted every password. Thirty-three years after the paper, one of the largest sites on the web had made Marcus's 2003 mistake.

Trust also extends to the code you didn't write. In 2014 Heartbleed, a bug in OpenSSL, let anyone read chunks of memory from servers across much of the web. OpenSSL secured a large share of the Internet, and its foundation was reported to receive about $2,000 a year in donations. Large tech companies then funded developers to work on it ([PCWorld](https://www.pcworld.com/article/439499/tech-giants-throw-money-at-openssl-in-response-to-heartbleed.html)). Everyone had trusted it; almost nobody had paid for it ([forces: who pays](forces.md#who-pays-vs-who-benefits)).

## What survived

Once strangers can reach a system, every boundary is a question of who is asking and what they may do. Trust nothing that crossed a boundary: treat input as data, never as instructions. Give every party, person or program, the least it needs. Store secrets so that a leak reveals as little as possible, and assume the leak will happen. Harms from data fall on people other than those who collect it, so the law steps in where incentives don't.

## Where it gets misapplied

- **Security theatre.** Rules that look strict and stop nothing, such as forced monthly password changes, while the real boundary goes unchecked.
- **Rolling your own crypto.** Marcus's first hash was at least a standard one. Inventing your own scheme is how a small mistake becomes a total one. Use well-reviewed libraries, and keep them updated.
- **A checklist instead of a threat model.** Ask who would attack this, what they'd want, and how they'd get in, before deciding what to defend.
- **The mirror:** treating every control as friction and shipping without any. "We're too small to be a target" is what Marcus thought in 2001. Strangers' tools don't check how small you are.

## Connections

- Learning this is also learning [sessions and tokens](auth/sessions-and-tokens.md), because once a password is checked, something has to prove who you are on every later request, and that something can be stolen too.
- Learning this is also learning [networking](05-machines-need-to-talk.md), because tokens and passwords travel, and every hop is a place they can leak.
- Learning this is also learning [AI](12-machines-that-learn-from-data.md), because prompt injection is Marcus's search box again: input from outside being treated as instructions.
- Learning this is also learning [software supply chain](vendors/supply-chain.md), because every library you install is code from strangers you've decided to trust.
- Learning this is also learning [the web](06-anyone-can-publish.md), because the client is a stranger's machine, and anything it sends can be forged.

## Resources

1. [OWASP Top Ten](https://owasp.org/www-project-top-ten/) (start here: the common ways web applications get broken, kept up to date). <!-- verify -->
2. [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) (what to actually do with passwords today). <!-- verify -->
3. Ross Anderson, [*Security Engineering*](https://www.cl.cam.ac.uk/~rja14/book.html) (go deeper: free online, and about thinking like an attacker). <!-- verify -->
4. Morris and Thompson, ["Password Security: A Case History"](https://www.profsandhu.com/cs6393_s20/p594-morris.pdf) (1979; four pages, and still right).

## Names you'll hear

- **SQL injection:** Marcus's search box. Input treated as part of a command.
- **Hash, salt, bcrypt:** one-way functions, the random value that makes each one unique, and a slow hash designed for passwords (1999).
- **Diffie–Hellman, RSA:** the 1970s ideas that let strangers agree on a secret over a public network, and sign things.
- **Least privilege:** give everything only the access it needs.
- **Zero trust:** don't trust a request because it comes from inside your own network.
- **Byzantine fault:** a part of a system that doesn't just fail but lies. Named after a puzzle about generals who can't trust each other's messages.

## Go and look

Find where a permission or role is decided in something you've built, and check whether it's worked out on the server or accepted from the client. That's a trust boundary.

## The model so far

New on this page: sentence 7, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

4. Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises.

5. Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so systems retry and tolerate repeats. Once data moves cheaply, distribution is free, and value shifts from copies to services, relationships, and trust.

6. Client and server split the work: the server owns the truth, the client owns presentation and a copy of state. Most interface bugs are two sources of truth disagreeing. The browser won because shipping one server beats shipping a million installs; native shells survive where platforms control distribution.

7. **Once strangers can reach a system, every boundary is a question of who is asking and what they may do. Trust nothing that crossed a boundary; give every party the least it needs. Harms from data fall on people other than those who collect it, so law steps in where incentives don't.**
