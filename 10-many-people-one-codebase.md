# 10. Many people, one codebase

Last reviewed: 2026-10-24

## Problem

Once dozens of people changed the same code, their changes collided, overwrote each other, and broke things nobody had touched. A codebase needed rules for who changes what and when, and the rules only held if something enforced them.

## The story

Sofia Lindqvist joined a company in Gothenburg in 1996 that made accounting software for small businesses. Eight developers kept the code in a folder on a shared network drive. If you wanted to change a file, you opened it and changed it.

In her third week she spent four days rewriting the tax calculation module. On the Friday afternoon she opened it to make one last fix and found her work gone. A colleague had opened the same file on Monday, made a two-line change, and saved it on Thursday evening, writing his Monday copy over her four days. He was mortified. She was furious, and then mostly tired. There was no history to go back to. She did it again.

The team bought a version control system the next month. To change a file you *checked it out*, which locked it so nobody else could edit it until you checked it back in. Every check-in was kept, so you could see who had changed what and go back to any earlier version. Nobody lost work again. For a team of eight, it was exactly right.

By 1999 the team was forty people, and the locks had become the problem. Some files, like the main menu or the database layer, were needed by almost every change. Someone would check out the menu file on a Thursday and go on holiday, and half the team would sit waiting. People started copying locked files to their own machines, editing them anyway, and checking their copies in over the top once the lock came free. Sofia lost work again, this time to people working around the tool that had been bought to stop exactly that. The tool had decided how they worked: one person per file, in turn. The team had outgrown that.

In 2001 they moved to a different kind of system. Nobody locked anything. Everyone edited their own copy, and when you were ready the tool *merged* your changes into the shared version, line by line. Only when two people had changed the same lines did it stop and ask a human. The waiting stopped. Merging felt almost like magic.

With merging so easy, the teams grew bolder. Each big feature got its own *branch*, a separate line of development, so it could be built without disturbing anyone. The payroll team branched in January, the reporting team in February, and the new invoicing team in March. Each planned to merge back when they were done. It seemed responsible. Nobody wanted half-finished features in the shared code.

They merged in September. It took three weeks. Every branch had changed the database layer, the menu and the shared calculations, and each had been built against a version of the code the others no longer had. Merging the lines was the easy part. Then the code had to work together, and it didn't. Fixes for one branch broke assumptions in another. The release slipped by a month. Sofia, who had been looking forward to the new invoicing screens for half a year, spent the autumn untangling them instead.

*Before reading on: merging small changes was easy, and merging big ones was a disaster. What would you have changed?*

Sofia's answer, worked out with the lead of the payroll team over a lot of coffee, was that the tool hadn't failed. The way they used it had. Merges were painful because they were rare; the longer two lines of code drifted apart, the worse it was to bring them back together. So they did the opposite of what had felt responsible. Everyone merged into the shared code at least once a day, in small pieces. Unfinished features went in too, switched off behind a setting so customers didn't see them. A machine built the whole product and ran the tests every time anyone merged, and if it broke, fixing it came before anything else. The first month felt reckless. By the third, merge day had stopped existing.

The daily merges brought another change. Before anything went into the shared code, one other person now had to read it. They argued about this. Some of the senior developers felt it was a waste of their time. But reviews caught bugs, and more than that, they meant at least two people understood every change. When someone left, their code didn't leave with them. It also meant no single person could put anything into the product alone, which the company's auditors liked a great deal.

None of it lasted on goodwill. When reviews were a team agreement, they were skipped in a busy week. When the build server simply refused merges that hadn't been reviewed, or that broke the tests, nobody skipped them. Sofia came to think that a practice that wasn't in a tool wasn't really a practice. It was a hope.

Years later, on a team using git, she watched a new developer use the history to answer a question nobody remembered the answer to: why did this odd line exist? The commit that added it explained a tax rule from 2004, with a link to the bug that had needed it. The codebase had become a system of its own. Its history was data, its branches and reviews were protocols, and its rules about who could change what were trust boundaries, just like the product's.

Looking back, Sofia noticed something she hadn't expected. Every change of tool had been a change in how people worked: locking meant taking turns, merging meant working in parallel, review rules meant nobody worked alone. Choosing a tool was choosing a practice, whether or not anyone said so.

## It really happened

