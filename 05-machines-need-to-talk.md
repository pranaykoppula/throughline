# 5. Machines need to talk

Last reviewed: 2026-10-24

## Problem

Data was rarely on the machine that needed it. Moving it between machines meant crossing a link that was slow, shared, and unreliable, where a message could be lost, delayed, or delivered twice, and neither side could see what the other had received.

## The story

Lin Zhao was a physics graduate student in California in 1980, and her experiment's data lived on a computer at a lab across the country. For two years the data had reached her the way it reached everyone: on magnetic tape, in a box, by mail. A week each way, if nothing got lost. Her adviser liked to say you should never underestimate the bandwidth of a station wagon full of tapes. Lin had started to hate that joke.

The department had just been connected to the ARPANET, the research network that linked a few hundred machines at universities and government labs. Nobody quite knew what to do with it yet. Lin decided to use it to fetch her data.

The network didn't work like a telephone line. It cut every message into small *packets* and sent each one on its own, hopping from machine to machine towards its destination. A packet could take a different route from the one before it. It could arrive late, or out of order, or not at all. Nothing guaranteed delivery. All a sender could do was send and wait to hear back.

Her first program was the obvious one. Send a block of data, wait for the other end to confirm it had arrived, then send the next. It worked. It was also painfully slow. Each confirmation took a fraction of a second to come back across the country, and for that whole time the line sat idle. She worked it out on paper: almost all of her transfer time was waiting for replies, not sending data. The cost of the transfer wasn't the size of the data. It was the number of round trips.

So she let the program send several blocks before waiting, numbering each one, and had the other end confirm by number. The transfer went eight times faster. Then the file arrived corrupted. She spent a week finding out why. A block had arrived safely, but its confirmation had been lost on the way back. Her program, hearing nothing, sent the block again, and the receiving end dutifully added it to the file a second time. From where Lin sat, *it never arrived* and *it arrived but the reply didn't* looked exactly the same. There was no way to tell them apart. The fix was to make repeats harmless: the receiver kept track of which numbered blocks it already had and quietly ignored duplicates. Then her program could resend as often as it liked.

In 1983 the whole network switched over to a new pair of protocols, TCP and IP, that did all of this for every program: numbered packets, confirmations, resending what was lost, ignoring duplicates, putting things back in order. Lin threw her transfer code away with some regret and a lot of relief. She thought of TCP as a contract between two machines that couldn't see each other. If both sides kept to it, data got through.

By 1986 she had finished her PhD and was running the department's computers, and the network had grown from a few hundred machines to several thousand. One week in October it stopped being usable. A link to a lab a few hundred yards away, which normally moved thousands of characters a second, was moving a few dozen. Nothing was broken. Every machine was up.

Lin looked at the traffic and couldn't make sense of it at first. The links were full, completely full, and almost nothing was getting through. Then she saw that most of what filled them was the same packets, sent again and again. The routers in the middle had more traffic than they could handle, so they dropped packets. Every sender, following its contract, saw the losses and resent. The resends added to the overload, so more was dropped, so more was resent. Each machine was doing exactly what it should to deliver its own data reliably. Together they were burying the network.

She checked her own scripts and found that she'd made it worse herself. A year earlier, to "make things reliable", she'd set her nightly backups to retry immediately and keep retrying until they got through.

*Before reading on: every sender was behaving correctly for itself, and the network was collapsing. What would you have changed?*

The answer came from Van Jacobson at the lab down the road, who had been tracing the same collapse. His conclusion turned Lin's instinct upside down. A lost packet usually wasn't bad luck. It was the network saying *too much*. So the right response to loss was to slow down, not to try harder. Start sending gently and speed up only while things are going well. When packets go missing, cut back sharply, and wait longer before each retry. Within a couple of years his changes were in nearly every TCP implementation, and the collapses stopped. Lin rewrote her backup scripts to wait a little longer after each failure, with a random amount added so they didn't all retry at the same moment. It felt strange to make something more reliable by making it try less often, but that's what worked.

Looking back, Lin saw the same few facts underneath everything she'd done with networks. Data is rarely where it's needed, so it has to move, and moving it is slow and unreliable and paid for in round trips. Protocols are contracts between machines that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so senders retry and receivers have to tolerate repeats. And retries have to back off, or a lot of well-behaved machines can bury a network together.

There was one more thing she only noticed years later. By the late 1990s she was downloading whole operating systems over the network in an afternoon, for free. Copying software had stopped costing anything. The companies that did well were the ones selling what you couldn't download: service, support, and someone you could trust to fix it.

## It really happened

