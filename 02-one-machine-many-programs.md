# 2. One machine, many programs

Last reviewed: 2026-10-24

## Problem

A computer was too expensive to sit idle, and running one program at a time left it idle most of the time. Letting several programs share it meant something had to decide who ran, who waited, and who got which device, and sharing brought new ways for everything to stop.

## The story

Ruth Kowalski ran the night shift at a university computing center in 1963. The machine cost more to rent each hour than she earned in a week, and her job was to keep it busy. Students and faculty handed in their programs as decks of punched cards. Ruth stacked them up, fed them in one at a time, and handed back the printouts in the morning.

One night, out of boredom, she sat with a stopwatch and watched the lights on the console. The processor would flicker furiously for a moment and then go still while a tape drive spun to find the next record, or the printer clattered out a line. Then another flicker, then another wait. She added it up on the back of a job card. The processor was doing useful work about a fifth of the time. The rest of the time the most expensive thing in the building was waiting for the cheapest.

*Before reading on: if the processor spends most of its time waiting on one program's tape drive, what would you have done with that time?*

Her idea was not original, and she knew it. She'd read that the newer machines could keep several programs in memory at once. When one stopped to wait for a device, the machine could switch to another that was ready to run. The center upgraded its operating system to one that did this, and Ruth started loading three or four jobs at a time. The processor's busy lights barely stopped. The pile of finished jobs in the morning was almost three times taller. She was rather pleased with herself.

The first problem arrived within a week. A graduate student's program had a loop that never ended and never asked for a device, so it never stopped to wait. Since programs only gave up the processor when they waited, this one never gave it up. The other three jobs sat in memory, ready, going nowhere, until Ruth noticed at two in the morning and stopped it by hand. The fix, which the operating system's next version added, was a clock. Every fraction of a second it interrupted whatever was running and gave the scheduler a chance to hand the processor to someone else. Nobody could keep it by accident any more.

The second problem was worse, because nothing looked wrong. One night in the spring the machine was running, every light was on, and no job had finished for forty minutes. No error messages, no crashed programs. Ruth went through the console log line by line. One job was holding tape drive 1 and waiting for drive 2. Another was holding drive 2 and waiting for drive 1. Each would let go of its drive when it finished, and neither could finish without the other's drive. They would wait for each other forever, politely, while everything behind them waited too.

She cancelled one of them and the night went on. A week later it happened again with different jobs and the printer. She realised it would keep happening. It wasn't anyone's bad program. It was what happened when programs that each made sense on their own grabbed shared things in whatever order they happened to need them. She'd tripled the work the machine could do by letting programs share it, and in doing so she'd created a way for it to do nothing at all.

She talked it over with one of the systems programmers, who had read a paper about it by a Dutch mathematician. The trap, he explained, needed a circle: A waits for B while B waits for A. Break the circle and the trap can't close. The simplest way to do that was a rule: any job that needed more than one drive had to ask for them in number order, lowest first. A job holding drive 2 could never be waiting for drive 1, because it would have had to ask for drive 1 first. Ruth wrote it on the submission form and refused decks that didn't follow it. The forty-minute silences stopped.

By 1966 the faculty wanted more than overnight results. They wanted to sit at a typewriter terminal, type a line, and get an answer while they were still thinking about the question. The center started running a time-sharing system. It sliced the processor so finely between a few dozen users that each of them felt they had the machine to themselves. Ruth watched it from her desk and saw her stopwatch night again, the other way round. Now the people were the slow device. The machine spent most of each second waiting for someone to finish typing, and in those gaps it could serve everyone else.

Looking back, Ruth thought the lesson of those years wasn't really about tape drives. A machine's resources are shared, so something has to divide them and decide who runs. Sharing means waiting, and the waiting, not the computing, was where nearly all the time went. Every improvement she'd seen had been a better way of filling the waiting with other work, and each one had brought a new way for things to get stuck.

## It really happened

