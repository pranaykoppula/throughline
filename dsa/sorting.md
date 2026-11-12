# Sorting

Last reviewed: 2026-11-12

A concept page: putting things in order is an investment. Once data is sorted, finding, merging, grouping and spotting duplicates all become cheap. There are many ways to sort because the needs keep changing, and each famous algorithm is the right answer to a different one.

## Problem

Nearly every system **finds** things, and sorted data is what makes finding fast: you can halve the search at every step, walk a range in order, merge two lists in one pass, or spot duplicates because they sit next to each other. But sorting costs something, and what it costs depends on the data. How much there is, whether it fits in memory, whether it's nearly in order already, whether equal items must keep their original order, whether you need all of it sorted or just the top few. No single method is best for all of these, and the one that was right last year can become the slowest thing you run.

## The story

Margit Halász spent thirty-seven years in the data-processing department of a mail-order company in Chicago, and in that time she sorted the same customers in almost every way there is.

**Cards, 1961.** When she started, each customer was a punched card, and the monthly catalogue mailing had to go out in postcode order so the post office would give the company its bulk rate. Sorting a hundred thousand cards was done on a card sorter, a machine that read one column of the card and dropped it into one of ten pockets by the digit it found. Margit learned the trick everyone used. Sort on the *last* digit of the postcode first, stack the pockets in order, then sort on the second-to-last digit, and so on, finishing with the first. Five passes for a five-digit code, however many cards there were. The only rule was to keep each pocket in order when you stacked it; one dropped tray could undo the whole morning. It never needed to compare two cards at all. It worked because the keys were short digits with only ten possible values.

**Tapes, 1966.** The company bought a computer with magnetic tape drives, and customers moved onto tape: half a million records, and memory for only a few thousand at a time. A list that doesn't fit in memory can't be sorted all at once, so Margit learned the method that came with the machine. Read as many records as fitted, sort them in memory, and write them out as a sorted *run*. Then merge the runs: read the front of two sorted runs at once, always write the smaller, and the output is sorted. Merge pairs of runs into longer runs, back and forth between tape drives, until one remains. The merging was fast and steady, because tapes were good at exactly one thing, reading straight through.

For the in-memory part she wrote the simplest sort she could think of, the way people sort a hand of cards: take each record and slide it back until it sits in the right place. With a few hundred records per run, it was instant.

Two years later the company bought more memory, Margit raised the run size to eight thousand records to make fewer runs, and the sort got slower, not faster. She timed it. Doubling the run size had roughly quadrupled the time spent sorting each run, because every record could be slid past every record before it. With eight thousand records, that was tens of millions of moves.

She replaced it with a method from a short paper in a computing journal: pick one record as a pivot, move everything smaller to one side and everything larger to the other, then do the same to each side. Each split roughly halved the problem, so eight thousand records needed about thirteen levels of splitting, not thousands of slides. The runs sorted in a fraction of the time.

**The night it took six hours, 1974.** Then one night a job that normally took twenty minutes ran for six hours. Nothing had changed except the input: the day's orders had arrived already in order, because a new system upstream had sorted them. Margit's version always took the first record as the pivot. On sorted data the first record was always the smallest, so every split put nothing on one side and everything else on the other. Each level only removed one record. The method that halved the work on ordinary data did the full slide-past-everything work on data that was already in order.

*Before reading on: the faster method had a worst case, and real data had found it. What would you have changed?*

She changed the pivot to the middle value of the first, middle and last records, which made a perfectly bad split very unlikely on real data. For the one nightly job where a slow run would hold up the warehouse, she used a different method entirely, one that arranged the records into a heap, a tree that always keeps the largest at the top, and took the largest off repeatedly. It was a little slower on average and never had a bad night: its worst case and its usual case were the same.

**Ties, 1979.** Customer service asked for a report of orders sorted by customer surname, and within each surname by order date. Margit sorted by date, then by surname, expecting the dates to stay in order inside each surname. They didn't. Her quick method moved equal surnames around freely, so the earlier sort by date was scrambled. She needed a *stable* sort, one that never reorders items that compare equal. The tape merge was stable by nature, because when two records tied it always took the one from the earlier run. She used that, and remembered the card sorter: the reason it had worked digit by digit was exactly this property.

