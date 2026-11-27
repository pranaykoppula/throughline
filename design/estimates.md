# Back-of-the-envelope estimates

Last reviewed: 2026-11-27

A concept page: a few known numbers, multiplied together and rounded hard, tell you whether a design can work before anyone builds it. The skill isn't arithmetic. It's knowing which number to estimate: the total, the average or the peak.

## Problem

Every design rests on numbers nobody has measured yet: how many people, how often, how much data, how fast it grows. Waiting to measure means building first and finding out later, which is the expensive way round. Guessing without arithmetic means arguing about adjectives, "big", "a lot", "fast enough". A rough calculation, done in a few minutes from numbers you can defend, settles most of those arguments. It goes wrong in one familiar way: the right sum about the wrong quantity.

## The story

In 2016 Nkechi Eze was the first back-end engineer at a small company in Manchester that made video doorbells. When someone pressed the button or walked up the path, the doorbell recorded a short clip and uploaded it, so the owner could watch it on their phone. The company was about to ship its first big batch, and Nkechi had to decide how much upload capacity and storage to rent.

She did what she'd been taught, on the back of a printout. Forty thousand doorbells. From the test homes, about twelve clips a day each, at about three megabytes a clip. That made about 1.4 terabytes a day. Kept for thirty days, about 43 terabytes of storage. Spread over the 86,400 seconds in a day, the uploads came to about 17 megabytes a second. She knew traffic wasn't spread evenly, so she rented upload servers for three times that, about 50 megabytes a second, and wrote the numbers on the team's wiki. It was a careful estimate, and every multiplication in it was right.

For seven months it was fine. Then came the evening of 31 October. Between six and eight o'clock, across the whole country at once, children in costumes walked up garden paths and rang doorbells. Every ring was a clip. Uploads climbed to about twenty-five times the daily average and stayed there for two hours. The upload servers filled their queues, the doorbells timed out and retried, and by seven o'clock most clips were failing altogether. Hundreds of customers' phones showed a notification with no video behind it. The storage, sized from the daily total, had room to spare all night.

*Before reading on: every number in Nkechi's estimate was right. What had she estimated that the upload servers didn't care about?*

Nkechi saw that she'd answered two different questions with one number. Storage cared about totals: how many bytes, kept for how long. Her daily figure was exactly right for that, and the storage never came close to running out. Upload capacity cared about the busiest minutes, and an average over a day had hidden them completely. A doorbell's day wasn't random. It followed people's days: quiet at night, busier when people left for work and came home, busiest when visitors called. And everybody's evening happened at the same time, because the doorbells were all in one time zone. Halloween was the extreme, but every weekday evening ran at about three times the average, which was where her "three times" had come from by luck.

She kept the method and changed what she estimated. For anything that had to keep up in real time, she estimated the peak, as the average times a peak factor, and found the factor from the shape of the users' days and the calendar: Halloween, Bonfire Night, the week before Christmas when parcels arrived. She stopped making the upload servers big enough for the worst evening of the year. Instead, a doorbell that couldn't upload kept the clip on its own memory card, sent the owner a still picture straight away, which was tiny, and uploaded the video later, when the evening was over. The peak was spread into the night. And she wrote the assumptions next to the numbers, so that next October someone could check them.

