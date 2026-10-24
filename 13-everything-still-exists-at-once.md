# 13. Everything still exists at once

Last reviewed: 2026-10-24

## Problem

Every earlier page told the story of something new replacing something old. In practice nothing got replaced cleanly. Old systems kept running alongside new ones, everything around them kept changing, and the hardest engineering became keeping systems true to their purpose while the world moved under them.

## The story

Ines Carvalho joined the payments team at a regional bank in Porto in 2014. On her first day someone showed her the system that moved the bank's money every night: a COBOL program on a mainframe, first written in 1979. Most of the people who had written it had retired. The team spoke about it the way people speak about a damp patch in the basement.

Ines read through some of it in her first month. Near the top of one file was a comment from 1979, signed with initials, explaining that years were stored as two digits "to save space". Further down, a second comment from 1998, with different initials, explained how the two-digit years had been fixed before the year 2000. Ines found herself oddly moved. Two people she'd never meet, twenty years apart, had each made a sensible decision for their time, and both decisions were still running.

That spring a new chief technology officer announced that the old system would be replaced. The team would rewrite it in Java, as modern services, in eighteen months, then switch over in a single weekend. The reasons were good ones. The people who understood COBOL were retiring, new ones were hard to hire, and the mainframe was expensive. Ines volunteered for the project the same afternoon.

Two years later, the new system did about seventy percent of what the old one did, and the last thirty percent kept growing. Every few weeks someone found a rule nobody had written down. One currency was rounded differently from the rest. A church charity's account had special handling, added in 1987 for reasons no one could remember. One region had its own holiday calendar. None of it was in any document. The old code was the only specification the bank had, and it held thirty-five years of decisions. Meanwhile the old system still needed changing too, because regulators didn't wait, so every new rule had to be built twice. The first rehearsal of the switchover weekend ended with the two systems' nightly totals differing by a few thousand euros, and nobody could say which one was right.

*Before reading on: the old system worked and was hard to change; the new one was easy to change and didn't work yet. What would you have done?*

Ines wrote a two-page proposal that she was half afraid to send. It said: stop trying to switch everything at once. Put a thin layer in front of the old system that can send each kind of payment to either the old system or the new one. Move one kind first, standing orders, because they were simple and well understood. Run both systems on every standing order every night, compare the results, and only switch once they've matched exactly for a month. Then move the next kind. Keep the old system running for whatever hasn't moved, for as long as it takes.

The new CTO hated it at first. It meant admitting the big switchover wouldn't happen. But the totals from the second rehearsal were still wrong, and he agreed to try. Standing orders moved in four months. Each mismatch the nightly comparison found was an undocumented rule, which they now discovered one at a time and calmly, instead of all at once during a weekend. Over the next four years most kinds of payment moved. The core settlement process, the oldest and most reliable part, stayed on the mainframe. The team decided, with numbers, that moving it would cost more than it saved. It was the right decision for now, and they wrote down when they'd look at it again.

Something else happened along the way that Ines hadn't expected. Everything drifted, all the time, whether or not anyone touched the code. One library upgrade quietly changed how it rounded halves. A partner bank changed its file format with two weeks' notice. Python 2 reached the end of its life and took the team's support scripts with it. A runbook described a server that had been gone for a year. A new regulation changed what had to be kept and for how long. The engineer who understood the reconciliation reports left. None of it was a failure, exactly. It was simply what time did to systems. Ines came to think that keeping a system true to its purpose while everything around it moved was most of the job, and that building it had only ever been the start.

Years later, a junior engineer asked her why the rewrite had gone wrong when the reasons for it had been so good. Ines thought about it for a while. The reasons were real, she said. But the problem they'd set out to solve was "the system is old", and that wasn't actually a problem. The real problems were "we can't hire people to change it" and "it's expensive to run". Those could be solved a piece at a time, without betting the bank on one weekend. The most common mistake she'd seen in her career was adopting a solution to a problem you don't have. The second most common was refusing to change anything at all.

Looking back, Ines thought the lesson of those years was that none of it had ever been replaced. Every era of computing she'd read about was still running somewhere in the bank: overnight batch jobs from the 1970s, a tree-shaped database nobody had dared migrate, a website, a mobile app, and now a language model drafting customer letters. Some of it was there because it was the best tool. Some of it was there because it came first, or because someone in 1979 had chosen it and nobody since had had a good enough reason to pay for changing it. Engineering judgment, she decided, was mostly knowing which limit was binding now and which would lift next.