**Nearly sorted, 1990.** By then the customer file lived on disk, already sorted, and each night a few hundred new customers had to be added. Sorting all two million records again every night was a waste. Margit used the simplest method of all, the one she'd abandoned in 1968: slide each new record back into place. On a list that was already almost in order, it barely did any work. The slowest method for scrambled data was the fastest for nearly sorted data.

**Only the top hundred, 1995.** The last request of her career was a list of the hundred customers who had spent the most that year. A colleague started to sort two million customers by spending. Margit stopped him. They kept a heap of just a hundred, smallest at the top, and read through the customers once: anyone who'd spent more than the smallest in the heap replaced it. They didn't need everyone in order. They needed the top of the order.

![Two diagrams of quicksort on eight records that are already in order. Left: taking the first record as the pivot puts nothing on one side and everything else on the other, so eight levels of splitting are needed. Right: taking the middle value splits the records in half each time, so three levels are enough.](../images/figures/dsa-sorting.svg)

*Quicksort on data that's already in order: the pivot decides whether the work grows like n² or n log n.*

Looking back, Margit thought she'd never learned "the best sorting algorithm", because there wasn't one. She'd learned to ask what was true about the data: how big it was, where it lived, how ordered it already was, whether ties mattered, and how much of the order anyone actually needed. Each answer pointed to a different method, and the cleverest one could be the wrong one.

## Where it shows up

| Page | What was sorted | What the order bought |
| --- | --- | --- |
| [B-trees](b-trees.md) | Keys kept sorted on disk, in blocks | Finding any key, or any range, in a few reads. |
| [LSM trees](lsm-trees.md) | Neha's writes, sorted in memory and flushed as sorted files | Files that can be merged cheaply, the way Margit merged tapes. |
| [Pagination](../data/pagination.md) | A feed in a fixed order | A cursor: "everything after this item", which a count from the start couldn't give. |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | Changes to the same file | Merging two ordered histories line by line, which is cheap only while they haven't drifted far. |
| [Information gain](../info/information-gain.md) | Anything you can search by halving | Each comparison rules out half of what's left. |
| [Growth](growth.md) | Margit's runs of eight thousand records | Sliding each record into place grows with the square of the size; splitting grows only a little faster than the size. |

It shows up elsewhere too: database indexes and query plans that sort before joining, spreadsheets, search results ranked by relevance, leaderboards, deduplicating logs by sorting then comparing neighbours, `git bisect`, which halves a sorted history to find a bad commit, and the postcodes on every bulk mailing.

What these share is order as an investment: sort once, at a cost that depends on the data, and finding, merging and grouping become cheap afterwards. Which way to sort is a question about the data, not about which algorithm is fastest in general.

Motif: [costs move; they don't disappear](../motifs.md#costs-move-they-dont-disappear).

## It really happened

Margit is fictional; her methods arrived about when she met them. Herman Hollerith's tabulating machines processed the 1890 US census, and card sorters doing exactly her digit-by-digit radix sort were in common use by the 1920s. John von Neumann described merge sort in 1945, and sorting with merges across tapes was standard practice on early commercial computers. Tony Hoare devised quicksort in 1959, as a visiting student in Moscow working on machine translation, when he needed to sort the words of sentences; it was published in 1961 ([Stanford's history of quicksort](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2008-09/tony-hoare/quicksort.html) <!-- verify -->). J. W. J. Williams published heapsort, and the binary heap with it, in 1964.