![A line chart of clip uploads through a day, as multiples of the daily average. An ordinary weekday rises from almost nothing at night to about three times the average in the evening. On Halloween the evening climbs to about twenty-five times the average between six and eight o'clock. A dashed line at three times the average marks the upload capacity Nkechi rented, which the Halloween evening exceeds for two hours.](../images/figures/design-estimates.svg)

*The daily total was right for storage. Only the shape of the day showed what the upload servers would face.*

Looking back, Nkechi thought the estimate had done its job: it told her, in an afternoon, that the design was roughly the right size. What it couldn't do was tell her which number mattered, and that was the part she'd skipped. Totals decide what you store and what you pay; peaks decide whether it works.

## Where it shows up

| Page | The estimate | What it taught |
| --- | --- | --- |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Maya's fifty reads for every write | One ratio, counted, decided the whole design: precompute the feeds. And the champion's 1.8 million followers showed that the biggest user, not the average one, sets the cost. |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Tariq's cloud bill | He expected compute at the top and found data transfer. An estimate of the bill before building would have shown it. |
| [Latency numbers](../performance/latency-numbers.md) | The cost of a memory read, a disk seek, a round trip | These are the numbers most system estimates are built from. |
| [Queueing](../performance/queueing.md) | Signe's operators, busy seventy percent of the time | Capacity can't be sized to the average load; waiting explodes near full use, so an estimate has to leave slack. |
| [Distributions and percentiles](../math/percentiles.md) | An average that described nobody | Peaks and tails are where things fail, and averages hide both. |

It shows up elsewhere too: electricity grids planning for the moment a popular television programme ends and a million kettles go on, restaurants staffing for Saturday night rather than the week's average, a footbridge designed for the crowd leaving a match, and the physics student asked how many piano tuners there are in a city.

What the rows share is a habit: before designing, multiply a few numbers you can defend, round them hard, and then ask which of them the design is sensitive to. The arithmetic is easy. Choosing between the total, the average and the peak is the judgement.

## It really happened

Nkechi is fictional, and so is her company. Estimates like hers are standard practice. At the Trinity test in July 1945, Enrico Fermi dropped small pieces of paper before, during and after the blast wave reached him, watched how far they were carried, and estimated the explosive yield at about ten kilotons of TNT. Later analyses put it at about 25 kilotons: wrong by a factor of between two and three, from paper and a pace count, which was the point ([Katz, "Fermi at Trinity"](https://arxiv.org/abs/2103.05784)). Estimation questions are still called Fermi problems.

In a 2009 keynote, Jeff Dean of Google showed back-of-the-envelope calculations as a design tool. One compared two ways of producing a page of thirty image thumbnails: reading the images one after another took about 560 milliseconds, mostly disk seeks, and reading them in parallel about 18 ([Dean's LADIS 2009 slides](https://www.cs.cornell.edu/projects/ladis2009/talks/dean-keynote-ladis2009.pdf)). The same talk carried the list of latency numbers that [latency numbers](../performance/latency-numbers.md) is about.

Peaks that line up with people's habits are well documented outside computing. Britain's electricity grid records a "TV pickup" when a popular programme ends and viewers switch on kettles at the same moment. The largest on record followed the penalty shoot-out in England's 1990 World Cup semi-final against West Germany, a surge of about 2,800 megawatts ([BBC](https://www.bbc.co.uk/news/articles/cx2124ly83po)).

## What it is

A back-of-the-envelope estimate multiplies a few rough numbers, such as users, actions per user, size per action and seconds in a day, to get the order of magnitude of a load, a store or a bill. Useful conventions: round to one significant figure, keep powers of ten visible, and use a day of about 100,000 seconds. Three quantities come out of the same inputs and answer different questions. The **total** sizes storage and the bill. The **average** rate is rarely what anything has to survive. The **peak** rate, the average times a peak factor, sizes anything that must keep up live. List the multipliers people forget, such as copies kept for safety, indexes, retries and growth, and write the assumptions down so the estimate can be checked later.

## Where it gets misapplied

- **Sizing live capacity from an average.** Nkechi's Halloween, and most capacity incidents on a predictable day.
- **False precision.** An estimate quoted to four figures invites people to trust the fourth; the inputs never justified the second.
- **Estimating once.** The numbers drift as users and habits change, and nobody rechecks the assumptions.
- **The mirror:** refusing to build until everything is measured. Some numbers can only be learned from users, and an estimate's job is to show whether the design is roughly the right size, not to replace measurement.

## Connections

- Learning this is also learning [latency numbers](../performance/latency-numbers.md), because estimates are built from known costs, and those are the ones to know.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because the peak and the tail are what fail, and an average describes neither.
- Learning this is also learning [queueing](../performance/queueing.md), because capacity sized to the expected load leaves no slack, and waiting grows without limit near full use.
- Learning this is also learning [growth](../dsa/growth.md), because the most important estimate is often what happens at ten times the size.
- Learning this is also learning [reading a cloud bill](../economics/cloud-bills.md), because the total is also a price, and the bill is an estimate you can check.
- Learning this is also learning [rate limiting and backpressure](rate-limiting.md), because Nkechi's fix was to refuse the peak politely and finish the work later.
- Learning this is also learning [how to approach a design](approach.md), because putting numbers on a design is its second step.

## Resources

1. Jeff Dean, ["Designs, Lessons and Advice from Building Large Distributed Systems"](https://www.cs.cornell.edu/projects/ladis2009/talks/dean-keynote-ladis2009.pdf) (2009) (start here: the slides on back-of-the-envelope calculations).
2. Jon Bentley, *Programming Pearls*, the column "The Back of the Envelope" (short and practical).
3. Lawrence Weinstein and John Adam, *Guesstimation* (go deeper: estimation as a skill, outside computing).
4. Martin Kleppmann, *Designing Data-Intensive Applications*, chapter 1 (reference: describing load and performance with percentiles, not averages).

## Names you'll hear

- **Back-of-the-envelope, Fermi estimate:** a rough calculation from a few defensible numbers.
- **Order of magnitude:** the power of ten, which is what an estimate is for.
- **Peak-to-average ratio, peak factor:** how much busier the busiest moment is than the average.
- **QPS, RPS:** queries or requests per second.
- **Headroom:** capacity kept above the expected peak.
- **Capacity planning:** estimating ahead what you'll need, and when.

## Go and look

Pick something you run and find its busiest hour of the past year. Divide its requests in that hour by the average hour. That number is your peak factor, and it's worth knowing before the next design meeting.
