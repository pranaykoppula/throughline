# Encodings

Last reviewed: 2026-11-04

A concept page in the information family: how anything is **represented** as bytes, and why bytes mean nothing on their own. Text, numbers, colours and dates only mean something under a convention, and the convention is usually not stored with the bytes.

## Problem

A computer stores numbers. To store a letter, someone has to agree which number stands for which letter; to store a price, which unit; to store a colour, which colour space. That agreement is an *encoding*. There have been hundreds, many incompatible, and a file rarely says which one it used. So the same bytes can be read correctly by one program and as nonsense by another, and the program reading them usually can't tell that anything is wrong. It just shows the wrong thing, confidently.

## The story

In 2001 Kasia Zielińska built the systems for an online bookshop in Warsaw. Every night, publishers sent files listing new books, prices and authors, and every day customers typed their names and addresses into the shop's forms. Her database, like most software of the time, came set up for Western European text, where each character took one byte. It handled English, French and German. She checked that Polish letters appeared correctly in a test, saw that they did, and moved on.

The complaints started in the first month. A customer named Łucja received a parcel addressed to "£ucja". The city of Łódź appeared on labels as "£ód¼". Then it got stranger. Books by one publisher had authors whose names were correct in the publisher's file and wrong in the shop. Another publisher's names were right in the shop and wrong in the emails it sent. Some names had been garbled twice, then saved, so the original letters were gone for good, and a few had been turned into question marks that could never be turned back.

Kasia sat down with the raw files and found that there was nothing wrong with any of the bytes. Polish text was being written in at least two different encodings: one publisher used the international standard for Central European text, and another used the one built into Windows. In both, a Polish letter was a single byte, but not the same byte. Her database read every byte as if it were Western European, where those same numbers stood for £, ¼ and other symbols. Her test had passed because she'd typed Polish into a form and read it back through the same mistaken convention both ways, so the error cancelled out. Every program in the chain was storing the bytes perfectly. Each one was simply reading them with a different codebook, and none of the bytes said which codebook was right.

*Before reading on: every byte was stored faithfully, and the names were still wrong. What would you have changed?*

Kasia decided the convention had to be settled at the edges and never guessed in the middle. Every file and form now declared its encoding, or had it agreed in writing with the supplier who sent it. At the moment data entered the shop, it was decoded using that declared encoding and converted into one internal encoding for everything: Unicode, stored as UTF-8, which gave every character in every language its own number. Inside the shop there was only ever one convention. Data was converted again only on the way out, to whatever each printer or email system required. A file that didn't decode cleanly was rejected and sent back, not loaded with a best guess, and the original file was kept so a mistake could be undone.

A second lesson followed. Customers searched for "Lodz" and found nothing, because "Łódź" was different text, and some systems wrote "ó" as one character and others as an "o" followed by an accent. Kasia had to decide what "the same" meant. Searches now compared names after converting them to a standard form, and also with accents removed, so "Lodz" found "Łódź" but the database still stored the name exactly as the customer wrote it.

Looking back, Kasia thought every file was a message in a language whose name wasn't written on it. The bytes arrived perfectly; meaning didn't travel with them. The only defence was to name the language at the border and then speak only one inside.

## Where it shows up

| Page | The bytes | The convention that wasn't written down |
| --- | --- | --- |
| [Serialization formats](../data/serialization.md) | The Mars Climate Orbiter's thruster data | Units: pound-force seconds on one side, newton-seconds on the other. |
| [Designed for human senses](../signals/perception.md) | Zainab's photo pixels | The colour profile, which her pipeline threw away, so the same numbers became duller colours. |
| [Information](information.md) | Thomas's private telegraph code | The codebook: a code word meant nothing to anyone who didn't hold it. |
| [0, Representations](../00-representations.md) | Numbers written in decimal or binary | The base: the same quantity under different conventions. |
| [Floating-point](../math/floating-point.md) | Bits that represent a real number | The format decides which numbers exist at all, and how the rest are rounded. |

It shows up elsewhere too: dates written as 03/04/2025, which mean March or April depending on the country; prices without a currency; time stamps without a time zone; the order of bytes in a number, which differs between processors; file extensions that don't match the contents; emoji that look different on every phone; Swedish sorting, where "ä" comes after "z"; Turkish, where the capital of "i" is "İ"; and web addresses using lookalike letters from other alphabets.

What these share is that meaning lives in the convention, not the data. A sequence of bytes, a number or a pixel is a sign, and it means one thing or another depending on which agreement you read it with. Systems that work either carry that agreement with the data or settle it at the boundary, once, on purpose.