Ruth is fictional; her years weren't. Multiprogramming spread through the 1960s for exactly the reason she timed: processors were expensive and kept waiting on slow devices. MIT's Compatible Time-Sharing System was demonstrated in 1961 and described in 1962, giving interactive users slices of a single machine (Corbató, Daggett and Daley, "An Experimental Time-Sharing System"; [overview](https://history.computer.org/pioneers/corbato.html)). The "Dutch mathematician" was Edsger Dijkstra, who called deadlock the "deadly embrace" and worked out ways to avoid it in the mid-1960s. A 1971 survey by Coffman, Elphick and Shoshani laid out the conditions it needs, including the circular wait that Ruth's numbering rule breaks ("System Deadlocks", *Computing Surveys*).

The same story ran again thirty-five years later. In 1999 Dan Kegel wrote ["The C10K problem"](http://www.kegel.com/c10k.html) <!-- verify -->: web servers that gave each connection its own thread were falling over well before ten thousand users, because most of those threads were just waiting on the network and each one still cost memory and switching. The answer was Ruth's, one level up: a single loop that waits on all the connections at once and works on whichever is ready. It became nginx and Node.js. And it brought back her graduate student's bug. In an event loop, one request that computes for a long time without waiting holds up everyone ([Node.js, "Don't Block the Event Loop"](https://nodejs.org/en/guides/dont-block-the-event-loop)). Ladder: up, an operating system abstraction (non-blocking I/O) in place of hand-managed thread pools.

## What survived

The operating system turns one machine into many processes and threads and decides who runs. It takes the processor back on a timer so nobody can keep it by accident, and it hands out devices and files so programs don't fight over them. Sharing creates waiting, and waiting, not computing, is where most time goes. Sharing also creates new failures that no single program causes, like deadlock, and they're fixed by rules about the order things are taken, not by better programs.

## Where it gets misapplied

- **Threads for everything.** A thread per task is easy to write and expensive at scale. Most of those threads are waiting.
- **"Async" with nothing to wait on.** Asynchronous code helps when a program waits on the network or disk. Wrapping pure computation in it adds complexity and saves nothing.
- **Blaming the language when the scheduler is the issue.** A slow service is often a blocked thread, a full pool, or a lock, not a slow language.
- **The mirror:** ignoring concurrency until production. Deadlocks and races rarely show up on a laptop with one user.

## Connections

- Learning this is also learning [event loops and threads](runtimes/event-loops-and-threads.md), because the concurrency model is a choice your language's runtime makes for you, and it decides what blocks.
- Learning this is also learning [queueing](latency/queueing.md), because most latency is time spent waiting in a queue, and queues get long suddenly as a machine nears full.
- Learning this is also learning [reliability](11-software-that-must-not-go-down.md), because something has to notice when a process dies or gets stuck, and decide what to do.
- Learning this is also learning [queues](dsa/queues.md), because a scheduler is a queue with rules about who goes next.
- Learning this is also learning [graphs](dsa/graphs.md), because a deadlock is a cycle in a graph of who waits for whom, and finding cycles is a standard graph algorithm.
- Learning this is also learning [cloud](09-buying-computers-is-too-slow.md), because a hypervisor is the same trick one floor down: dividing one machine among whole operating systems instead of programs. IBM was doing it by the late 1960s, and it's what the hyperscalers rent out by the hour, noisy neighbours included.

## Resources

1. Remzi and Andrea Arpaci-Dusseau, [*Operating Systems: Three Easy Pieces*](https://pages.cs.wisc.edu/~remzi/OSTEP/) (start here: free, and the concurrency part covers this page). <!-- verify -->
2. Dan Kegel, ["The C10K problem"](http://www.kegel.com/c10k.html) (go deeper: dated now, but it shows the thinking). <!-- verify -->
3. Node.js, ["Don't Block the Event Loop (or the Worker Pool)"](https://nodejs.org/en/guides/dont-block-the-event-loop) (the event loop's one rule, explained).
4. Coffman, Elphick and Shoshani, "System Deadlocks", *ACM Computing Surveys* 3(2), 1971 (reference).

## Names you'll hear

- **Process, thread:** a process is a running program with its own memory; threads are several lines of execution sharing one process's memory.
- **Preemption, time slice:** the scheduler taking the processor back on a timer.
- **Deadlock** (Dijkstra's "deadly embrace"), **semaphore:** Dijkstra's tool for programs taking turns.
- **Event loop:** one thread waiting on many things and handling whichever is ready.

## Go and look

Find something running on serverless compute and watch for a cold start: the first request after a quiet spell is slower. That's the scheduler made visible.

## The model so far

New on this page: sentence 2, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. **A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.**
