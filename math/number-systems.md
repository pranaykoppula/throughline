# Number systems

Last reviewed: 2026-10-24

A concept page: how numbers are written down, in which base, and in how many digits, and what happens at the edge of the last digit.

## Problem

Computers store integers in a fixed number of binary digits, usually 8, 16, 32 or 64. Each width holds a fixed range of values. Programs that count things, such as users, seconds, views or IDs, eventually reach the top of that range, and what happens next depends on details almost nobody thinks about until it happens: the number wraps round to a large negative value, or to zero, or the program crashes.

## The story

In 2007 Priyanka Iyer built the database for a photo-sharing site. Each photo had an ID, a number counting up from one, stored as a 32-bit signed integer, the database's default integer type. It could count to just over 2.1 billion. The site had forty thousand photos. Two billion felt like a number from astronomy.

The site grew far faster than anyone expected. In early 2012 a monitoring alert Priyanka had set up years before, half as a joke, fired: photo IDs had passed two billion. She had about three months before new uploads would fail. She knew exactly what would happen, because she'd tested it on a copy. The next ID after 2,147,483,647 wouldn't fit; the database would refuse to insert the row, and every upload would fail at once.

The obvious fix was to widen the column to 64 bits, room for nine quintillion photos. It was also hard. The ID was in eleven tables, in the mobile apps, in URLs people had bookmarked, in the code of two partners, and in several places where it had been stored as a 32-bit number in memory. Some of that code would silently mangle a 64-bit ID rather than fail.

*Before reading on: the counter was about to overflow, and widening it touched everything that had ever stored it. How would you have done it, and what would you have done differently in 2007?*

Priyanka treated it as a migration. The new, wider column was added alongside the old one, written to by both, backfilled, verified, and switched over a table at a time. Every client was tested with IDs above the 32-bit limit before the limit was reached, and the mobile apps were updated and given a few weeks to spread. They crossed 2,147,483,647 on a Tuesday afternoon, and nothing happened.

What she'd do differently was simple: in 2007, she'd have chosen 64 bits for anything that counts up forever. It would have cost four extra bytes per row, a negligible price against months of work later.

Looking back, Priyanka thought every number in a program has a width, whether or not anyone chose it, and the edge of that width is a date in the future. You can either work out when you'll reach it, or be surprised.

## Where it shows up

| Page | The width | The edge |
| --- | --- | --- |
| [0, Representations](../00-representations.md) | Decimal against binary | Every way of writing numbers has an edge; this is the integer version. |
| [Floating point](floating-point.md) | A fixed number of bits for fractions | Precision runs out instead of range. |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | Two-digit years | Y2K: a width chosen to save space in 1979, reached in 2000. |
| [Hashing](../dsa/hashing.md) | A fixed-size output for any input | Collisions are certain eventually, because the space of values is finite. |

It shows up elsewhere too: counters, timestamps, IDs, file sizes, and memory addresses.

What these share is that a fixed number of digits is a promise about the largest thing you'll ever need to count, and someone eventually checks.

## It really happened

Priyanka is fictional; her deadline is common. In December 2014 YouTube said that the view count of "Gangnam Style" had passed the largest value a 32-bit signed integer can hold, and that it had already moved the counter to 64 bits. In 2015 the US aviation regulator required operators of the Boeing 787 to restart its electrical power system periodically, after it was found that a software counter could overflow after about 248 days of continuous power and shut down the generators. Many Unix systems store time as a 32-bit count of seconds since 1970, which overflows in January 2038, and is being migrated, slowly, to 64 bits.

## What it is

A number system is a way of writing numbers: a base, such as 2, 10 or 16, and in computers a fixed width. An unsigned n-bit integer holds 0 to 2ⁿ−1; a signed one, using the usual two's complement form, holds −2ⁿ⁻¹ to 2ⁿ⁻¹−1. A 32-bit signed integer tops out at 2,147,483,647. Going past the limit, overflow, wraps round, is rejected, or is undefined, depending on the language. Choose widths from the largest value you could ever need, and know what your language does at the edge.

## Where it gets misapplied

- **32-bit IDs for anything that grows forever.** Priyanka's 2007.
- **Ignoring overflow behaviour.** In some languages a counter silently wraps to a large negative number.
- **Narrowing across boundaries.** A 64-bit ID passed through code that stores 32 bits, or through a format that loses precision on large numbers.
- **The mirror:** 128-bit integers for a counter that will never pass a thousand. Size for the plausible future, not infinity.

## Connections

- Learning this is also learning [floating point](floating-point.md), because it's the other way to spend a fixed number of bits.
- Learning this is also learning [hashing](../dsa/hashing.md), because a hash is a fixed-width number, and that's why collisions exist.
- Learning this is also learning [migrations](../data/migrations.md), because widening a column everyone depends on is a migration.
- Learning this is also learning [serialization formats](../data/serialization.md), because a number's width has to survive every format it passes through.
- Learning this is also learning [data modelling](../data/modelling.md), because choosing each field's type is a modelling decision with a deadline.

## Resources

1. Charles Petzold, *Code*, the chapters on binary and hexadecimal (start here).
2. Randal Bryant and David O'Hallaron, *Computer Systems: A Programmer's Perspective*, chapter 2, "Representing and Manipulating Information" (go deeper).
3. Your language's documentation on integer overflow (reference).

## Names you'll hear

- **Bit, byte, word:** a binary digit, eight of them, and the machine's natural number size.
- **Binary, octal, hexadecimal:** bases 2, 8 and 16.
- **Signed, unsigned, two's complement:** whether negative numbers are allowed, and the usual way they're stored.
- **Overflow, wraparound:** exceeding the largest value, and what happens next.
- **Year 2038 problem:** 32-bit Unix time running out.

## Go and look

Find the ID column of the largest table in a system you work on. Check its width, how fast it's growing, and work out the date it runs out.