Motifs: [every representation has an edge](../motifs.md#every-representation-has-an-edge), [enforce it once, at the boundary](../motifs.md#enforce-it-once-at-the-boundary).

## It really happened

Kasia is fictional; her bookshop's problem was the web's. ASCII, published in 1963, gave numbers to 128 characters, enough for English. Every other language needed its own extension, and dozens appeared: separate standards for Western, Central and Eastern European text, several for Japanese, and others for Greek, Hebrew and Arabic, all reusing the same numbers for different letters. The Japanese even had a word for the result: *mojibake*, roughly "character transformation".

Unicode, first published in 1991, set out to give every character in every writing system a single number. The encoding that made it practical was designed in September 1992 by Ken Thompson and Rob Pike, sketched on a placemat in a New Jersey diner, according to Pike's account ([Pike's history of UTF-8](https://doc.cat-v.org/bell_labs/utf-8_history) <!-- verify -->). UTF-8 stored the original 128 ASCII characters exactly as before, so old English text was already valid, and used longer sequences for everything else. It became the dominant encoding on the web.

One alphabet for everything brought its own trick. In 2017 the security researcher Xudong Zheng registered a domain written entirely in Cyrillic letters that looked identical to "apple.com", and showed that Chrome, Firefox and Opera displayed it as if it were the real thing. Chrome changed how it displayed such addresses in version 58 ([Zheng, "Phishing with Unicode Domains"](https://xudongz.com/blog/2017/idn-phishing/)). The bytes were different; the signs were the same to a human eye.

## What it is

An encoding is a convention mapping meanings to bytes: characters to numbers (character encodings such as ASCII, ISO 8859 and UTF-8), but also units, time zones, colour spaces and number formats. Unicode assigns every character a number called a code point; UTF-8 is the most common way to store those numbers as bytes. Problems arise when data is decoded with a different convention from the one that encoded it, and the bytes give no sign of it. The working rule is to decode at the boundary using a declared or agreed encoding, use one internal representation everywhere, encode again only on output, and reject what doesn't decode instead of guessing. Comparing text needs its own decisions, such as normalisation and case and accent rules, because the same visible text can be stored in more than one way.

## Where it gets misapplied

- **Guessing the encoding.** Programs that sniff bytes and pick an encoding get it right often enough to be trusted, and wrong often enough to corrupt data.
- **Converting more than once.** Each wrong round trip garbles text further, and some losses can't be undone.
- **Comparing text byte by byte.** Two names that look identical can differ in storage, and two that differ can be meant as the same.
- **The mirror:** declaring every possible convention on every value, everywhere. Settle it at the boundary and keep the inside simple; one agreed convention beats a thousand labels nobody reads.

## Connections

- Learning this is also learning [information](information.md), because an encoding is a codebook, and data means nothing to someone who doesn't share it.
- Learning this is also learning [serialization formats](../data/serialization.md), because a format is a set of encodings agreed between two programs, and anything left unagreed is a bug waiting.
- Learning this is also learning [designed for human senses](../signals/perception.md), because pixel values are encoded too, in a colour space recorded in a profile.
- Learning this is also learning [input validation](../auth/input-validation.md), because text should be decoded and normalised before it's checked, or two spellings of the same thing get different answers.
- Learning this is also learning [tokens and context windows](../ai/tokens.md), because language models read text as tokens built from encoded bytes, and the encoding shapes what a token can be.

## Resources

1. Joel Spolsky, ["The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)"](https://joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses) (2003) (start here: still the clearest short introduction).
2. Rob Pike, ["UTF-8 history"](https://doc.cat-v.org/bell_labs/utf-8_history) (2003) (go deeper: the placemat, in the designers' own emails). <!-- verify -->
3. The Unicode Consortium, [*The Unicode Standard*](https://www.unicode.org/standard/standard.html) (reference: especially the sections on normalisation and security). <!-- verify -->

## Names you'll hear

- **Character encoding, character set:** the mapping between characters and numbers.
- **ASCII, ISO 8859, Windows-1252:** older encodings, one byte per character, each for a few languages.
- **Unicode, code point:** one number for every character, written like U+0141 for Ł.
- **UTF-8, UTF-16:** ways of storing code points as bytes.
- **Mojibake:** garbled text from decoding with the wrong encoding.
- **Normalisation:** converting text to a standard form so equal-looking strings compare equal.
- **Homograph attack:** using lookalike characters to impersonate something.

## Go and look

Open a text file in a code editor and find where it shows the file's encoding, usually in a corner. Change it to a different encoding and watch what happens to any accented letters. Then find where something you run accepts text from outside, and check whether it ever decides which encoding that text is in.
