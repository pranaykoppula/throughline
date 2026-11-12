# Compression

Last reviewed: 2026-11-03

A concept page in the information family: making data smaller by removing what's repeated, or what someone has decided you won't miss, and who that someone was thinking of.

## Problem

Storing and sending data costs money and time, and most data is larger than the information in it. Lossless compression removes the repetition and gives back exactly the original. Lossy compression goes further and throws information away, keeping what a model of the receiver says matters. It's only safe if that model matches whoever actually uses the result.

## The story

In 2010 Mei Lin Chou ran the document systems for a property insurer in Leeds. Forty years of claim files, each a folder of forms, photographs, builders' quotes and invoices, filled two floors of a warehouse. The board wanted them scanned and the warehouse closed.

Mei Lin tested the scanners' settings on a hundred real files. The standard lossless setting, which kept every pixel exactly, made files that would have needed a storage system the size of the budget. The scanners' "high compression" mode made files ten times smaller. She put the two versions side by side on a screen, page after page, and couldn't tell them apart. Text was crisp. If anything the compressed pages looked cleaner. She chose high compression, and the project came in under budget.

Two years later a loss adjuster disputed a claim. The scanned builder's invoice said £8,840; the builder's own copy said £6,840. The adjuster assumed fraud until a colleague found the original paper in a box that hadn't been shredded yet. It said £6,840. The scan was sharp, clean and wrong.

Mei Lin took it apart. To save space, the high-compression mode looked for small patches of the page that resembled each other, such as letters and digits, stored one copy of each, and drew that copy everywhere it judged the shape to appear again. On a slightly smudged invoice, a 6 had looked enough like an 8 to be replaced by one. Nothing marked the substitution. The page didn't look damaged; it looked like a clean page with a different number on it. She ran a test on a sample of the archive and found the same kind of substitution in several hundred documents.

*Before reading on: the compression had been tested by eye and looked perfect, and it had quietly changed numbers. What had the test missed, and what would you have done instead?*

The test had asked the wrong person. The compression's idea of what didn't matter was built for someone glancing at a page, for whom one clean digit shape is as good as another. The people who used claim files read numbers, and to them a 6 and an 8 were the whole point. Mei Lin rescanned everything still held on paper with lossless compression and paid for the storage. Pages where only a picture mattered, like photographs of water damage, could use ordinary lossy compression, which blurred fine detail rather than replacing it, so its losses looked like losses. Every scan recorded which setting made it. Files scanned before the change were marked as possibly unreliable for figures, and any number that mattered in a dispute was checked against paper or the other party's copy.

Looking back, Mei Lin thought lossy compression was a decision about the receiver, made in advance by someone who'd never met them. The question to ask wasn't whether it looked right. It was what the compression had decided she wouldn't miss, and whether that was true for everyone who'd ever use the file.

## Where it shows up

| Page | What was compressed | What it decided you wouldn't miss |
| --- | --- | --- |
| [Information](information.md) | Thomas's telegraph code | Redundancy. Lossless, but nothing was left to catch an error. |
| [Distributions and percentiles](../math/percentiles.md) | Thousands of response times into one average | The tail, which is where users suffered. |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Every checkout into overall success rates | One small group whose checkouts were all failing. |
| [Tokens and context windows](../ai/tokens.md) | A contract cut down to the few most relevant sections | Whatever retrieval judged irrelevant, which is right until it isn't. |
| [Storage tiers](../cost/storage-tiers.md) | Thumbnails kept hot, originals archived | Detail, for most uses; the cost motive behind every compression decision. |

It shows up elsewhere too: images, audio and video, log sampling, summaries, executive dashboards, abstracts of papers, and the "too long; didn't read" line at the top of a document.

What these share is the split between the two kinds. Lossless compression finds and removes repetition, and is always reversible. Lossy compression keeps what a model of the receiver says matters and discards the rest for good. Averages, dashboards and summaries are lossy compression too, and they deserve the same question: whose idea of what matters did this keep?

