# Event loops and threads

Last reviewed: 2026-10-24

A concept page: the ways a program does several things at once, and the bugs each way invites.

## Problem

Most programs have to handle several things at the same time: many users, many requests, a screen that must stay responsive while work goes on. Threads let several lines of work run at once and share memory, which makes them powerful and easy to get subtly wrong. Event loops avoid most of that by doing one thing at a time very quickly, and fail in their own way when one thing takes too long.

## The story

In 2014 Omar Haddad built the backend for a concert ticketing app in Python. Each incoming request was handled by its own thread, so a slow request didn't hold up the others. It was the standard design for the framework he used, and it worked.

During a big on-sale, the count of remaining tickets went wrong. The venue had 2,000 seats and the app sold 2,047. Omar found the cause after a long night. Two threads would read the count, say 15, at almost the same moment. Each subtracted one and wrote back 14. Two tickets were sold and the count fell by one. It happened rarely, only when requests arrived within microseconds of each other, which at an on-sale was all the time.

His fix was a lock: only one thread at a time could touch the ticket count. The overselling stopped. Then, at the next on-sale, the app slowed to a crawl. Every request needed the lock for a moment, and some held it while they waited on the payment provider. Hundreds of threads queued behind one lock, each mostly waiting. The app had threads to do things in parallel, and the lock had made it do them one at a time, slowly.

*Before reading on: threads sharing a counter oversold tickets, and a lock to fix it made everything wait. How would you have restructured it?*

Omar separated the two kinds of work. The requests were mostly waiting, on the database and on the payment provider, so he moved them to an event loop: a single thread that started each piece of work, set it aside while it waited, and picked up whatever was ready next. Thousands of requests could wait at once without thousands of threads. The ticket count left the application altogether. It moved to the database, decremented in one atomic operation that refused to go below zero, so no two requests could ever both take the last seat. The one genuinely heavy task, generating PDF tickets, went to a separate pool of worker processes, so it couldn't block the loop.

The event loop brought its own lesson a month later. A developer added a function that resized uploaded profile photos directly in a request handler. Each resize took two seconds of computation, and during those two seconds the loop could do nothing else, so every other user waited. It was moved to the worker pool, and Omar wrote a rule on the team wiki: nothing slow runs on the loop.

Looking back, Omar thought each model came with a different danger. Threads shared memory, so the danger was two of them changing the same thing at once. The event loop shared time, so the danger was one piece of work never letting go. Choosing between them was really choosing which danger to guard against.

## Where it shows up

| Page | The model | Its failure |
| --- | --- | --- |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | Many jobs sharing one processor | A job that never waits keeps the processor; jobs grabbing shared drives in different orders deadlock. |
| [Queues](../dsa/queues.md) | An event loop's list of ready work | One slow item at the front holds up everything behind it. |
| [6, Anyone can publish](../06-anyone-can-publish.md) | JavaScript in the browser, a single event loop | A long script freezes the page. |
| [Queueing](../latency/queueing.md) | Threads waiting for a lock | A queue at the slowest point, invisible until it's long. |

It shows up elsewhere too: user interfaces that freeze while saving, databases handling concurrent transactions, and every server framework's choice of how to handle requests.

What these share is that doing several things at once always means sharing something, memory or time, and every bug here comes from that sharing.

## It really happened

Omar is fictional; his bug is the classic race condition, and its worst real example is grim. Between 1985 and 1987 the Therac-25 radiation therapy machine gave several patients massive overdoses, some fatal. Investigators Nancy Leveson and Clark Turner found that one cause was a race condition: if an operator edited the treatment settings quickly enough, the software's separate tasks fell out of step and the machine fired at full power without its safety shield in place (Leveson and Turner, "An Investigation of the Therac-25 Accidents", *IEEE Computer*, 1993). Earlier models had hardware interlocks that caught such errors; this one relied on software alone. On the event-loop side, Node.js's own guide is built around Omar's second rule ([Node.js, "Don't Block the Event Loop"](https://nodejs.org/en/guides/dont-block-the-event-loop)).

## What it is

Threads are separate lines of execution sharing one program's memory; they suit work that computes in parallel, but any shared data must be protected, usually with locks, which bring their own risks of contention and deadlock. An event loop is a single thread that runs short pieces of work in turn, switching whenever one would wait; it suits work that mostly waits on input and output, but any long computation blocks everything. Processes are separate programs with separate memory, safer and heavier. Most real systems combine them.

## Where it gets misapplied

- **Shared mutable state between threads.** Omar's ticket count. Keep shared state to a minimum, or move it somewhere built for concurrency, like a database.
- **A lock held while waiting.** Holding a lock across a network call turns parallelism into a queue.
- **Heavy computation on an event loop.** The photo resize. Push it to workers.
- **The mirror:** asynchronous code everywhere, for programs with nothing to wait on. It adds complexity and saves nothing ([page 2](../02-one-machine-many-programs.md)).

## Connections

- Learning this is also learning [queues](../dsa/queues.md), because an event loop is a queue of ready work.
- Learning this is also learning [queueing](../latency/queueing.md), because a contended lock is a queue, and queues near capacity explode.
- Learning this is also learning [graphs](../dsa/graphs.md), because deadlock between threads is a cycle in who waits for whom.
- Learning this is also learning [JavaScript](javascript.md), because the browser's single event loop shaped how the whole language handles concurrency.
- Learning this is also learning [state machines](../dsa/state-machines.md), because making each change one allowed move, applied atomically, is how shared state stays valid.

## Resources

1. Remzi and Andrea Arpaci-Dusseau, [*Operating Systems: Three Easy Pieces*](https://pages.cs.wisc.edu/~remzi/OSTEP/), the concurrency part (start here: free). <!-- verify -->
2. Node.js, ["Don't Block the Event Loop (or the Worker Pool)"](https://nodejs.org/en/guides/dont-block-the-event-loop) (go deeper: the event loop's one rule).
3. Leveson and Turner, "An Investigation of the Therac-25 Accidents" (*IEEE Computer*, 1993) (reference: why concurrency bugs matter).

## Names you'll hear

- **Thread, process:** a line of execution sharing memory, and a program with its own.
- **Race condition:** a result that depends on the timing of concurrent work.
- **Lock, mutex:** a way to let only one thread at a time into a piece of code.
- **Atomic operation:** one that happens all at once, with no half-done state visible.
- **Event loop, async/await:** one thread switching between tasks as they wait, and the syntax that makes it read like ordinary code.
- **GIL:** Python's global interpreter lock, which limits threads running Python code to one at a time.

## Go and look

Find one piece of shared state in something you've built, a counter, a cache, a balance, and work out what happens if two requests change it at the same moment. Then find out what actually stops that.
