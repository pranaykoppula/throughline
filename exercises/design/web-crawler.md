# The crawl

A design case in the category **search**. It draws on [asynchronous work](../../design/async-work.md), [rate limiting and backpressure](../../design/rate-limiting.md), [timeouts](../../design/timeouts.md) and [Bloom filters](../../dsa/bloom-filters.md).

## The situation

A research organisation wants a fresh copy of a large part of the public web, about a billion pages, refreshed every month, to study how news and public information spread. Its first crawler was a program on one machine that fetched pages, extracted their links and added them to a list to fetch. It got stuck for days inside a calendar website that generated a new page for every day into the future, and it was blocked by several news sites within hours for fetching hundreds of pages a second from each of them.

## Requirements and numbers

- Fetch about a billion pages a month, and keep their text and links.
- Never fetch the same site too fast: at most about one request a second per site, and less if the site asks.
- Respect each site's rules about what may be crawled.
- Don't fetch the same page twice in a crawl, and don't get trapped in endless generated pages.
- Prioritise: important, frequently changing pages first.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** A graph of pages and links, far larger than any list in memory, and owned by strangers.
- **What limits bind?** Not bandwidth: the politeness rule per site.
- **How does it fail?** Slow sites, dead sites, enormous pages, traps, and duplicates under different addresses.

## The tempting first design

One queue of URLs. Many workers take URLs from it, fetch them, extract links and add any new ones to the queue. A database table of every URL seen decides what's new.

A single queue fills with the links of whatever site was crawled last, so workers hammer one site at a time; that's how the news sites blocked it. A table of a billion URLs is queried for every link extracted, tens of billions of lookups a month. A slow site ties up a worker for its whole timeout. And a site that generates pages without end feeds the queue faster than anything can drain it.

## Hints

<details markdown="1"><summary>Hint 1</summary>

The per-site limit, not the number of workers, sets the pace for each site. How would you organise the queue so that no site is ever fetched faster than its limit, while all workers stay busy?

</details>

<details markdown="1"><summary>Hint 2</summary>

"Have I seen this URL?" is asked tens of billions of times, and a wrong "yes" now and then only means a page is skipped this month. Which structure answers that cheaply?

</details>

<details markdown="1"><summary>Hint 3</summary>

How would you notice that a site is generating pages without end, before it has filled the queue?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

A billion pages a month is about 400 a second. At an average of about 100 kilobytes a page, that's 40 megabytes a second, about 100 terabytes a month of raw pages; compressed text is a fraction of that. If each site may be fetched at one page a second, 400 pages a second needs at least 400 sites in progress at all times, and in practice thousands, since most sites are small ([estimates](../../design/estimates.md)).

### Design A: a frontier of per-site queues

- **The frontier.** URLs waiting to be fetched are grouped by site, one queue per site. A scheduler keeps, for each site, the earliest time it may next be fetched, in a [heap](../../dsa/heaps.md) ordered by that time. A worker asking for work gets a URL from the site whose time has come, and the site's next time is pushed back by its limit ([rate limiting](../../design/rate-limiting.md)).
- **Partitioned by site.** Sites are divided among crawler machines by hashing the site's name, so each site's politeness is enforced in one place, and a machine's frontier fits on its own disks ([partitioning](../../data/partitioning.md)).
- **Seen-before checks.** Each machine keeps a [Bloom filter](../../dsa/bloom-filters.md) of URLs it has scheduled this crawl. A rare false positive skips a page until next month, which is acceptable. URLs are normalised first (lower-case host, sorted parameters, no tracking parameters), and page contents are fingerprinted, so the same page at two addresses is stored once.
- **Fetching as async work.** Fetchers use short connection and read timeouts and a size limit, and give up on slow sites rather than wait. Failed fetches go back to the frontier with a later time and a retry count, and give up after a few tries ([timeouts](../../design/timeouts.md), [asynchronous work](../../design/async-work.md)).
- **Rules and traps.** Each site's crawl rules are fetched first and cached. A budget per site (pages per crawl, link depth from the site's front page) stops generated pages from filling the frontier.
- **Priority.** Within each site, important pages, measured by how many other sites link to them, and pages that changed last time, are fetched first.

**What it costs:** a lot of state per machine, and a crawl whose speed is set by politeness to thousands of small sites rather than by hardware.

### Design B: a batch crawl in rounds

Crawl in rounds: a batch job takes the list of known URLs, decides which to fetch this round, partitions them by site, and hands each partition to fetchers that obey the per-site limit within it. After the round, another batch job extracts links, removes duplicates exactly by joining against the full list, and produces the next round's list ([batch or stream](../../design/batch-or-stream.md)).

**What it gives:** exact deduplication, simple recovery (rerun a round), and easy analysis between rounds.

**What it costs:** freshness. A page linked for the first time today waits for the next round. For a monthly research crawl, that's fine; for a search engine that wants breaking news within minutes, Design A, or a mix, is needed.

</details>

## What breaks at ten times the size

- **Ten billion pages.** The Bloom filters and frontiers grow tenfold; more machines, partitioned by site, handle it, but the biggest sites need their own machines.
- **Rendering.** Many pages build their content with scripts; fetching the HTML isn't enough, and running a browser per page costs a hundred times more.
- **Freshness.** Refreshing a few million news pages hourly while the rest refresh monthly needs two speeds of crawl sharing the same politeness limits.

## Where people slip

- **One global queue.** It crawls one site at a time, fast, and gets blocked.
- **A database lookup per link.** Use a compact, approximate membership check; a skipped page is a small cost.
- **No limits per site.** Calendars, search results and session IDs in URLs produce endless pages.
- **Waiting on slow sites.** Short timeouts and moving on keep workers busy.
- **Ignoring a site's rules.** It's impolite, it gets the crawler blocked, and it may be unlawful.

## Related

- The other case in this category: [three letters in](search-as-you-type.md), search-as-you-type suggestions.
- Design pages: [rate limiting and backpressure](../../design/rate-limiting.md), [asynchronous work and message queues](../../design/async-work.md), [timeouts](../../design/timeouts.md), [batch or stream](../../design/batch-or-stream.md).
- Other pages: [Bloom filters](../../dsa/bloom-filters.md), [heaps](../../dsa/heaps.md), [graphs](../../dsa/graphs.md), [partitioning](../../data/partitioning.md), [hashing](../../dsa/hashing.md), [search](../../dsa/search.md).
