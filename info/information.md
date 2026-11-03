# Information

Last reviewed: 2026-11-03

A concept page, and the first of the information family: what a message actually carries, why packing it tighter makes it fragile, and why it only means anything to someone who shares the codebook.

## Problem

Sending words costs something: money, time, bandwidth, attention. So people squeeze messages, saying more with less. But a message carries information only by ruling out possibilities, and only to a receiver who already knows what the possibilities were. Squeeze too hard and there's nothing left to catch a mistake. Assume too much shared knowledge and the receiver decodes something else entirely.

## The story

In 1886 Thomas Hale was the code clerk for a grain merchant in Chicago. The firm's buyers travelled the farming towns of Kansas and Nebraska and reported by telegraph, and the telegraph companies charged by the word. A routine report, *I have bought ten thousand bushels of wheat at eighty-two cents; awaiting your instructions on the remainder*, cost as much as a clerk earned in a day. The firm sent dozens a week.

Like most merchants, the firm used a commercial codebook, in which a single invented word stood for a whole sentence. Thomas went further. He compiled a private code for the firm's own trade, and made the words as short as he could: three or four letters for the most common messages, a word for each price, a word for each quantity. *BAY* meant "I have bought". *BUY* meant "buy as much as you can at the price named". A day's reports shrank to a line. The telegraph bill fell by more than two thirds, and the partners gave Thomas a raise. He'd squeezed every unnecessary letter out of the firm's messages, and he was proud of it.

In the autumn a buyer in a Kansas town sent *BAY*, meaning he had bought a modest lot and was waiting. Somewhere between the towns on the line, one operator sent or heard one extra dot, and the A became a U. The firm's agent at the other end received *BUY*, a perfectly valid word in Thomas's code, and did exactly what it said. He bought, as much as he could, for two days, in a falling market. By the time the error was found, the firm had lost more than it made in a good year. The telegraph company offered a refund of the message fee. It had offered, at extra cost, to repeat important messages back for checking; the firm had always declined, to save money.

Thomas went over his codebook with a sick feeling. He'd made every short word mean something. So any slip in any letter didn't produce nonsense, which someone would have queried. It produced a different, sensible instruction, which someone obeyed.

*Before reading on: Thomas's code was efficient precisely because every word was meaningful. How would you change it so that a garbled word gets noticed instead of obeyed?*

He rebuilt the code with a rule he found in the better commercial codebooks: any two code words had to differ in at least two letters. A single garbled letter could then never turn one valid word into another. It produced a word that wasn't in the book at all, and the clerk receiving it would know at once to ask. The words got longer and the bills went up by about a fifth. Quantities and prices, where a mistake was most expensive, were sent twice, in two different forms, and for any order above a certain size the firm paid to have the message repeated back. Over the next ten years the firm's telegraph errors didn't stop. But they were all caught before anyone acted on them.

There was a second lesson, which took longer to sink in. A new agent in Omaha received a message that used a code word from an old edition of the codebook, which he'd never been given. He decoded it from his own edition, where the same word meant something else, and acted on it in good faith. The word had arrived perfectly. It had simply been decoded against a different book. A code word carried meaning only for someone holding the same book as the sender.

Looking back, Thomas thought he'd learned what a message really was. It wasn't the letters. It was the difference between what the receiver knew before and after: which of all the possible messages this one was. Squeezing out redundancy made messages cheap and left nothing to catch an error, so some of it had to be put back on purpose. And none of it worked unless both ends were reading from the same book.

## Where it shows up

| Page | The message | What it taught |
| --- | --- | --- |
| [0, Representations](../00-representations.md) | Every way of writing things down | A representation is a codebook; it only means something to those who share it, and it has edges. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Lin's numbered blocks and confirmations | Numbering and acknowledgement are redundancy added so errors and duplicates can be noticed. |
| [Serialization formats](../data/serialization.md) | The Mars Climate Orbiter's thruster data | The bytes arrived perfectly; the two sides decoded the units against different books. |
| [Hashing](../dsa/hashing.md) | A short fingerprint of a long input | Squeezing any input into a fixed size must lose information, which is why collisions exist. |
| [Tokens and context windows](../ai/tokens.md) | What a language model is given | The model only knows what's in its context; everything else is a codebook it doesn't hold. |

It shows up elsewhere too: in abbreviations that mean different things to different teams, in error messages that assume the reader knows the system, and in every "as discussed" that assumes a discussion the reader wasn't part of.

