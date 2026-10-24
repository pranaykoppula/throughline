# 0. Humans need representations before they need machines

Last reviewed: 2026-10-24

## Problem

Nobody works on the world directly. We write it down first, as numbers, symbols, rules, and work on what we wrote. Every way of writing it down works for the problems its inventors had, and quietly fails on some problem they didn't.

## The story

**Debts.** For a long time, numbers were for counting things you could hold: sheep, jars, coins. Then people needed to write down things they *owed*. Chinese officials doing accounts with counting rods, around two thousand years ago, used red rods for amounts gained and black rods for amounts owed. In seventh-century India, Brahmagupta wrote out rules for working with "fortunes" and "debts", including what happens when you subtract a debt. Europe resisted for another thousand years. Michael Stifel, writing in 1544, called numbers below zero *absurd*. People kept using them anyway, because the accounts didn't balance without them.

**The diagonal.** The Pythagoreans believed every length could be written as a ratio of whole numbers. Then someone noticed that the diagonal of a square with side one can't be. No fraction squared makes exactly two. Legend says the man who revealed this, Hippasus, was drowned for it. That part is almost certainly a story people told later, but it shows how much the belief mattered. The numbers had an edge, and the people who relied on them didn't want to find it.

**The impossible step.** In the 1500s, Italian mathematicians found a formula for solving cubic equations. Sometimes, on the way to a perfectly ordinary answer, the formula asked for the square root of a negative number, which was obviously impossible. Rafael Bombelli, in 1572, decided to carry these impossible quantities through the working anyway, just to see what happened. They cancelled out and left the right answer. Descartes later called them *imaginary*, and he didn't mean it kindly. The name stuck. So did the numbers: electrical engineers use them every day.

**Ten fingers, two states.** ENIAC, one of the first general-purpose electronic computers, finished in 1945, did its arithmetic in decimal, because that's how people counted. Its builders had to make circuits that could hold ten distinct states reliably, and it was hard. The same year, a report on its successor, EDVAC, argued for binary instead. Circuits that only need to tell *on* from *off* are simpler, cheaper, and far more reliable. A few years earlier, Claude Shannon's master's thesis had shown that switching circuits could carry out Boolean logic. Binary won inside machines. Humans kept decimal. Every computer since has translated between the two.

**Where binary ran out.** The translation has an edge. You can't write one third exactly in decimal: 0.333… goes on forever. In the same way, you can't write one tenth exactly in binary. In 1982 the Vancouver Stock Exchange launched an index at 1000. It was recalculated after every trade, and each time the result was cut off at three decimal places instead of rounded. The losses were tiny each time, and there were thousands of trades a day. Twenty-two months later the index stood at about 520, when the correct value was about 1098. In 1991, a Patriot missile battery at Dhahran had been running for more than 100 hours. It counted time in tenths of a second in binary, and a tenth can't be stored exactly, so its clock drifted further from the truth the longer it ran. It failed to intercept an incoming Scud missile, which hit a barracks and killed 28 American soldiers. A software fix was already on its way. It arrived the next day.

**The edge of logic itself.** In the early 1900s, David Hilbert hoped mathematics could be put on a complete foundation: a set of rules from which every true statement could be proved. In 1931 Kurt Gödel showed that this can't be done. Any consistent system of rules powerful enough to do arithmetic contains true statements it can't prove. Five years later Alan Turing hit a related wall from the side of computation: no program can decide, for every program, whether it will ever finish. Even the most careful representation humans had ever built had an edge.

**Still happening.** Qubits are the newest representation. They don't replace bits, but for a narrow class of problems they can hold something bits can't. Their edge is being explored right now.

Every time, the pattern was the same. A way of writing things down worked well, so people trusted it. Then a new problem came along that it couldn't express. People called the fix absurd or imaginary, then used it, and eventually forgot it had ever been controversial.

## What survived

Every representation is a choice among others that could have been made, and every one has an edge where it stops being true. This wiki hands out representations the way every textbook does, cleanly, as if they had no edges: bits, request and response, tables, consistency models. Each one stops being true somewhere. The pages don't stop to point that out every time. Finding the edge is your job.

## Names you'll hear

- **Gödel's incompleteness theorems:** any consistent system rich enough for arithmetic has true statements it can't prove, and can't prove its own consistency.
- **The halting problem** (Turing): no program can decide whether every program halts. It comes back on [page 3](03-programs-too-big-for-one-head.md) as Turing-completeness.
- **Floating point:** the standard way computers approximate real numbers in binary, and where most programmers first meet an edge.

## Connections

- Learning this is also learning every later page, because each one hands you a representation that has an edge somewhere.
- Learning this is also learning [floating point](math/floating-point.md), because the Vancouver index and the Patriot clock are the edge most programmers meet first, usually as `0.1 + 0.2` not equalling `0.3`.
- Learning this is also learning [number systems](math/number-systems.md), because most of the edges above were found by mathematicians first and by engineers later, at much greater cost.
- Learning this is also learning [computability](dsa/computability.md), because the halting problem is why no tool can check every program for you, and why Turing-completeness comes up on [page 3](03-programs-too-big-for-one-head.md).
- Learning this is also learning [machine learning](12-machines-that-learn-from-data.md), because there the representation is learned from data, and the data itself moves.

## Resources

1. Charles Petzold, *Code: The Hidden Language of Computer Hardware and Software* (start here: from flashlights to binary to a working computer).
2. Paul Nahin, *An Imaginary Tale: The Story of √−1* (go deeper: the impossible step, in full).
3. David Goldberg, ["What Every Computer Scientist Should Know About Floating-Point Arithmetic"](https://docs.oracle.com/cd/E19957-01/816-2464/ncg_goldberg.html) (1991; reference, and heavy going).
4. US General Accounting Office, ["Patriot Missile Defense: Software Problem Led to System Failure at Dhahran, Saudi Arabia"](https://www.gao.gov/products/imtec-92-26) (1992): the primary source, and short.

## The model so far

New on this page: sentence 0, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. **Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.**
