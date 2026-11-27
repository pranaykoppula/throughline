# Three letters in

A design case in the category **search**. It draws on [tries](../../dsa/tries.md), [caching](../../performance/caching.md), [batch or stream](../../design/batch-or-stream.md) and [search](../../dsa/search.md).

## The situation

A large online grocer wants its search box to suggest completions as customers type: after "str" it should offer "strawberries", "strawberry jam" and "string beans", the most popular first, and the suggestions should change with every letter. Customers abandon the search if suggestions lag behind their typing. The first version sent each keystroke to the product database with a query for names beginning with what had been typed. It worked in testing and buckled on the first Saturday morning, when hundreds of thousands of people typed at once.

## Requirements and numbers

- Up to ten suggestions for any prefix, within about 100 milliseconds of a keystroke, including the round trip.
- Ranked by how often customers have searched for them recently, so that seasonal items rise quickly.
- Never suggest something offensive, or a product that's been withdrawn.
- About 10 million searches a day, and an average of six keystrokes per search; the busiest hour is three times the average.
- About 5 million distinct past search phrases worth suggesting.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What can we do with it?** One question, asked constantly: "the top ten completions of this prefix". The set of answers changes slowly.
- **What's the peak?** Keystrokes, not searches.
- **Which answers must be fresh?** Popularity can lag by an hour; a withdrawn product must disappear within minutes.

## The tempting first design

Each keystroke queries the database: phrases beginning with the prefix, ordered by popularity, top ten. Popularity is a counter incremented on every search.

Sixty million keystrokes a day is about 700 a second on average and over 2,000 at the peak, each a range query and a sort. Short prefixes are the worst: "s" matches hundreds of thousands of phrases, all of which must be sorted to find the top ten. And every search updates a popularity counter in the same database, so reads and writes fight.

## Hints

<details markdown="1"><summary>Hint 1</summary>

The answer for a given prefix is the same for everyone and changes slowly. How many different prefixes are there, really, that customers type?

</details>

<details markdown="1"><summary>Hint 2</summary>

A trie walks to a prefix in one step per letter. What could each node store so that, once you reach it, the top ten are already there?

</details>

<details markdown="1"><summary>Hint 3</summary>

Counting popularity and answering suggestions don't have to happen in the same place, or at the same speed. Which one needs to be instant?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

Ten million searches × six keystrokes is 60 million suggestion requests a day: about 700 a second on average and about 2,000 at the peak. 5 million phrases of about 20 characters is about 100 megabytes of text; a trie over them, with a top-ten list stored at each node, fits comfortably in a few gigabytes of memory ([estimates](../../design/estimates.md)).

### Design A: a trie with precomputed answers, rebuilt in the background

- **A trie in memory.** Each node is a prefix, and stores the ten most popular complete phrases below it, already sorted. A suggestion request walks one node per letter and returns that list: no sorting at request time ([tries](../../dsa/tries.md)).
- **Counting separately.** Every completed search is written to a log. A batch job every hour counts searches per phrase over the last few weeks, weighting recent days more, so that strawberries rise in June and fall in October ([batch or stream](../../design/batch-or-stream.md)).
- **Build, then swap.** The job builds a new trie from the counts, filters out blocked words and withdrawn products, and hands it to the serving machines, which swap it in atomically. Serving never writes ([append-only logs](../../dsa/append-only-logs.md)).
- **Urgent removals.** A small block list is checked at request time, so a withdrawn product disappears within a minute without waiting for the next build.
- **Caches in front.** The browser keeps answers for prefixes it has already asked about, and short prefixes, which most customers type and whose answers barely change, are cached at the edge of the network ([caching](../../performance/caching.md)).
- **Fewer requests.** The page waits until typing pauses for about 50 milliseconds before asking, which removes many keystrokes from fast typists without anyone noticing.

**What it costs:** popularity lags by up to an hour, and every serving machine holds the whole trie in memory.

### Design B: a search engine's prefix index

Use the general search engine the shop already runs for full searches, with an index of "edge n-grams": every phrase is indexed under each of its prefixes. Suggestions become ordinary search queries, ranked by a popularity field.

**What it gives:** one system instead of two, typo tolerance and synonyms for free, and personalisation (suggesting what this customer usually buys) becomes possible ([search](../../dsa/search.md)).

**What it costs:** much more work per keystroke than a trie lookup, so more machines, and a heavier dependency on one system for both search and suggestions. A common compromise is Design A for the first few letters and Design B once the prefix is long enough to be specific.

</details>

## What breaks at ten times the size

- **More languages and shops.** One trie per language or region, each smaller, rather than one giant trie.
- **Personalisation.** Per-customer suggestions can't be precomputed for everyone; blend a shared top ten with a few items from the customer's own history at request time.
- **Fresher trends.** Hourly rebuilds miss a product that goes viral in minutes; a small stream job can keep a "trending now" list merged in at request time.

## Where people slip

- **Querying the database per keystroke.** Short prefixes match a large share of all phrases, and sorting them every time is the cost.
- **Counting and serving in the same store.** Writes from every search slow down every suggestion.
- **Forgetting the filter.** Suggestions are shown to everyone; one offensive phrase searched often enough will appear.
- **Not debouncing.** A request per keystroke from fast typists is mostly wasted.

## Related

- The other case in this category: [the crawl](web-crawler.md), a web crawler.
- Design pages: [batch or stream](../../design/batch-or-stream.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [tries](../../dsa/tries.md), [search](../../dsa/search.md), [caching](../../performance/caching.md), [append-only logs](../../dsa/append-only-logs.md), [6, Anyone can publish](../../06-anyone-can-publish.md).
