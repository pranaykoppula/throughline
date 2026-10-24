# The cost of reliability

Last reviewed: 2026-10-24

A concept page: every extra nine costs more than the last, and complexity bought for reliability can cost reliability.

## Problem

Users want software that never fails, and leaders promise it. But each step closer to "never" costs far more than the step before: more machines, more regions, more engineers, more rules about change. Past some point, the machinery added to prevent failure becomes a new source of it.

## The story

In 2015 Camille Laurent was the infrastructure lead at a startup selling scheduling software to hospitals. A large hospital group was ready to sign, and its contract asked for 99.99% availability: about four minutes of downtime a month. The CEO agreed on the spot. Camille's platform ran in one cloud region and had managed about 99.9% that year, roughly forty minutes a month.

She did what the contract seemed to demand. The whole system was rebuilt to run in two regions at once, each able to take over from the other automatically. It took six months and two extra engineers, and doubled the hosting bill. On paper, a whole region could now fail and users would barely notice.

In the next year, availability went down. The failover system itself caused three outages: twice it decided a healthy region was dead and moved everyone away from it, and once both regions briefly believed they were in charge. Keeping data in step between the regions added a new kind of bug every few weeks. Deploys got slower and riskier, because every change had to work in two places at once. Meanwhile, the outages users actually noticed were mostly bad deploys and one expired certificate, none of which a second region would have prevented.

*Before reading on: the two-region design was built to prevent failures, and it caused more than it stopped. How would you have spent the money instead?*

Camille went back to what had actually hurt users over two years and sorted the outages by cause. Region failures were a tiny fraction. Bad deploys, expired credentials, and slow recovery were most of it. So she shifted the effort. The second region stayed only for the scheduling data hospitals truly couldn't lose, as a standby rather than live. The rest went into making deploys small and quick to undo, automatic renewal and alerts for every certificate and key, and practising recovery until restoring service took minutes rather than an hour. She also persuaded the CEO to agree different targets for different features. Booking an appointment got 99.99%. The monthly reports page got 99.5%.

The next year was the most reliable the company had had, and cheaper than the year before.

Looking back, Camille thought the contract had asked for a number and she'd bought machinery. What users felt was how often things broke and how quickly they came back, and most of that came down to ordinary discipline, not a second region.

## Where it shows up

| Page | The cost | What it bought |
| --- | --- | --- |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Zero failure would have meant no deploys and two of everything | Rosa's target of 99.9% left a budget to spend on shipping. |
| [Queueing](../latency/queueing.md) | Spare capacity, paid for and mostly idle | Short waits when traffic clumps. |
| [Replication](../data/replication.md) | A replica for every primary, and the failover logic around it | Survival when a machine dies, and new failure modes like split brain. |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Every extra copy, region and standby is on the bill | Availability, at a price someone should choose on purpose. |

It shows up elsewhere too: backup systems, on-call rotations, redundant network links, and the extra review steps on risky changes.

What these share is diminishing returns: the first nine is cheap, the fourth is very expensive, and the money is often better spent on recovering quickly than on never failing.

## It really happened

Camille is fictional; her finding is well known. Google's site reliability engineers wrote that improving reliability has sharply diminishing returns, with each increment costing far more than the last, which is why they set targets below 100% and treat the gap as a budget ([*Site Reliability Engineering*, "Embracing Risk"](https://sre.google/sre-book/embracing-risk/) <!-- verify -->). Large cloud outages regularly show the other side. When a major region has a bad day, many services that assumed a single region go down with it, and the companies decide afterwards, with numbers, whether a second region is worth its cost.

## What it is

Reliability is bought with redundancy, spare capacity, careful process and people's time, and each additional nine of availability costs roughly an order of magnitude more than the last. Complexity added for redundancy, such as failover, replication and multi-region designs, brings its own failures. Good spending starts from what actually causes outages and what users actually notice, sets targets per feature, and favours fast detection and recovery over trying never to fail.

## Where it gets misapplied

- **Promising nines without pricing them.** Camille's CEO and the four minutes a month.
- **Redundancy against the wrong failure.** A second region doesn't help with bad deploys, which are the common cause.
- **One target for everything.** A report page held to the same standard as the payment flow.
- **The mirror:** no redundancy at all for data that can't be recreated. Some things are worth the second copy.

## Connections

- Learning this is also learning [replication](../data/replication.md), because replicas are the most common reliability purchase, and they bring their own failures.
- Learning this is also learning [queueing](../latency/queueing.md), because spare capacity is what keeps waits short, and it's paid for whether used or not.
- Learning this is also learning [reading a cloud bill](cloud-bills.md), because every copy and standby is a line on it.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because availability targets are only meaningful when measured the way users experience them.
- Learning this is also learning [CI pipelines](../tooling/ci.md), because small, easily undone deploys prevent more outages than most redundancy.

## Resources

1. Google, [*Site Reliability Engineering*](https://sre.google/sre-book/table-of-contents/), chapter 3, "Embracing Risk" (start here). <!-- verify -->
2. Google, *The Site Reliability Workbook*, on implementing targets (go deeper).
3. Public post-incident reports from cloud providers (reference: what actually takes things down).

## Names you'll hear

- **Nines:** 99.9%, 99.99% and so on, the shorthand for availability.
- **Redundancy:** spare components ready to take over.
- **Active-active, active-passive:** both copies serving at once, or one on standby.
- **MTTR:** mean time to recovery, how long it takes to come back.
- **Blast radius:** how much is affected when something fails.

## Go and look

List the last five outages of something you run and their causes. Then ask which of them the most expensive reliability feature you have would actually have prevented.
