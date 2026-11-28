# Load balancing

Last reviewed: 2026-11-27

A concept page: spreading requests across many servers so that none is overwhelmed while others sit idle. Every rule for choosing a server reads some sign of how busy or healthy it is, and a server can look like the best choice for exactly the wrong reason.

## Problem

Once one server isn't enough, there are several, and something has to **decide** which one gets each request. Sending them in turn is simple and fair if every request costs the same, but they don't. Sending each to the least busy server is cleverer, but "least busy" has to be judged from outside, from signs such as open connections or response times, and the judging is done thousands of times a second without anyone looking. When a server's signs stop meaning what they used to, the balancer keeps obeying them.

## The story

In 2012 Tomasz Wójcik ran the search service for an online travel agency in Kraków. Customers typed in a journey, and twenty identical servers worked out the fares, behind a load balancer that handed out requests in turn. Most searches took about 200 milliseconds. A few, multi-city trips with flexible dates, took several seconds, and when two or three of those landed on the same server, the ordinary searches queued behind them while the server next door sat idle.

Tomasz switched the balancer to *least connections*: each new request went to the server with the fewest requests in progress. It was the textbook fix, and it worked. A server stuck on a long search had more open connections, so new searches went elsewhere. The slowest searches got quicker, the servers' load evened out, and for a year he didn't think about it again.

Then one Thursday evening, a server's connection to the fares cache broke. It didn't crash. It answered every search, instantly, with an error page: two milliseconds instead of two hundred. Because it finished so quickly, it always had the fewest open connections, so the balancer sent it more searches than anyone else, which it failed just as quickly. Within ten minutes about sixty percent of all searches were going to that one server out of twenty. The balancer's health check, which asked each server once every ten seconds whether it was listening, said all twenty were fine. The customer error rate went from almost nothing to more than half.

*Before reading on: the balancer did exactly what it was told. What was it trusting that had stopped being true?*

Tomasz saw that the balancer had been reading two signs, and both had drifted. *Few open connections* was meant to mean *has spare capacity*, and for a year it had; but a server that failed fast had few connections because it wasn't doing the work. *Answers the health check* was meant to mean *can serve customers*, and it only meant the process was alive. Least connections had made the problem worse than doing nothing: round robin would have sent the broken server one search in twenty.

He changed both. The health check now ran a real search against a known journey and checked the answer, and the balancer also watched the real traffic: a server whose error rate was far above its neighbours' was taken out of rotation for a while, whatever it said about itself. And he replaced least connections with a rule he found in a paper from the 1990s: for each request, pick two servers at random, and send it to the one with fewer connections. It kept nearly all the benefit, since a server stuck on long searches still lost most comparisons. But a server could now win only when it happened to be one of the two picked, about one request in ten. A broken server that looked perfect could attract at most twice its fair share, not most of the traffic.

![A bar chart of the share of searches sent to the one broken server, out of twenty. Round robin: five percent, its fair share. Least connections: about sixty percent, because failing fast made it look the least busy. Two random choices: about ten percent at most, because it can only win when it's one of the two picked.](../images/figures/design-load-balancing.svg)

*The broken server looked like the best choice. Two random choices limit how much any one server can attract, however good it looks.*

Looking back, Tomasz thought least connections had been the right idea with too much trust in it. Every balancing rule reads some sign of how a server is doing. The better rules still work when one of those signs is lying.

## Where it shows up

| Page | The balancing | What it taught |
| --- | --- | --- |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Rosa's green squares | A check that asks whether a machine is on isn't a check that customers can buy a ticket. Tomasz's health check asked the same wrong question. |
| [Queueing](../performance/queueing.md) | Signe's callers, one line in front of many operators | One shared line in front of many servers keeps waiting short; separate lines let one slow customer hold up everyone behind them, which is what round robin did to Tomasz's searches. |
| [Partitioning](../data/partitioning.md) | Choosing which machine holds each key | When the same key must always reach the same server, balancing becomes placement, and consistent hashing keeps most keys where they were when servers come and go. |
| [Sampling and observation](../info/observation.md) | Kofi's sensors, silent over a weekend | A monitor reports what it was built to see; silence and speed can both be signs of failure. |
| [Greedy algorithms](../dsa/greedy.md) | Always taking the step that looks best now | Least connections is greedy: it takes the best-looking server every time, which is exactly what a misleading sign exploits. |

It shows up elsewhere too: the single snaking queue at a post office or airport security instead of a line per desk, a hospital emergency department sending patients to whichever team can take them, electricity grids sharing demand between power stations, and DNS answering with different addresses for the same name.

What the rows share is that the balancer can't see load or health directly. It reads a sign of them, and a rule that trusts one sign completely will, sooner or later, send everything to the server whose sign is wrong.

Motif: [the sign drifts from the thing](../motifs.md#the-sign-drifts-from-the-thing).

## It really happened

Tomasz is fictional, and so is his travel agency. The failure is well known. Amazon's guide to health checks describes a bug that left a few servers in a large fleet producing blank error pages much faster than healthy servers produced real ones; the load-balancing technology of the time favoured fast servers, so it sent them a disproportionate share of traffic. It names the general pattern: a failing server often fails quickly, and rules such as "least requests" turn it into a black hole that attracts more work than its healthy neighbours ([Amazon Builders' Library, "Implementing health checks"](https://aws.amazon.com/builders-library/implementing-health-checks/)).

The two-choices rule comes from the mathematics of throwing balls into bins. Yossi Azar, Andrei Broder, Anna Karlin and Eli Upfal showed in 1994 that placing each ball in the emptier of two randomly chosen bins makes the fullest bin dramatically less full than choosing one bin at random, and Michael Mitzenmacher's 1996 doctoral thesis applied it to load balancing ([thesis](https://www.eecs.harvard.edu/~michaelm/postscripts/mythesis.pdf)). Envoy, a widely used proxy, makes it the default for its least-request balancer, and its documentation gives resistance to herding as the reason ([Envoy's load balancers](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers)).