## It really happened

Ines is fictional; her bank is a composite of many. In 2017 Reuters reported that COBOL still underpinned 43% of banking systems and 95% of ATM transactions, as reported in secondhand coverage ([The New Stack](https://thenewstack.io/cobol-everywhere-will-maintain/)). The big-bang switchover she avoided happened to the UK bank TSB in April 2018. It moved its customers to a new platform in one weekend, and up to two million of them couldn't use their accounts properly for weeks. An independent report found the platform hadn't been ready and hadn't been properly tested, and the costs ran to hundreds of millions of pounds ([Computer Weekly](https://www.computerweekly.com/news/252473750/Major-report-on-TSB-IT-disaster-expected-soon); [DatacenterDynamics](https://www.datacenterdynamics.com/en/news/major-tsb-banking-outage-be-blamed-failure-test-data-center-ahead-it-migration/)). TSB disputed parts of the report. Ines's piece-by-piece approach has a name, the strangler fig, from Martin Fowler ([Fowler](https://martinfowler.com/bliki/StranglerFigApplication.html) <!-- verify -->).

Adoption is slow because the people who pay for switching are rarely the people who benefit. IPv6, the successor to the Internet's addressing scheme, was standardised in the late 1990s. Native IPv6 access to Google first passed 50% in March 2026 ([Internet Society Pulse](https://pulse.internetsociety.org/en/blog/18-years-later-ipv6-reaches-majority/)). Python 3 was released in December 2008, and Python 2 wasn't retired until January 2020. The year 2000 problem was a sensible decision made when memory was expensive ([page 1](01-one-machine-one-program.md)), paid for decades later by different people.

"Why did X win?" has three honest answers: it was better, it was first, or it was lucky. JavaScript shipped in the only browser that mattered. TCP/IP beat the more thoroughly designed OSI by working first and being free. x86 won on compatibility with what people already had. React was helped by Facebook's name. Many frameworks and databases became defaults because a popular tutorial used them. None of these were stupid choices, but none of them were inevitable either.

## Kinds of drift

Named so they can be noticed. Other pages mention whichever kind applies to them.

| Kind | What moves | Example |
| --- | --- | --- |
| Dependency | Library versions, deprecations, behaviour under you | A minor upgrade changing a default |
| Data | Schemas; for learned models, the input itself | A spam filter trained on last year's spam ([page 12](12-machines-that-learn-from-data.md)) |
| Infrastructure | What's deployed versus what the configuration says | A server changed by hand and never written down |
| Contract | Two sides of an interface changing separately | A partner's file format changing with two weeks' notice |
| Provider | Prices, quotas, model retirements | A cloud price change; a model you depend on being withdrawn |
| Requirement | The reason for a system moving while the system stays | Features nobody uses any more |
| Knowledge | Docs, runbooks, this wiki | A runbook for a server that no longer exists |
| Security | The world changing around a system that didn't | New vulnerabilities found in old dependencies |
| Organisational | The team's shape, and the system following it | Code nobody owns after someone leaves |

## What survived

None of this replaced what came before; every era still runs somewhere, and some of it is there because it was first or lucky, not because it was right. Adoption is slow because switching costs are paid now by the adopter, and the benefits arrive later, mostly to someone else. Everything drifts: dependencies, data, prices, requirements, and the reasons behind them. Replace old systems a piece at a time, with both running, rather than all at once. Engineering judgment is mostly knowing which limit binds now and which will lift next.

## Where it gets misapplied

- **The hype cycle.** Excitement, disappointment, then quiet usefulness, or nothing. Gartner's famous chart of it is a marketing artifact, but the shape is real.
- **Blockchain for everything.** Around 2017 and 2018, many projects put a distributed ledger under problems an ordinary database solved. It's the reference case for adopting a solution to a problem you don't have.
- **The big-bang rewrite.** Ines's first eighteen months, and TSB's weekend.
- **The mirror:** never changing. Staying on Python 2 until the security updates stopped. Christensen's *innovator's dilemma*: companies doing everything right for today's customers while something cheaper and worse grows up underneath them.

## Connections

- Learning this is also learning every earlier page, because each one handed you a solution that is still running somewhere next to the ones that followed it.
- Learning this is also learning [representations](00-representations.md), because the loop closes: every model on these pages has an edge, and time is what finds it.
- Learning this is also learning [migrations](data/migrations.md), because moving a running system's data without stopping it is the hardest part of Ines's piece-by-piece approach.
- Learning this is also learning [pushback](pushback.md), because "what problem do we have today, measured?" is the question that would have saved Ines's first eighteen months.
- Learning this is also learning [the forces](forces.md#switching-costs-and-lock-in), because lock-in, seen from the inside, is a migration nobody can afford.

## Resources

1. Martin Fowler, ["Strangler Fig Application"](https://martinfowler.com/bliki/StranglerFigApplication.html) (start here: Ines's proposal, in a page). <!-- verify -->
2. Titus Winters, Tom Manshreck and Hyrum Wright, [*Software Engineering at Google*](https://abseil.io/resources/swe-book), the chapters on Hyrum's law and deprecation (go deeper: free online). <!-- verify -->
3. Ward Cunningham, ["The WyCash Portfolio Management System"](https://c2.com/doc/oopsla92.html) (1992): where "technical debt" comes from, and it meant something narrower than it does now. <!-- verify -->
4. Simon Wardley's writing on evolution, genesis to custom to product to commodity (reference: the ladder itself drifting over time).

## Names you'll hear

- **Technical debt:** Cunningham's 1992 metaphor for shipping code before you fully understand the problem, then paying interest until you refactor. The term itself has drifted to mean almost any old code.
- **Legacy system:** a system that still works, that people depend on, and that nobody wants to touch.
- **Strangler fig:** replacing a system one piece at a time while it keeps running.
- **Hype cycle** (Gartner): the shape of excitement around a new technology.
- **Bit rot:** software getting worse without being changed, because everything around it did.
- **Path dependence:** where you can go depends on where you've been.

## Go and look

Find something you maintain with a stale "last reviewed" date, or something that should have one and doesn't.

## The model so far

New on this page: sentence 13, in bold. This is the whole model; it's also in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

4. Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises.

5. Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so systems retry and tolerate repeats. Once data moves cheaply, distribution is free, and value shifts from copies to services, relationships, and trust.

6. Client and server split the work: the server owns the truth, the client owns presentation and a copy of state. Most interface bugs are two sources of truth disagreeing. The browser won because shipping one server beats shipping a million installs; native shells survive where platforms control distribution.

7. Once strangers can reach a system, every boundary is a question of who is asking and what they may do. Trust nothing that crossed a boundary; give every party the least it needs. Harms from data fall on people other than those who collect it, so law steps in where incentives don't.

8. When one machine isn't enough, data is copied and split, and copies disagree for a while. Every distributed design chooses what to promise about consistency versus availability. Precompute what is read often; accept approximate answers where exactness costs too much.

9. Machines are rented by the unit, so cost is a live design variable: every architecture is also a bill. Subscription ties the vendor's revenue to the customer's continued use, and capex becoming opex changes who can start a company. An advantage competitors can't copy quickly is worth more than a better product, and most such advantages, switching costs, network effects, scale, are things engineers build or erode.

10. Systems are built by many people over time, so the codebase is itself a system, with its own data (history), protocols (branches, reviews), and trust boundaries. Practices live in tools; choosing a tool is choosing a practice.

11. Everything fails; the questions are how you'll know and what you promised. Define what "working" means before measuring it. Instrument for questions you haven't asked yet.

12. Some transformations are learned from data rather than written, and are only as good as the data and the context they're given. Inference is a new kind of round trip, paid in tokens and uncertain in output, and it reintroduces every trust problem at a new boundary.

13. **None of this replaced what came before; every era still runs somewhere, and some of it is there because it was first or lucky, not because it was right. Adoption is slow because switching costs are paid now by the adopter and the benefits arrive later, mostly to someone else. Nothing stays put: dependencies, data, prices, requirements, and the reasons behind them all drift, and what was rightly hand-built becomes a commodity someone else maintains. Keeping a system true to its purpose while everything around it moves is as much the job as building it. Engineering judgment is mostly knowing which limit binds now and which will lift next, and the commonest failure is adopting a solution to a problem you don't have.**
