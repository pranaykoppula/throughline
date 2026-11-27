# Time and ordering

Last reviewed: 2026-11-27

A concept page: across machines there's no single clock, so "which happened first?" can't be answered by comparing timestamps. Wall-clock time is for people. Order between events has to come from the events themselves.

## Problem

Every machine has a clock, and every clock is a little wrong: it runs fast or slow, is corrected in jumps, and occasionally goes backwards. On one machine that rarely matters. Across many, it means two events stamped a few milliseconds apart may have happened in the opposite order, and any rule of the form "the later one wins" can pick the earlier one. Systems need to know the order of events, to apply updates, resolve conflicts and explain what happened. Clocks look like the answer, and they're the wrong tool for it.

## The story

In 2013 Emre Aydın built the system behind a company in Istanbul that sold hotel rooms on dozens of booking websites at once. When a room sold on one site, his system told all the others it was gone; when a hotel added rooms, it told them they were back. Updates for the same hotel could arrive at different servers, so each server stamped every update with the time from its own clock, and when two updates for the same room disagreed, the later timestamp won. The servers' clocks were kept in step by the standard time service, to within a few milliseconds. It was the simplest rule that could work, and it worked for over a year.

Then the company moved its servers to new hardware, and one of them came up with its time service misconfigured. Its clock drifted, and within a week it was four seconds fast. Nothing complained; four seconds didn't look like anything on a screen. But every update that server stamped now seemed to have happened four seconds later than it had. When a room sold through another server and, a second or two earlier, an older "available" update had passed through the fast one, the stale update carried the later timestamp, and it won. Rooms that were sold went back on sale. Over one busy weekend, about 120 guests arrived at hotels that had already given their rooms to someone else.

*Before reading on: every server's clock was close to right, and the rule was "the latest update wins". What should "latest" have meant?*

Emre saw that he'd been using the clocks for two different things. People needed to know when a booking was made, to the minute, in their own time zone; for that, a clock that was usually right to within seconds was fine. The system needed to know which of two updates to the same room came after the other, and for that no clock was good enough, because no two clocks were the same clock. What the system needed was order, and order could come from somewhere that never drifted.

So each room's availability got a version number, kept by the database that owned the room. An update had to say which version it had seen, and the database applied it only if that was still the current version, then increased the number. A stale update, however late its timestamp, now named an old version and was refused, and its sender had to read the current state and try again. Timestamps stayed, for people and for logs, stored in universal time and converted only for display. Anything that measured a duration, such as a timeout or how long a request took, now used the machine's monotonic clock, which only ever counts forwards, instead of the time of day.

![A timeline of two updates to the same hotel room, seen by two servers. In true time, the room is marked available at 14:00:01 and then sold at 14:00:03. The fast server, four seconds ahead, stamps the older "available" update 14:00:05, so by timestamps it looks later and wins, and the sold room goes back on sale. With version numbers, the sale is version 8, the stale update names version 7, and the database refuses it.](../images/figures/design-time-and-ordering.svg)

*A clock four seconds fast is close enough for people and wrong enough for ordering. Version numbers can't drift.*

Looking back, Emre thought the clocks had never lied to him. Each one said what time it believed it was, as well as it could. He'd asked them a question about the order of events on different machines, which no clock could answer, and the answer had to be built into the data instead.

## Where it shows up

| Page | The ordering | What it taught |
| --- | --- | --- |
| [0, Representations](../00-representations.md) | The Patriot missile battery's clock | A clock counting tenths of a second in binary drifted by about a third of a second over a hundred hours, enough to miss. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Lin's numbered blocks | Numbers, not times, told the receiver what order the blocks belonged in and which were missing. |
| [Consensus and leader election](consensus.md) | Ilinca's numbered leases | Leases measured by different clocks drift apart; an increasing number lets the storage decide which leader is current. |
| [Replication](../data/replication.md) | A replica applying the main database's changes | Order comes from position in the log, not from when each change was written. |
| [Batch or stream](batch-or-stream.md) | Beatriz's bus fares, arriving hours late | When something happened and when it arrived are two different clocks. |
| [Append-only logs](../dsa/append-only-logs.md) | Teresa's ledger | A log's order is the order of the entries, decided once, and the timestamps are just for people. |

It shows up elsewhere too: a cheque book's numbered cheques, the minutes of a meeting numbered in order, the railway time that replaced each town's own noon in the nineteenth century, and the sports scoreboard that shows the order goals were scored, not each referee's watch.

What the rows share is that order between separate places has to be carried by the events themselves, as numbers that only increase or as positions in one log. Clocks tell people when; only something both sides share can tell the system which came first.