Quicksort's worst case is not only a matter of bad luck with sorted input. In 1999 Doug McIlroy showed how an adversary could construct input that drove many library quicksorts to their slowest possible behaviour, which is why careful libraries now guard against it. The modern answer to Margit's whole career is a hybrid. Tim Peters wrote Timsort for Python in 2002. It finds the runs that are already in order in real data, sorts short stretches by insertion, and merges the runs, stably. Java, Android and many other platforms adopted it. In 2015 researchers at CWI in Amsterdam, trying to prove Timsort correct with a formal verification tool, found an input that made the Java and Python implementations fail, and their fix was adopted ([de Gouw and de Boer, ERCIM News](https://ercim-news.ercim.eu/en102/r-i/fixing-the-sorting-algorithm-for-android-java-and-python) <!-- verify -->).

## What it is

Sorting arranges items by a key. Comparison sorts decide by comparing pairs: insertion sort is simple and fast on small or nearly sorted lists but grows with the square of the size; merge sort, quicksort and heapsort grow only a little faster than the size (n log n), which is the best any comparison sort can do in general. Merge sort is stable and suits data on disk or tape; quicksort is usually the fastest in memory but has a quadratic worst case without care over the pivot; heapsort is in place with no bad cases but is not stable. Non-comparison sorts such as radix and counting sort use the structure of the keys, short digits or small integers, to beat n log n. External sorting handles data larger than memory by sorting runs and merging them. Partial sorting finds the top few without ordering everything. Real libraries combine several of these.

## Where it gets misapplied

- **Asking which sort is fastest, without asking about the data.** Margit's run of eight thousand, her pre-sorted orders, and her nearly sorted file each wanted something different.
- **Forgetting the worst case.** A method that's fast on average can be slow on exactly the input your system produces, or an attacker sends.
- **Sorting everything to get the top ten.** A heap of ten does it in one pass.
- **Assuming a sort keeps ties in order.** Only stable sorts do; sorting by several keys depends on it.
- **The mirror:** writing your own sort. Your language's built-in sort has been tuned and tested on real data for decades. Know which properties it has, and use it.

## Connections

- Learning this is also learning [growth](growth.md), because the difference between sliding and splitting is the difference between n² and n log n, and it only shows at size.
- Learning this is also learning [B-trees](b-trees.md), because an index is order kept up to date as data changes.
- Learning this is also learning [LSM trees](lsm-trees.md), because they sort in memory and merge sorted files, exactly like tape sorting.
- Learning this is also learning [queues](queues.md), because a priority queue is usually a heap, the structure behind both heapsort and the top-hundred list.
- Learning this is also learning [information gain](../info/information-gain.md), because sorted data lets each question rule out half of what's left.
- Learning this is also learning [power and predictability](power-and-predictability.md), because an attacker who knows your algorithm can choose its worst case, as with regular expressions and hash tables.
- Learning this is also learning [divide and conquer](divide-and-conquer.md), because merge sort and quicksort are its two classic forms: one does the work in combining, the other in splitting.
- Learning this is also learning [heaps and priority queues](heaps.md), because heapsort and Margit's top-hundred list are both a heap, used differently.

## Resources

1. [VisuAlgo, sorting](https://visualgo.net/en/sorting) (start here: watch each algorithm run, step by step, on data you choose). <!-- verify -->
2. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th edition, chapter 2, with free material on the book's site (go deeper: sorting explained with working code and real measurements).
3. Donald Knuth, *The Art of Computer Programming*, Volume 3: *Sorting and Searching* (reference: including the history of tape sorting).

## Names you'll hear

- **Insertion sort, merge sort, quicksort, heapsort:** the classic comparison sorts.
- **Radix sort, counting sort:** sorts that use the structure of the keys instead of comparing them.
- **Stable sort:** one that keeps equal items in their original order.
- **In place:** sorting without needing much extra memory.
- **Pivot:** the item quicksort splits around; choosing it well avoids the worst case.
- **External sort, run:** sorting data larger than memory, and the sorted pieces it merges.
- **Timsort:** the hybrid used by Python, Java and Android.
- **n log n:** how the good comparison sorts grow, and the limit for sorting by comparison.

## Go and look

Find out which algorithm your language's built-in sort uses, and whether it's stable. Then time it on a million numbers that are random, already sorted, and sorted in reverse. If the times differ a lot, the sort is reacting to the order already in the data.
