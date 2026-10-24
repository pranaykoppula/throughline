# Floating point

Last reviewed: 2026-10-24

A concept page: how computers approximate real numbers in binary, and where the approximation shows.

## Problem

Computers store most fractional numbers as binary floating point: a fixed number of binary digits and an exponent saying where the point goes. It handles huge and tiny numbers well. But most decimal fractions, like 0.1, have no exact binary form, so every such number is slightly off. Usually nobody notices. Over millions of operations, or in money, or in comparisons, everyone eventually does.

## The story

In 2011 Oskar Lindgren built the interest engine for a small online savings bank. Every night it calculated each account's daily interest and added it to the balance. He used the language's ordinary number type, a 64-bit floating-point number, accurate to about sixteen significant digits. Sixteen digits seemed far more than enough for amounts in kronor and öre.

Six months in, the finance team's monthly reconciliation failed. The total of all account balances didn't match the bank's ledger. The difference was small, a few hundred kronor across two hundred thousand accounts, but a bank's books have to match to the öre. Oskar traced it. Each night's interest was a fraction like 0.000136986 of the balance, which floating point stored very slightly wrong. Adding it each night compounded the tiny errors, and some accounts had been rounded to the öre on display but not in storage, so displayed and stored values had drifted apart. Each error was a billionth of a krona. There were two hundred thousand accounts and a hundred and eighty nights.

*Before reading on: the numbers were accurate to sixteen digits, and the books still didn't balance. What would you have stored instead?*

Oskar stopped using floating point for money entirely. Balances became whole numbers of öre, stored as integers, which are exact. Interest was calculated with a decimal arithmetic library, which stores numbers in base ten so that 0.1 really is 0.1. It was then rounded to whole öre once, at a defined point each night, using the rounding rule the bank's accountants specified, not whatever the computer did by default. The rounding remainder was recorded rather than lost. The reconciliation matched the next month, and every month after.

He kept floating point for what it was good at. The bank's risk models, which estimated probabilities and ran simulations, used it happily, because there a billionth of a krona meant nothing and speed mattered.

Looking back, Oskar thought floating point had never been wrong. It did exactly what it promised: a very good approximation, very fast. Money needed something else, exactness and agreed rounding, and he'd used the default without asking which one he needed.

## Where it shows up

| Page | The numbers | What went wrong, or right |
| --- | --- | --- |
| [0, Representations](../00-representations.md) | The Vancouver index and the Patriot clock | Tiny errors in representing tenths, accumulated until they mattered enormously. |
| [JavaScript](../runtimes/javascript.md) | Every number in the language | `0.1 + 0.2` is `0.30000000000000004`, and Zara's prices came out as `59.99000000000001`. |
| [Number systems](number-systems.md) | Fixed-width numbers | Floating point is one choice of how to spend a fixed number of bits. |
| [Computability](../dsa/computability.md) | Representations with edges | Every way of writing numbers down stops being exact somewhere. |

It shows up elsewhere too: graphics, physics simulations, machine learning, where it's the right tool, and accounting, billing and comparisons for equality, where it usually isn't.

What these share is page 0's lesson in its most common form: a representation that's excellent for one job and quietly wrong for another.

## It really happened

Oskar is fictional; the standard he relied on is IEEE 754, first published in 1985, largely the work of William Kahan, who won the Turing Award for it. It made floating point behave the same way on every machine, which was a great achievement. Its edges still surprise people. In 2007 Microsoft Excel 2007 displayed the result of `850*77.1` as 100,000 instead of 65,535; the calculation was right, but a bug in converting the floating-point result to text for display showed the wrong number, and Microsoft issued a fix. Banks and accounting systems have long used decimal or integer representations for money for exactly Oskar's reasons.

## What it is

Floating-point numbers store a sign, a fixed number of significant binary digits and an exponent. 64-bit "double" values give about 15 to 17 significant decimal digits over an enormous range. Most decimal fractions can't be represented exactly, so results are rounded at each step, errors can accumulate, and two values that should be equal often aren't exactly. Use floating point for measurement and computation where approximation is acceptable. Use integers of the smallest unit, or decimal types with explicit rounding, for money and anything that must add up exactly.

## Where it gets misapplied

- **Money in floating point.** Oskar's first design.
- **Comparing floats for exact equality.** Compare within a tolerance, or don't compare at all.
- **Rounding only for display.** The stored value and the shown value drift apart.
- **The mirror:** using slow decimal arithmetic for a physics simulation or a machine-learning model, where floating point is exactly right.

## Connections

- Learning this is also learning [number systems](number-systems.md), because floating point is one way to spend a fixed number of bits.
- Learning this is also learning [JavaScript](../runtimes/javascript.md), because every number in it is a float.
- Learning this is also learning [statistical significance](statistics.md), because numerical error is one more source of noise in results.
- Learning this is also learning [data modelling](../data/modelling.md), because choosing the type of each field, including money, is a modelling decision.
- Learning this is also learning [computability](../dsa/computability.md), because representations having edges is the theme of page 0.

## Resources

1. [floating-point-gui.de](https://floating-point-gui.de/) (start here: "What every programmer should know about floating-point arithmetic", short). <!-- verify -->
2. David Goldberg, ["What Every Computer Scientist Should Know About Floating-Point Arithmetic"](https://docs.oracle.com/cd/E19957-01/816-2464/ncg_goldberg.html) (1991) (go deeper).
3. Your language's decimal type documentation (reference: what to use for money).

## Names you'll hear

- **IEEE 754:** the floating-point standard nearly every machine uses.
- **Single, double precision:** 32-bit and 64-bit floating point.
- **Rounding error, epsilon:** the small error in each operation, and the gap between adjacent representable numbers.
- **Decimal type:** numbers stored in base ten, exact for decimal fractions.
- **Banker's rounding:** rounding halves to the nearest even digit, to avoid systematic bias.
- **NaN:** "not a number", the result of undefined operations, which isn't even equal to itself.

## Go and look

Find one place in code you know where money or another exact quantity is stored, and check its type. If it's a float, find out where and how it's rounded.