Motif: [copies disagree](../motifs.md#copies-disagree).

## It really happened

Emre is fictional, and so is his company. The theory is from 1978, when Leslie Lamport showed that in a distributed system the order of events is only partial: one event can be known to happen before another only if a chain of messages connects them. He described *logical clocks*, counters carried on messages, that give every event a number consistent with that order without any physical clock at all ([Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System"](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)).

Clocks going backwards cause real outages. At midnight on 1 January 2017, a leap second was added to universal time. Inside Cloudflare's DNS software, a duration measured by subtracting one time of day from another came out negative during that second, and the negative value eventually made the program crash, so some DNS lookups for Cloudflare's customers failed. Cloudflare's fix was to measure durations with a monotonic clock ([Cloudflare, "How and why the leap second affected Cloudflare DNS"](https://blog.cloudflare.com/how-and-why-the-leap-second-affected-cloudflare-dns)). Leap seconds have caused enough trouble that in 2022 the international body responsible for time decided to stop adding them by 2035.

Google took the opposite approach in Spanner, its global database, described in 2012: rather than trusting clocks, it measured how uncertain each clock was, with GPS receivers and atomic clocks in its data centres, and made each transaction wait out the uncertainty before committing, so that timestamps could be trusted for ordering.

## What it is

A **wall clock** (time of day) is synchronised with others, usually by NTP, to within milliseconds on a good day, and can jump forwards or backwards when corrected or when a leap second is applied; it's for showing people when something happened, and should be stored in UTC. A **monotonic clock** only moves forwards and is for measuring durations on one machine. Neither can reliably order events across machines. For that, systems use **logical clocks** (Lamport clocks, counters carried on messages), **version numbers** checked on update (optimistic concurrency, compare-and-set), **sequence numbers** from a single source or a log, or **vector clocks**, which can tell when two updates were concurrent rather than ordered. "Last write wins" by timestamp silently discards updates whenever clocks disagree; it's acceptable only when losing an update doesn't matter.

## Where it gets misapplied

- **Last write wins by timestamp.** A fast clock's stale write beats a slow clock's fresh one, silently.
- **Durations from the time of day.** A correction or leap second makes them negative or huge.
- **Local time in storage.** Daylight-saving changes make an hour repeat or vanish once a year.
- **Assuming the clock is synchronised.** Nothing warns you when a machine's time service stops working.
- **The mirror:** building logical clocks where order doesn't matter. Most timestamps are only for people, and a wall clock is exactly right for them.

## Connections

- Learning this is also learning [consensus and leader election](consensus.md), because a lease number is a logical clock, and it's what lets storage refuse a stale leader.
- Learning this is also learning [replication](../data/replication.md), because a replica's order comes from the log it applies, not from when changes were written.
- Learning this is also learning [batch or stream](batch-or-stream.md), because event time and processing time are two clocks that streaming has to keep apart.
- Learning this is also learning [append-only logs](../dsa/append-only-logs.md), because one log gives everything that reads it the same order.
- Learning this is also learning [floating point](../math/floating-point.md), because the Patriot's drifting clock was a representation error accumulating over time.
- Learning this is also learning [consistency](../data/consistency.md), because what copies may promise depends on whether they agree on the order of writes.

## Resources

1. Leslie Lamport, ["Time, Clocks, and the Ordering of Events in a Distributed System"](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) (1978) (start here: short, and the foundation of the rest).
2. Cloudflare, ["How and why the leap second affected Cloudflare DNS"](https://blog.cloudflare.com/how-and-why-the-leap-second-affected-cloudflare-dns) (2017) (a clear, small postmortem of a clock going backwards).
3. Martin Kleppmann, *Designing Data-Intensive Applications*, chapter 8 (go deeper: unreliable clocks and what to do instead).
4. Corbett et al., "Spanner: Google's Globally-Distributed Database" (OSDI 2012) (reference: making clocks trustworthy by measuring their uncertainty).

## Names you'll hear

- **Wall clock, monotonic clock:** time of day, and a counter that only moves forwards.
- **NTP, clock skew, clock drift:** the time service, and how far clocks differ and wander.
- **UTC, leap second:** universal time, and the occasional extra second added to it.
- **Lamport clock, vector clock:** counters that order events without physical time.
- **Happens-before:** the order of events that messages can establish.
- **Last write wins (LWW):** keeping the update with the latest timestamp.
- **Optimistic concurrency, compare-and-set:** applying an update only if the version it read is still current.
- **TrueTime:** Spanner's clock with a stated uncertainty.

## Go and look

Find a place in something you've built where two updates to the same thing can arrive from different places. Find out how it decides which one wins. If the answer involves comparing timestamps from different machines, find out how far apart those machines' clocks are right now.

Practise this: [the school's messages](../exercises/design/group-chat.md), group chat in the same order on every screen.