Lin is fictional; the network and its collapse weren't. ARPANET began in 1969. Vint Cerf and Bob Kahn described the design that became TCP/IP in 1974, and ARPANET switched to it on 1 January 1983. In October 1986 the Internet had the first of a series of congestion collapses: throughput between Lawrence Berkeley Laboratory and UC Berkeley, about 400 yards apart, fell from 32 kilobits a second to 40 bits a second. Van Jacobson and Michael Karels traced it and fixed it with slow start, backoff and congestion avoidance, which are still how TCP behaves ([Jacobson and Karels, "Congestion Avoidance and Control", 1988](https://people.eecs.berkeley.edu/~sylvia/cs268/papers/congavoid.pdf)). Today's version of the same mistake is the *retry storm*, where many clients retry together and keep a struggling service down. The standard advice is Jacobson's, applied to services: back off, add randomness, and only retry operations that are safe to repeat ([Amazon Builders' Library, "Timeouts, retries, and backoff with jitter"](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)).

The round trip is still the unit of cost, and the most direct answer to it is moving the data closer. Since 2012 Netflix has given its own servers, filled with copies of its catalogue, to internet providers to install inside their networks, so most viewing never crosses the wider internet at all ([Netflix](https://about.netflix.com/en/news/how-netflix-works-with-isps-around-the-globe-to-deliver-a-great-viewing-experience)). That's Netflix's own description. Ladder: down, a hand-built delivery network at a scale where renting one cost more.

## What survived

Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, and "it didn't arrive" looks the same as "the reply didn't arrive". So senders retry, receivers make repeats harmless, and retries back off. Once data moves cheaply, copies are free, and value shifts to services, relationships, and trust.

## Where it gets misapplied

- **Chatty APIs.** Ten round trips where one would do. Each costs the full network delay, and on a phone that adds up to seconds.
- **Retries without idempotency.** Retrying "charge this card" when you can't tell whether the first attempt worked. Make the operation safe to repeat first, usually with an ID the receiver can check.
- **Trusting the network.** Assuming it's reliable, fast, and secure because it is on your laptop. Lin's corrupted file, on a bigger scale.
- **The mirror:** retrying nothing. Giving up at the first failure turns every blip into an outage. Retry, but with backoff.

## Connections

- Learning this is also learning [state machines](dsa/state-machines.md), because a TCP connection is one: a fixed set of states and the messages that move between them.
- Learning this is also learning [shortest paths](dsa/graphs.md), because routing a packet is finding a path through a graph of machines.
- Learning this is also learning [TLS](auth/tls.md), because a network you can't see into is one where you can't tell who's on the other end without it.
- Learning this is also learning [round trips](latency/round-trips.md), because round trips, not bandwidth, decide how fast most things feel.
- Learning this is also learning [serialization formats](data/serialization.md), because everything on the wire has to be turned into bytes in a format both sides agree on.
- Learning this is also learning [deadlock](02-one-machine-many-programs.md), because congestion collapse is deadlock's cousin: every party behaving reasonably, and the whole stuck.
- Learning this is also learning [queueing](latency/queueing.md), because a router's buffer is a queue, and congestion collapse is what happens when a queue overflows and everyone retries into it.

## Resources

1. Julia Evans, ["Networking! ACK!"](https://wizardzines.com/zines/networking/) (start here: short, illustrated, and exactly this page). <!-- verify -->
2. Jacobson and Karels, ["Congestion Avoidance and Control"](https://people.eecs.berkeley.edu/~sylvia/cs268/papers/congavoid.pdf) (1988; go deeper: the first page is the whole story).
3. Amazon Builders' Library, ["Timeouts, retries, and backoff with jitter"](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) (the same lesson, for services).
4. Ilya Grigorik, [*High Performance Browser Networking*](https://hpbn.co/) (reference: free, and the clearest book on what round trips cost). <!-- verify -->

## Names you'll hear

- **TCP/IP:** the protocols the Internet runs on. IP moves packets; TCP makes them a reliable stream.
- **OSI:** a rival design, more thorough and committee-built, that lost to TCP/IP because TCP/IP already worked and shipped free with Berkeley Unix. Its seven-layer diagram survives in textbooks.
- **REST:** Roy Fielding's description, in his 2000 dissertation, of the style the web's protocol follows.
- **Idempotent:** an operation that has the same effect however many times you repeat it.
- **Fallacies of distributed computing:** a famous list of false assumptions, starting with "the network is reliable".

## Go and look

Pick a number on a screen you use every day and trace how many network round trips it took to put it there.

## The model so far

New on this page: sentence 5, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

4. Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises.

5. **Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so systems retry and tolerate repeats. Once data moves cheaply, distribution is free, and value shifts from copies to services, relationships, and trust.**
