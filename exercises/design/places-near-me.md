# The café round the corner

A design case in the category **location and matching**. It draws on [partitioning](../../data/partitioning.md), [caching](../../performance/caching.md), [replication](../../data/replication.md) and [search](../../dsa/search.md).

## The situation

A travel app lets people search for places near them: "coffee", "pharmacy open now", "vegetarian restaurant". It shows the best matches within walking distance, on a map and as a list, ordered by a mix of distance, rating and relevance. It covers 150 million places worldwide. The first version stored places in a database with latitude and longitude columns and searched within a box around the user. In a city centre, "restaurant" within a kilometre matched thousands of places, all fetched and sorted for every search; in the countryside, the box was empty and the user saw nothing at all.

## Requirements and numbers

- Return the best 20 places for a query near a point, in under 200 milliseconds.
- Work equally in a dense city centre and an empty rural area, widening the search where places are sparse.
- Filters: category, "open now", price, rating.
- Places change slowly (new openings, changed hours); reviews and ratings change daily.
- About 150 million places. About 50,000 searches a second at peak, worldwide, following the evening around the globe.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** Data that is read far more than it changes, and nearly always read by place.
- **What can we do with it?** "Find near this point" is a spatial question; "and matching 'vegetarian'" is a text question; both at once is the difficulty.
- **What breaks at ten times?** The densest few square kilometres in the world.

## The tempting first design

A table of places with latitude and longitude, indexed on each. A search selects places with latitude and longitude inside a box around the user, filters by category, computes the distance to each, and sorts.

An index on latitude finds everything in a horizontal band right round the world, and the database must then check the longitude of each; the box is only fast if the index understands two dimensions. A fixed-size box returns thousands of places in central Tokyo and none in rural Scotland. And every search sorts its matches from scratch.

## Hints

<details markdown="1"><summary>Hint 1</summary>

How could you give every small area of the Earth's surface an ID, so that "places near here" becomes "places in these few IDs"?

</details>

<details markdown="1"><summary>Hint 2</summary>

If the area IDs were built so that nearby areas share a prefix, how would you widen a search that found too little, and narrow one that found too much?

</details>

<details markdown="1"><summary>Hint 3</summary>

The data changes slowly and is read constantly, nearly always by place. How would you split it across machines, and how many copies would you keep?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

150 million places at about 2 kilobytes each, with their names, categories, hours and a summary of reviews, is about 300 gigabytes: too much for one machine's memory, easy for a dozen. 50,000 searches a second is a lot of reads, but they're reads of slowly changing data, which can be copied many times. Writes, new places and changed hours, are a few a second ([estimates](../../design/estimates.md)).

### Design A: cells with prefixes, partitioned by place

- **Cells.** The Earth's surface is divided into cells in a hierarchy: each cell divides into smaller ones, and a cell's ID is a prefix of its children's IDs. Geohashes and similar schemes work this way. Every place is stored with the ID of the small cell it's in ([tries](../../dsa/tries.md) work the same way with letters).
- **Search by rings.** For a search, find the user's cell at a fine level and its neighbours, collect matching places, and if there are too few, move up a level to larger cells and repeat. In a city centre the first ring is enough; in the countryside the search widens until it finds something.
- **Ranking.** Candidates are scored by a mix of distance, rating and how well they match the query, and the top 20 are returned ([search](../../dsa/search.md)).
- **Partitioned by region, copied many times.** Places are partitioned by large cells, so a search usually touches one or two partitions; each partition is copied many times, since the data is read far more than it's written ([partitioning](../../data/partitioning.md), [replication](../../data/replication.md)).
- **Caching.** Popular searches in popular places, "coffee" in a busy station's cell, are cached for a few minutes ([caching](../../performance/caching.md)). "Open now" is computed at request time, since it changes by the minute.

**What it costs:** partitions by region are uneven: central London's partition is far busier than the Sahara's, so busy regions need smaller partitions and more copies.

### Design B: a search engine with a geographic index

Use a search engine that supports geographic queries alongside text: places are indexed with their text and location, and a query combines "matches 'vegetarian'" with "within 1 km" and a distance-aware score.

**What it gives:** text relevance, typos, synonyms and filters together with location, in one query.

**What it costs:** a heavier system per query, and less control over how the search widens in sparse areas. Many services use a search engine for the text and their own cell index to choose which part of the index to search.

</details>

## What breaks at ten times the size

- **Hot cells.** The busiest few square kilometres need their own partitions and many more copies than the average.
- **Freshness.** Ratings and "busy now" estimates change constantly; keep them in a separate, frequently updated store, joined at request time, rather than rebuilding the place index.
- **Personalisation.** Ranking for each user's tastes can't be cached per cell; cache the candidates and rank them per user.

## Where people slip

- **Separate indexes on latitude and longitude.** Each finds a band around the whole Earth; use a spatial index.
- **A fixed search radius.** Too many results in cities, none in the country; widen and narrow by cell.
- **Distance as the only ranking.** The closest café isn't always the best answer to "coffee".
- **Ignoring the cell edge.** A user standing at the edge of a cell has neighbours in the next one; always search the surrounding cells too.

## Related

- The other case in this category: [the nearest car](ride-hailing.md), ride-hailing dispatch.
- Design pages: [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [partitioning](../../data/partitioning.md), [replication](../../data/replication.md), [caching](../../performance/caching.md), [search](../../dsa/search.md), [tries](../../dsa/tries.md), [B-trees](../../dsa/b-trees.md), [access patterns](../../data/access-patterns.md).
