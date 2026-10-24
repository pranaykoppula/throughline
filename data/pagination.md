# Pagination

Last reviewed: 2026-10-24

A concept page: showing a long, changing list a piece at a time without skipping, repeating, or slowing down.

## Problem

No screen shows a million items at once, so lists are served in pages. The obvious way, numbered pages that skip the first so many items, works for short lists that don't change. Feeds change constantly, and lists grow long, and then page numbers show duplicates, skip items, and get slower the deeper anyone scrolls.

## The story

In 2012 Hamza Okafor built the activity feed for a professional networking app. The feed showed twenty items at a time, newest first. Page one was the first twenty; page two skipped twenty and took the next twenty; and so on. The database query was the standard one, and every tutorial showed it.

Users started reporting that the feed repeated itself. Scroll down, and there were items they'd just seen. Hamza tried it and couldn't reproduce it, until he tried during the busy morning hours. Between loading page one and scrolling to page two, five new items had arrived at the top of the feed. Everything shifted down by five. "Skip twenty" now skipped the five new items and fifteen old ones, so the last five of page one appeared again at the top of page two. When items were deleted, the opposite happened, and some were skipped and never shown at all.

There was a second problem in the database's logs. Some users scrolled a long way back, and a request for page five hundred meant the database had to find and discard ten thousand items before returning twenty. Deep pages took seconds, and a few bots that crawled feeds to the end were slowing everyone down.

*Before reading on: "skip N items" was wrong whenever the list changed, and slow when N was large. What could the next request say instead?*

Hamza changed what the request remembered. Instead of "page two", the app sent back the position of the last item it had shown: its timestamp and ID. The next request asked for "the twenty items older than this one". New items arriving at the top no longer shifted anything, because the request didn't count from the top. And the database could jump straight to that position using its index on time and ID, so page five hundred was as fast as page one. The app no longer showed page numbers, which nobody had used anyway. It just kept loading as people scrolled.

Looking back, Hamza thought page numbers had come from printed books, where pages don't change while you read. A feed was more like a river. You couldn't count your way back to a spot in it. You could only remember where you'd got to.

## Where it shows up

| Page | The list | What it needed |
| --- | --- | --- |
| [6, Anyone can publish](../06-anyone-can-publish.md) | Infinite feeds | A way to page through data that changes underneath you; page numbers couldn't do it. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Maya's precomputed feeds | The same feed, built at write time, served a slice at a time. |
| [B-trees](../dsa/b-trees.md) | An index on time and ID | Lets the database jump to "older than this" directly, instead of counting. |
| [Round trips](../latency/round-trips.md) | Each page a request | Page size trades round trips against the size of each response. |

It shows up elsewhere too: search results, API endpoints listing records, admin screens, and exports of large tables.

What these share is that a position in a changing list is best described by the item you reached, not by a count from the start.

## It really happened

Hamza is fictional; his change is how most large APIs now page. Many public APIs, including those of large social networks and messaging platforms, return a cursor, an opaque token marking where the last page ended, instead of page numbers. Markus Winand's *Use The Index, Luke* explains the database side, and campaigns against deep offset queries under the slogan "no offset" ([Winand](https://use-the-index-luke.com/no-offset) <!-- verify -->).

## What it is

Pagination returns a large result in pieces. Offset pagination, skipping N and taking the next M, is simple and supports jumping to page numbers, but it repeats or skips items when the list changes, and gets slower as N grows. Cursor, or keyset, pagination returns items after a remembered position, usually the sort key of the last item seen. It's stable under insertions and fast at any depth with a suitable index, at the cost of not supporting "jump to page 37".

## Where it gets misapplied

- **Offset pagination on live feeds.** Duplicates and gaps as items arrive.
- **Deep offsets.** Page ten thousand costs the database ten thousand pages of work.
- **Sorting by a value that isn't unique.** Items with the same timestamp get split or repeated across pages; add a tiebreaker like the ID.
- **The mirror:** cursors for a small, static admin table where people really do want page numbers. Offsets are fine there.

## Connections

- Learning this is also learning [B-trees](../dsa/b-trees.md), because keyset pagination is a range scan from a position, which is what B-tree indexes do well.
- Learning this is also learning [access patterns](access-patterns.md), because "newest first, then keep scrolling" is a pattern the index should be built for.
- Learning this is also learning [consistency](consistency.md), because a list changing between requests is copies of the truth at different moments.
- Learning this is also learning [round trips](../latency/round-trips.md), because each page is a round trip.
- Learning this is also learning [state machines](../dsa/state-machines.md), because a cursor is the state of a walk through the list, handed to the client to keep.

## Resources

1. Markus Winand, ["We need tool support for keyset pagination"](https://use-the-index-luke.com/no-offset) (start here). <!-- verify -->
2. Your database's documentation on indexes and range queries (go deeper).
3. The pagination section of a large public API's documentation (reference: how cursors are exposed in practice).

## Names you'll hear

- **Offset, limit:** skip this many, return this many.
- **Cursor, keyset pagination:** continue from a remembered position.
- **Opaque cursor:** a token the client passes back without interpreting.
- **Infinite scroll:** loading more as the user scrolls, with no page numbers.
- **Tiebreaker:** a second sort key, usually an ID, so positions are unique.

## Go and look

Find a list in an app you build that uses page numbers or offsets. Open it, add an item from another tab, and go to the next page. Check whether anything repeats.
