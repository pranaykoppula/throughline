# Queueing

Last reviewed: 2026-10-24

A concept page: why waiting, not working, is where time goes, and why it gets worse suddenly.

## Problem

Whenever work arrives faster than it can be handled, even briefly, it waits. Most slowness people experience is waiting in a line they can't see. And the line doesn't grow steadily as a system gets busier: it stays short for a long time and then explodes.

## The story

In 1912 Signe Holm supervised the operators at a telephone exchange in Copenhagen. Callers lifted the receiver, a lamp lit on the switchboard, and an operator answered and connected them. When every operator was busy, callers waited, listening to silence.

The company's directors wanted costs down, and operators were the largest cost. Signe's numbers showed her operators were busy about seventy percent of the time. Thirty percent idle seemed wasteful, so she cut the evening shift from ten operators to eight. On paper, the remaining eight would now be busy close to ninety percent of the time, still with room to spare.

The complaints arrived within a week. At seventy percent, callers had barely waited at all. At ninety, some waited a minute or more, and in the busiest half hour many hung up and tried again, which made the line longer still. The operators weren't working slower. Nothing had changed except two empty chairs. A twenty-point rise in how busy they were had turned seconds of waiting into minutes.

*Before reading on: the operators were busier, but not overloaded. Why did the waiting get so much worse, so fast?*

A young mathematician at the company was working on exactly this question, and he showed Signe why. Calls didn't arrive evenly; they came in clumps, at random. When operators had slack, a clump was absorbed in moments. When they were nearly always busy, each clump piled up behind the last, and the queue had no time to drain before the next one arrived. As operators got close to fully busy, the waiting didn't rise in a straight line. It climbed steeply, towards infinity. Signe put the two operators back, and she never again judged a switchboard by how busy it looked.

Looking back, Signe thought the lesson was to stop treating idle time as waste. Some slack was what kept the waiting short. A system run at close to full capacity doesn't save money; it just moves the cost to the people waiting.

## Where it shows up

| Page | The queue | What it taught |
| --- | --- | --- |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | Jobs waiting for the processor, and the processor waiting for tape drives | Ruth's machine was mostly idle because programs queued on slow devices. Waiting, not computing, was where time went. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Packets in routers' buffers | When buffers filled, packets were dropped, senders retried into the queue, and the network collapsed. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Feed updates behind the champion's 1.8 million writes | Nothing failed. Everyone's update waited behind one enormous job. |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Checkouts waiting on a slow payment provider | The site was up; requests waited until they timed out. Waiting is how most outages start. |

It shows up elsewhere too: thread pools, connection pools, message queues, and every "please hold" on a phone line.

The pages show three lessons. Things get slow near full capacity long before they break, as with Signe and Maya. Retrying into a full queue makes it worse, which is why page 5 needed backoff. And a queue needs a limit and a timeout, because an unbounded one turns overload into waiting forever, as Rosa found.

## It really happened

Signe is fictional; the mathematician wasn't. Agner Krarup Erlang joined the Copenhagen Telephone Company in 1908 and published the first paper on what became queueing theory in 1909. His 1917 formulas for waiting and lost calls were adopted by telephone companies across the world ([MacTutor](https://mathshistory.st-andrews.ac.uk/Biographies/Erlang/)). In 1961 John Little proved a simple rule that holds for almost any queue: the average number waiting equals the arrival rate times the average time each one waits. The same mathematics now sizes server pools, call centres, and the buffers in every router.

## What it is

A queue forms whenever work arrives faster than it's served, even for a moment. Because arrivals clump, waiting time rises sharply as a server approaches full use: a server busy half the time keeps queues short, and one busy ninety-five percent of the time can keep people waiting many times longer. Latency is mostly time in queues. Keep slack, put limits and timeouts on every queue, and back off rather than retry into a full one.

## Where it gets misapplied

- **Running at "full efficiency".** Ninety-five percent utilisation looks thrifty on a dashboard and feels terrible to users.
- **Unbounded queues.** They don't remove overload; they hide it until memory runs out or requests time out.
- **Averages.** The average wait can look fine while the unluckiest tenth of requests wait seconds ([percentiles](../math/percentiles.md)).
- **The mirror:** so much slack that nothing is ever used. Headroom is a cost too; choose it on purpose.

## Connections

- Learning this is also learning [queues](../dsa/queues.md), because the data structure is the same line, in memory.
- Learning this is also learning [round trips](round-trips.md), because each hop on the network is a place to wait.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because queues punish the tail, and the average hides it.
- Learning this is also learning [the cost of reliability](../cost/reliability.md), because slack is capacity you pay for and hope not to need.
- Learning this is also learning [consistency](../data/consistency.md), because asking the one owner of some data means queueing for it.

## Resources

1. Marc Brooker's blog posts on queueing and backoff (start here: short, practical, by an engineer who runs large systems).
2. Neil Gunther, *Guerrilla Capacity Planning* (go deeper).
3. Mor Harchol-Balter, *Performance Modeling and Design of Computer Systems* (reference: the mathematics, readably).

## Names you'll hear

- **Utilisation:** the fraction of time a server is busy.
- **Little's law:** number waiting = arrival rate × time waiting.
- **Erlang:** the unit of telephone traffic, and the name of a programming language built at Ericsson, both after him.
- **Backpressure:** a full queue telling senders to slow down instead of silently growing.
- **Head-of-line blocking:** everyone stuck behind one slow item, like Maya's feed behind the champion.

## Go and look

Find a queue in something you run, a job queue, a thread pool, a connection pool, and look at how long it is at the busiest time of day, not the average. Then find out what happens when it's full.
