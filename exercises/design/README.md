# System design exercises

Design cases, two for each kind of system. Each one gives a situation, requirements and rough numbers, and the questions from [how to approach a design](../../design/approach.md) that matter most for it. Then it shows the tempting first design and where it breaks, gives three hints, and hides two defensible designs with what each one costs. It ends by asking what breaks at ten times the size. There's no single right answer to a design case. The point is to see the trade-offs and to know which numbers decide between them.

Work through the case yourself before opening anything: write down the numbers, sketch a design, and find its weakest point. Then open the hints one at a time.

| Kind of system | Cases |
| --- | --- |
| Feeds and fan-out | [The final whistle](social-feed.md) (a social feed with very large accounts); a live leaderboard for a global game |
| Writes at volume | [Every click, once](ad-click-counter.md) (an ad-click counter that bills); a metrics and monitoring system |
| Real-time messaging | [The school's messages](group-chat.md) (group chat with receipts); a document several people edit at once |
| Money that must be exact | [The tutors' wages](payments-ledger.md) (a payments ledger); a flash ticket sale that must never oversell |
| Search | Search-as-you-type suggestions; a web crawler |
| Location and matching | Ride-hailing dispatch; "places near me" search |
| Large media | Video upload and streaming; file sync across devices |
| Coordination | A rate limiter shared by many servers; a job scheduler for millions of timed tasks |

Cases without a link are still to be written.

## Which ideas each case exercises

Every page in [system design](../../design/README.md) is exercised by at least one case, so that the set as a whole covers the main ideas of distributed systems.

| Idea | Cases |
| --- | --- |
| [Estimates](../../design/estimates.md) | All of them; [the final whistle](social-feed.md) turns on it |
| [Load balancing](../../design/load-balancing.md) | [The school's messages](group-chat.md); ride-hailing dispatch; video streaming |
| [Rate limiting and backpressure](../../design/rate-limiting.md) | A shared rate limiter; [the school's messages](group-chat.md); a web crawler |
| [Idempotency](../../design/idempotency.md) | [The tutors' wages](payments-ledger.md); [every click, once](ad-click-counter.md); [the school's messages](group-chat.md) |
| [Timeouts and circuit breakers](../../design/timeouts.md) | [The tutors' wages](payments-ledger.md); a web crawler; ride-hailing dispatch |
| [Consensus and leader election](../../design/consensus.md) | A job scheduler; a flash ticket sale |
| [Sagas](../../design/sagas.md) | [The tutors' wages](payments-ledger.md); a flash ticket sale |
| [Asynchronous work](../../design/async-work.md) | [The school's messages](group-chat.md); video upload; a web crawler |
| [Batch or stream](../../design/batch-or-stream.md) | [Every click, once](ad-click-counter.md); metrics and monitoring |
| [Time and ordering](../../design/time-and-ordering.md) | [The school's messages](group-chat.md); a shared document; file sync |
| [Service boundaries](../../design/service-boundaries.md) | Ride-hailing dispatch; video upload and streaming |
| [Replication](../../data/replication.md) and [consistency](../../data/consistency.md) | File sync; a shared document; a live leaderboard |
| [Partitioning](../../data/partitioning.md) | [Every click, once](ad-click-counter.md); [the final whistle](social-feed.md); "places near me" |
| [Caching](../../performance/caching.md) | [The final whistle](social-feed.md); search-as-you-type; video streaming |
