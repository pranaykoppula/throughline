# Tries

Last reviewed: 2026-11-12

A concept page: a tree that stores words by their letters, so that everything sharing a beginning shares a path. It answers "what starts with this?" as fast as you can type, and it's how routers match addresses, how autocomplete keeps up with your fingers, and part of how search engines read their indexes.

## Problem

Some questions are about beginnings, not whole keys: every product name starting with "para", every phone number starting with an area code, the most specific route for an address. A hash table can't help, because it only answers about exact keys. A sorted list can find the range of matches, but every keystroke starts the search again from scratch. What's needed is a structure where typing one more letter means taking one more step, not starting over.

## The story

In 2009 Anjali Kulkarni built the search box for an online pharmacy in Pune. Pharmacists at two hundred partner shops typed the start of a medicine's name, and the box had to suggest matches as they typed: forty thousand medicines, many with similar names, where picking the wrong one could hurt someone. Her first version asked the database, on every keystroke, for names beginning with what had been typed so far. It was simple, and correct, and with a few shops it felt instant. With two hundred shops typing all day, the database spent most of its time answering autocomplete, and suggestions lagged a second behind the typing.

She moved the names into the server's memory, in a structure built for beginnings: a tree in which each step down was one letter. From the root, the letter P led to everything starting with P, then A to everything starting with PA, and so on. Every name was a path, and names that shared a beginning shared the path as far as they agreed. To suggest completions for "para", the server took four steps from the root and listed what lay below. Typing a fifth letter took one more step from where it already was. The lag disappeared.

Then the server's memory use climbed far past what she'd expected. Forty thousand names had become well over a million nodes, and each node set aside room for a link to every possible next character, letters, digits, hyphens and spaces, most of them empty. Long chemical names were the worst: "hydrochlorothiazide" and its few relatives ran for a dozen letters in a single file, one node per letter, each node nearly all empty space.

*Before reading on: the tree was fast because each letter was a step, and huge for the same reason. What would you have changed?*

Anjali kept the shape and squeezed out the waste. A node now stored only the links it actually had, in a small list, instead of a slot for every possible character. And wherever a path ran on with only one way forward, she merged the run into a single node labelled with the whole stretch of letters: one node for "rochlorothiazide" instead of sixteen. The tree branched only where names really diverged. Memory fell to a small fraction of what it had been, and the speed was unchanged.

Speed wasn't the whole problem. The prefix "par" matched four hundred medicines, and the box could show eight. Listing them alphabetically buried the common ones. Anjali stored, at each node, the eight most-dispensed names somewhere beneath it, updated each night from the sales figures. Now each keystroke was one step down the tree and a list that was already waiting there.

Looking back, Anjali thought the tree had been the right idea from the start, because it matched how people typed: one letter at a time, from the beginning. The mistakes had been in the bookkeeping: storing room for paths that didn't exist, and answering "what matches?" when the pharmacist was asking "which one do I probably mean?".

![A tree of medicine names stored by their letters. Names sharing a beginning share a path from the top. Left: one node per letter, with long single-file chains. Right: the same names with each single-file chain merged into one node, branching only where names differ.](../images/figures/dsa-tries.svg)

*The same names, one letter per node and then compressed. The tree only needs to branch where the names do.*

## Where it shows up

| Page | The prefixes | What the tree gave |
| --- | --- | --- |
| [Search](search.md) | Agnes's archive search box, suggesting as readers typed | Popular queries completed from their first few letters. |
| [Sorting](sorting.md) | Names in alphabetical order | A sorted list can find a prefix too, as a range; a trie avoids starting again on every keystroke. |
| [Hash tables](hash-tables.md) | Exact keys | The contrast: perfect for "this key", useless for "keys starting with this". |

It shows up elsewhere too: autocomplete in search boxes and phones, spell checkers, the routing tables of internet routers, URL routing in web frameworks, phone exchanges matching dialled numbers, compressing collections of similar strings, and the tokenisers that split text for language models.

What these share is a question about beginnings, asked one step at a time. Storing keys by their prefixes turns "what starts with this?" into a walk down a tree, and compressing the paths keeps the tree no bigger than the places where the keys actually differ.

## It really happened

Anjali is fictional. René de la Briandais described the idea in 1959, for file searching with keys of varying length, and Edward Fredkin independently described it in 1960. He named it *trie* from the middle of "retrieval", and it's usually pronounced "try" to tell it apart from "tree". In 1968 Donald Morrison published PATRICIA, a trie that skips one-way branches, the same compression Anjali used, and compressed tries of this kind are now often called radix trees ([NIST, "trie"](https://xlinux.nist.gov/dads/HTML/trie.html) <!-- verify -->).

Internet routers face the prefix problem billions of times a second. A router's table lists blocks of addresses, from very broad to very specific, and each packet must go to the route with the longest prefix matching its destination address. Software routers, including the one inside the Linux kernel, have long used compressed tries for this lookup, and dedicated hardware does the same job with specialised memory.

## What it is

A trie stores a set of strings as a tree in which each edge is labelled with a character (or a run of characters), so that each string is a path from the root and strings sharing a prefix share the beginning of their path. Looking up a key, or every key with a given prefix, takes steps in proportion to the length of the key, not the number of keys. Naive tries waste memory on sparse nodes; compressed tries (radix trees, PATRICIA) merge chains with a single child. Nodes can carry extra data, such as counts or the most popular completions below them, to answer ranking questions cheaply.

## Where it gets misapplied

- **Asking the database on every keystroke.** Anjali's first version: correct, and a constant load for the most frequent query in the system.
- **A slot for every possible character in every node.** Memory grows with the alphabet, not with the data.
- **Answering "what matches?" when people are asking "what do I mean?".** Four hundred matches in alphabetical order is technically correct and useless.
- **The mirror:** a trie for exact lookups only. If nobody ever asks about prefixes, a hash table is simpler and faster.

## Connections

- Learning this is also learning [search](search.md), because prefix completion is the first thing a search box does.
- Learning this is also learning [hash tables](hash-tables.md), because both find keys quickly, but only a trie can answer questions about beginnings.
- Learning this is also learning [sorting](sorting.md), because a sorted list answers prefix questions as ranges, which is the alternative to a trie.
- Learning this is also learning [round trips](../latency/round-trips.md), because a suggestion that needs a database query on every keystroke pays a round trip per letter.
- Learning this is also learning [tokens and context windows](../ai/tokens.md), because tokenisers match the longest known piece of text at each position, a trie-shaped question.

## Resources

1. [VisuAlgo, trie](https://visualgo.net/en/suffixtree) (start here: watch strings share their prefixes; this page covers the closely related suffix tree). <!-- verify -->
2. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th edition, section 5.2, "Tries" (go deeper).
3. Edward Fredkin, "Trie Memory", *Communications of the ACM* (1960) (reference).

## Names you'll hear

- **Trie, prefix tree:** a tree that stores strings by their characters.
- **Radix tree, PATRICIA, compressed trie:** a trie with single-child chains merged.
- **Longest prefix match:** finding the most specific stored prefix of a key, as routers do.
- **Suffix tree:** a trie of every ending of a text, for finding any substring quickly.
- **Autocomplete, typeahead:** suggesting completions as someone types.

## Go and look

Type slowly into a search box you use and watch the suggestions change with each letter. Then find out whether something you build answers prefix questions, and whether each keystroke starts a new search from the beginning.