What these share are the three ideas the rest of this family builds on. Information is the reduction of uncertainty: what a message rules out. Redundancy is what lets errors be noticed, and compression removes it, so the two pull against each other. And meaning depends on context the message doesn't carry, which is why a perfect transmission can still be misunderstood.

## It really happened

Thomas is fictional; his loss is the case of Frank Primrose, a Philadelphia wool dealer. In 1887 a telegram he sent his agent in Kansas, containing the code word *BAY*, arrived as *BUY*, apparently because of a single added dot. The agent bought several hundred thousand pounds of wool, and Primrose lost more than $20,000. The case reached the US Supreme Court in 1894, which held that Western Union owed him only the $1.15 he'd paid for the message, partly because he hadn't paid for it to be repeated back ([*Primrose v. Western Union*, 154 U.S. 1](https://supreme.justia.com/cases/federal/us/154/1/)). Later commercial codebooks adopted the rule that any two code words must differ in at least two letters, so a single garbled letter produced a word not in the book ([Steven Bellovin on commercial codebooks](https://www.cs.columbia.edu/~smb/talks/codebooks.pdf) <!-- verify -->).

The idea that frequent things should get short codes is older still. Morse code gives the most common English letter, E, a single dot. Alfred Vail is said to have worked out which letters were common by counting the type in a printer's cases; that story is widely repeated but hard to document. In 1948 Claude Shannon turned all of this into mathematics in "A Mathematical Theory of Communication". Information could be measured in bits, as the number of yes-or-no questions a message answers. A source's average information was its *entropy*. Ordinary English was highly redundant, which is why it can be compressed, and why it survives errors. And any channel with noise could still carry information reliably, if enough redundancy was added in the right way. Shannon deliberately left meaning out of his theory. The bits are the same whether or not the receiver understands them; understanding depends on the shared book.

## What it is

Information, in Shannon's sense, is the reduction of uncertainty: a message is informative to the extent that it rules out possibilities the receiver couldn't rule out before. It's measured in bits. Entropy is the average information per message from a source, and it is highest when every message is equally likely and unpredictable. Redundancy is the gap between a message's length and its information. Compression removes redundancy; error detection and correction add it back in a structured form. Meaning is outside the measure entirely: it depends on the receiver interpreting the message against the same assumptions, codebook or context as the sender.

## Where it gets misapplied

- **Squeezing out all redundancy where errors are costly.** Thomas's three-letter code: cheap, and every mistake looks valid.
- **Assuming shared context.** A message that's perfectly clear to the sender, decoded against a different book.
- **Measuring communication by volume.** Long reports and many messages can carry little information; one surprising number can carry a lot.
- **The mirror:** so much redundancy that the message is buried. A ten-page document with one important line has protected nothing.

## Connections

- Learning this is also learning [representations](../00-representations.md), because every representation is a codebook, agreed between those who use it.
- Learning this is also learning [serialization formats](../data/serialization.md), because a format is a codebook between programs, and the costliest failures are decoding against the wrong one.
- Learning this is also learning [hashing](../dsa/hashing.md), because a fixed-size fingerprint necessarily throws information away.
- Learning this is also learning [statistical significance](../math/statistics.md), because how surprising an observation is, given what you expected, is both a measure of information and the heart of a statistical test.
- Learning this is also learning [round trips](../latency/round-trips.md), because a reply confirming a message is redundancy bought with time.

## Resources

1. James Gleick, *The Information* (2011) (start here: telegraph codes, Morse, Shannon and much more, as a story).
2. Claude Shannon, "A Mathematical Theory of Communication" (1948) (go deeper: the first sections are readable, and the rest is where the field began).
3. Steven Bellovin, ["Compression, Correction, Confidentiality, and Comprehension: A Modern Look at Commercial Telegraph Codes"](https://www.cs.columbia.edu/~smb/papers/codebooks.pdf) (reference: the codebooks, their rules and their motives). <!-- verify -->

## Names you'll hear

- **Bit:** the information in one yes-or-no answer between two equally likely options; Shannon credited the word to John Tukey.
- **Entropy:** the average information per message from a source.
- **Redundancy:** what a message contains beyond its information, which can be removed to compress it or used to detect errors.
- **Channel, noise:** whatever carries the message, and whatever corrupts it on the way.
- **Codebook:** the shared agreement that turns symbols into meaning.

## Go and look

Find a message you sent this week that the receiver misunderstood. Work out whether the bits were garbled on the way, or decoded against a different book.