## It really happened

Mei Lin is fictional; her scanners are real. In 2013 David Kriesel, a German computer scientist, found that some Xerox office scanners could change numbers in scanned documents. In his test a room's area on a building plan went from 21.11 to 14.13 square metres. The cause was the JBIG2 compression setting, which substitutes visually similar patches across a page. Xerox released a patch, and documents already scanned remained in doubt ([TidBITS](https://tidbits.com/2013/08/05/researcher-finds-some-copiers-can-alter-scanned-numbers/)).

Summaries are lossy too, and the stakes can be higher. While the space shuttle Columbia was in orbit in 2003, engineers briefed managers on whether foam striking the wing could have damaged it. A slide's title spoke of "conservatism" in the test data. Further down, the bullets noted that the actual impact was far outside the conditions the tests had covered. The accident investigation board wrote that it was easy to see how a senior manager might read the slide and not realise it addressed a life-threatening situation. Edward Tufte's critique, *The Cognitive Style of PowerPoint*, made the slide famous. Meanwhile the good lossy formats, JPEG (1992) and MP3, succeed because they model their receiver well: they discard what human eyes and ears are least sensitive to.

## What it is

Compression represents data in fewer bits. Lossless compression removes statistical redundancy, such as repeated patterns and predictable symbols, and can be reversed exactly; Shannon's entropy is the limit on how small it can go. Lossy compression also discards information, choosing what to keep by a model of the receiver: human vision, human hearing, or a reader's attention. It can go much smaller, it can't be undone, and its errors are only acceptable if they fall where that model says nobody will look.

## Where it gets misapplied

- **Lossy compression on data whose details matter.** Numbers, text, legal and medical records: use lossless.
- **Errors that look like data.** Substitution is worse than blur, because blur announces itself.
- **Summaries treated as the record.** A dashboard, an average or a slide is a lossy copy; keep the originals and know how to get back to them.
- **The mirror:** keeping everything uncompressed forever. Most data has plenty of redundancy, and lossless compression costs almost nothing in accuracy.

## Connections

- Learning this is also learning [information](information.md), because compression removes redundancy, which is also what protects a message from errors.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because an average is the most common lossy compression of all.
- Learning this is also learning [storage tiers](../cost/storage-tiers.md), because the motive for compressing is almost always cost.
- Learning this is also learning [round trips](../latency/round-trips.md), because smaller payloads cross the network faster.
- Learning this is also learning [tokens and context windows](../ai/tokens.md), because summarising a long conversation for a model is lossy compression with a model of what matters.
- Learning this is also learning [designed for human senses](../signals/perception.md), because JPEG and MP3 work by modelling human eyes and ears, and image numbers are already shaped by that model.
- Learning this is also learning [greedy algorithms](../dsa/greedy.md), because Huffman codes are built greedily, and are provably the shortest possible.

## Resources

1. Colt McAnlis and Aleks Haecky, *Understanding Compression* (2016) (start here: practical and readable).
2. David Kriesel's write-up of the Xerox scanner issue, or [TidBITS's summary](https://tidbits.com/2013/08/05/researcher-finds-some-copiers-can-alter-scanned-numbers/) (go deeper: a lossy compressor whose model of the receiver was wrong).
3. Edward Tufte, *The Cognitive Style of PowerPoint* (2003) (reference: summaries as lossy compression, with the Columbia slide).

## Names you'll hear

- **Lossless, lossy:** exactly reversible, or not.
- **Compression ratio:** how much smaller the result is.
- **Entropy coding:** giving frequent symbols short codes, as Morse did.
- **Perceptual coding:** discarding what eyes or ears won't notice, as JPEG and MP3 do.
- **Artifact:** a visible or audible trace of lossy compression, like blockiness or blur.

## Go and look

Find a summary you rely on, such as a dashboard, a weekly report, or an average on a status page. Find out what it was compressed from, and one thing it discards that someone, somewhere, would care about.