Sofia is fictional; her tools follow the real ones. Version control began with lock-based systems in the 1970s and 80s. CVS, from 1990, popularised editing in parallel and merging, and Subversion followed in 2000. The Linux kernel, with thousands of contributors, used a proprietary system called BitKeeper from 2002. When its free licence was withdrawn in April 2005, Linus Torvalds made the first commit of git on 7 April, and it was usable for the kernel within about ten days. Torvalds has said the ideas had been forming for months before that ([GitHub, "Git turns 20"](https://github.blog/open-source/git/git-turns-20-a-qa-with-linus-torvalds/); [Pro Git](https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git)). Integrating continuously instead of on merge day was written up by Martin Fowler as [continuous integration](https://martinfowler.com/articles/continuousIntegration.html) <!-- verify -->.

Organisations have their own versions of Sofia's lesson. Around 2002, by the account of a former Amazon engineer, Jeff Bezos told every team to expose its data and functionality only through service interfaces, with no other way for teams to reach each other's systems. The memo itself has never been published. What's known comes from Steve Yegge's 2011 post, written for Google colleagues and made public by accident ([copy](https://courses.cs.washington.edu/courses/cse452/22wi/papers/yegge-platform-rant.html)). It was a rule about how people worked, enforced through how the systems were built. The reverse also happens: the "Spotify model" of squads and tribes was copied by many companies from a 2012 description, and a former Spotify engineer later wrote that Spotify itself never fully worked that way ([Jeremiah Lee, "Failed #SquadGoals"](https://www.jeremiahlee.com/posts/failed-squad-goals/) <!-- verify -->).

And sometimes giving code away is strategy. Google released Kubernetes as open source in 2014. One reading, Joel Spolsky's "commoditize your complement", is that it made the layer where Amazon was strongest cheap and interchangeable ([forces: marginal cost](forces.md#marginal-cost)). Google's stated reasons were different. Both can be true.

## What survived

A codebase built by many people over time is a system in its own right. Its history is data, its branches and reviews are protocols, and its rules about who can change what are trust boundaries. Integrate often, in small pieces; drift is what makes merging hard. Practices live in tools: a rule enforced by the build lasts, and a rule kept on goodwill doesn't. Choosing a tool is choosing a practice.

## Where it gets misapplied

- **Cargo-culting big-company process.** Squads, tribes, quarterly planning ceremonies, adopted from a blog post by a team of twelve. Often the company described didn't work that way either.
- **Tooling adopted for the CV.** A monorepo build system or a multi-stage release pipeline for a project two people work on.
- **Review as gatekeeping.** Reviews that wait days, or argue about style a formatter could settle, turn a safety practice into a queue.
- **The mirror:** no version control, or a single shared branch with no review. Still seen, usually right up until the first lost week.

## Connections

- Learning this is also learning [Merkle DAGs](dsa/merkle-dags.md), because git is a content-addressed graph of commits, where each one is named by the hash of what it contains.
- Learning this is also learning [CI pipelines](tooling/ci.md), because the build server is where Sofia's rules lived, and each one shapes how your team works.
- Learning this is also learning [code signing](auth/code-signing.md), because review and signed commits are controls on who can change what reaches users.
- Learning this is also learning [commit messages and design records](writing/commit-messages.md), because they're how the next person learns why.
- Learning this is also learning [forces](forces.md#incentives-inside-the-org), because systems take the shape of the teams that build them.

## Resources

1. Scott Chacon and Ben Straub, [*Pro Git*](https://git-scm.com/book/en/v2) (start here: free, and chapter 1 is the history). <!-- verify -->
2. Martin Fowler, ["Continuous Integration"](https://martinfowler.com/articles/continuousIntegration.html) (go deeper: Sofia's rethink, written up properly). <!-- verify -->
3. Titus Winters, Tom Manshreck and Hyrum Wright, [*Software Engineering at Google*](https://abseil.io/resources/swe-book) (reference: free online; review, testing and deprecation at very large scale). <!-- verify -->
4. Melvin Conway, ["How Do Committees Invent?"](http://www.melconway.com/Home/Committees_Paper.html) (1968): the origin of Conway's law. <!-- verify -->

## Names you'll hear

- **git:** Torvalds named it after himself, he joked; "git" is British slang for an unpleasant person.
- **DAG:** directed acyclic graph, the shape of git's history.
- **Trunk-based development, CI:** Sofia's daily merging, and the machine that checks every one.
- **Feature flag:** a setting that hides unfinished code from users.
- **Conway's law:** systems mirror the communication structure of the organisation that builds them.
- **DevOps:** the people who write software also running it, enforced, as ever, by tools.

## Go and look

Find a practice your team follows that's written into a file (a lint configuration, a build file, a contributing guide) and one that still only lives in someone's head. Ask which one will survive that person leaving.

## The model so far

New on this page: sentence 10, in bold. The full model is in [the-model.md](the-model.md).

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

10. **Systems are built by many people over time, so the codebase is itself a system, with its own data (history), protocols (branches, reviews), and trust boundaries. Practices live in tools; choosing a tool is choosing a practice.**
