# Queues

Last reviewed: 2026-10-24

A concept page: the data structure behind waiting in line, and the rules for who goes next.

## Problem

When work arrives faster than it can be done, it has to wait somewhere, in some order. First come, first served is the obvious rule, and it feels fair. But it treats a two-second job and a two-hour job the same, and an urgent request the same as a routine one.

## The story

In 2013 Yusuf Adeyemi ran the infrastructure for a company that sent email on behalf of other businesses: receipts, password resets, newsletters. Every email to be sent went into one queue, and a pool of workers took emails off the front and sent them, first in, first out. It was simple, it was fair, and it never lost anything.

On a Tuesday morning a large retailer scheduled its weekly newsletter, two million emails, and they went into the queue in one go. Behind them, over the next three hours, went every password reset and every order receipt from every other customer. A person who'd forgotten their password clicked "reset" and waited. And waited. The workers were going as fast as ever; they were just working through two million newsletters first. By the time Yusuf noticed, the support inboxes of thirty customers were full of people asking where their reset emails were.

The queue had done exactly what it was built to do. First in, first out had been fair to the order emails arrived in, and unfair to everyone waiting for something that mattered right now.

*Before reading on: every email was handled in the order it arrived, and the urgent ones waited hours. How would you have arranged the line?*

Yusuf split the one queue into three: one for messages a person was actively waiting for, like password resets and two-factor codes, one for receipts and notifications, and one for bulk mail. Workers always took from the urgent queue first, then the next, and only then from bulk. That fixed the resets, and created a new worry, that bulk mail might never be sent if urgent mail kept arriving. So bulk was guaranteed a share of the workers whatever else was happening. And within bulk, each customer had their own line, served in turn, so one retailer's two million emails couldn't hold up another's ten thousand.

Looking back, Yusuf thought "fair" had been the wrong word for what he'd built. First in, first out was fair to the queue. What people needed was fairness to the people waiting, which meant deciding who goes next on purpose.

## Where it shows up

| Page | The queue | The rule for who goes next |
| --- | --- | --- |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | Jobs waiting for the processor | The scheduler, with a clock so no job can keep the processor forever. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Packets in a router's buffer | First in, first out, until the buffer fills and packets are dropped. |
| [8, Too many users, too much data](../08-too-many-users-too-much-data.md) | Feed updates behind the champion's post | One huge job at the front held up everyone, Yusuf's newsletter at a different scale. |
| [Queueing](../latency/queueing.md) | Every line, anywhere | How long the wait is depends on how busy the server is; this page is about the order. |

It shows up elsewhere too: message brokers between services, print queues, breadth-first search in graphs, and the "please hold" line at a call centre.

What these share is two separate decisions: the order of the line, and what happens when it's full. First in, first out is a fine default, but most real systems need priorities, limits, and a guarantee that nothing waits forever.

## It really happened

Yusuf is fictional; his fix is very old. MIT's time-sharing system, CTSS, used a *multilevel feedback queue* in the early 1960s: several queues at different priorities, with short interactive jobs served first and long-running jobs moved to lower-priority queues, so people at terminals got quick responses while big jobs still finished ([summary](https://en.wikipedia.org/wiki/Multilevel_feedback_queue)). Operating systems have used variations ever since. Email and messaging services now commonly separate transactional mail from bulk mail for the reason Yusuf found.

## What it is

A queue is a data structure where items are added at one end and removed from the other: first in, first out. A priority queue removes the most important item first instead, usually built on a heap. Real systems combine them: several queues with rules for which to serve, limits on how long each can grow, and guarantees that low-priority work still gets done.

## Where it gets misapplied

- **One queue for everything.** Urgent and bulk work in the same line, so the urgent waits for the bulk.
- **Strict priority with no floor.** Low-priority work that never runs while higher-priority work keeps arriving, called starvation.
- **Unbounded queues.** A queue with no limit hides overload until it runs out of memory ([queueing](../latency/queueing.md)).
- **The mirror:** an elaborate priority scheme for a queue that's never more than a few items long. If it drains in a second, first in, first out is fine.

## Connections

- Learning this is also learning [queueing](../latency/queueing.md), because how long a line gets depends on how busy the server is, whatever the order.
- Learning this is also learning [graphs](graphs.md), because breadth-first search is a queue of places to visit next.
- Learning this is also learning [event loops and threads](../runtimes/event-loops-and-threads.md), because an event loop is a queue of ready work and a rule for taking from it.
- Learning this is also learning [round trips](../latency/round-trips.md), because a message queue between services turns waiting for a reply into waiting in line.
- Learning this is also learning [least privilege](../auth/least-privilege.md), because giving each customer their own line is limiting how much of the system any one of them can take.

## Resources

1. Remzi and Andrea Arpaci-Dusseau, [*Operating Systems: Three Easy Pieces*](https://pages.cs.wisc.edu/~remzi/OSTEP/), the scheduling chapters, including the multilevel feedback queue (start here: free). <!-- verify -->
2. Thomas Cormen et al., *Introduction to Algorithms*, the chapters on heaps and priority queues (go deeper).
3. Your message broker's documentation on priorities, limits and dead-letter queues (reference).

## Names you'll hear

- **FIFO:** first in, first out.
- **Priority queue, heap:** a queue that hands out the most important item first, and the structure usually used to build one.
- **Starvation:** low-priority work never getting served.
- **Fair queuing:** taking turns between several lines so none can crowd out the others.
- **Dead-letter queue:** where messages go when they repeatedly fail to be processed.

## Go and look

Find a queue in something you run and check whether everything in it is equally urgent. If it isn't, find out what happens to the urgent items when a big batch arrives.