## What it is

A load balancer sits in front of a pool of servers and chooses one for each request or connection. Common rules are round robin (in turn), weighted round robin (in turn, in proportion to capacity), least connections or least requests (fewest in progress), random, and the power of two random choices (the less busy of two picked at random). Hashing a key, such as a user or a session, to a server keeps related requests together, and consistent hashing limits how many keys move when the pool changes. Health checks take servers out of rotation: *active* checks send a test request, and *passive* checks, also called outlier detection, watch real traffic for errors and slowness. Balancing happens at several layers: DNS, network-level balancers that forward connections, and application-level proxies that read each request.

## Where it gets misapplied

- **A health check that only asks whether the process is alive.** It passes for a server that fails every real request.
- **Trusting one sign completely.** Least connections and fastest-response rules send the most work to the server that fails fastest.
- **Taking out too many servers at once.** When every server is overloaded, failing health checks shrink the pool and overload the rest; good balancers stop removing servers past a limit and fail open.
- **Sticky sessions for convenience.** Tying a user to one server makes that server's failure their failure, and makes the pool hard to resize.
- **The mirror:** a clever balancer where a simple one would do. With requests that all cost about the same, round robin is fair, predictable and easy to reason about.

## Connections

- Learning this is also learning [queueing](../performance/queueing.md), because a balancer decides which line each request joins, and one shared line beats many separate ones.
- Learning this is also learning [partitioning](../data/partitioning.md), because sending each key to a fixed server is placement, and consistent hashing is how it survives change.
- Learning this is also learning [sampling and observation](../info/observation.md), because a health check is a monitor, and it reports only what it was built to look at.
- Learning this is also learning [greedy algorithms](../dsa/greedy.md), because always picking the best-looking server is greedy, and greed trusts its measure completely.
- Learning this is also learning [rate limiting and backpressure](rate-limiting.md), because when the whole pool is full, spreading load evenly isn't enough and something has to say no.
- Learning this is also learning [the cost of reliability](../economics/reliability.md), because a pool of identical servers is redundancy, and it only helps if broken ones are noticed.

## Resources

1. Amazon Builders' Library, ["Implementing health checks"](https://aws.amazon.com/builders-library/implementing-health-checks/) (start here: real failures, including fast-failing servers attracting traffic).
2. Google, *Site Reliability Engineering*, ["Load Balancing in the Datacenter"](https://sre.google/sre-book/load-balancing-datacenter/) (go deeper: subsetting, weighted round robin, and how a large fleet does it).
3. Michael Mitzenmacher, Andréa Richa and Ramesh Sitaraman, ["The Power of Two Random Choices: A Survey of Techniques and Results"](https://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf) (reference: the mathematics).

## Names you'll hear

- **Round robin, weighted round robin:** in turn, optionally in proportion to capacity.
- **Least connections, least requests:** the server with the fewest in progress.
- **Power of two choices, P2C:** the less busy of two servers picked at random.
- **Health check, active and passive; outlier detection:** test requests, or watching real traffic, to take broken servers out.
- **Sticky sessions, session affinity:** keeping a user on one server.
- **Layer 4 and layer 7 balancing:** forwarding connections, or reading each request.
- **Fail open:** when every server looks unhealthy, use them all rather than none.

## Go and look

Find the health check behind something you run and read what it actually tests. Then ask what would happen to a server that answered it perfectly while failing every real request, and how long it would stay in rotation.

Practise this: [the school's messages](../exercises/design/group-chat.md), with a million long-lived connections to spread, and [the nearest car](../exercises/design/ride-hailing.md), where position updates must reach the machine that owns their area.
