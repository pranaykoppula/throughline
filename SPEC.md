# Spec: the engineering learning wiki

**Status:** draft, 2026-09-15; revised 2026-10-24. This document is the design. Pages are built from it; when the two disagree, fix one or the other in the same change.

## 1. Purpose

A wiki for growing engineers with different starting points into full-stack engineers who make good trade-offs, can reason about a layer they haven't worked in, know what to ask (a colleague or Claude Code) when their knowledge runs out, and understand why the business wants what it wants.

It is a launchpad, not a curriculum. It gives general mental models and the start of every branch, then points outward. Depth lives in external resources, in the style of The Odin Project and the "awesome-*" repositories: a short spine of glue prose with curated links.

**It is not:** internal documentation, a skills matrix, a set of exercises with answers, or a history book.

**Later tracks** (not in this spec, but shaped by it): business acumen in depth (pricing, unit economics, go-to-market); AI engineering as a practice; mathematical intuition, built from the problems already on the spine (tail latency and percentiles, hash collisions, sampling and significance, what gradient descent does geometrically) rather than taught as a standalone syllabus.

## 2. Principles

1. **Problems before solutions.** Every topic is introduced as a limit that was hit, then the thing invented to get past it, then the abstraction that survived. Textbooks and "data structures and algorithms" present solutions with the problem removed; that's why they don't produce intuition.
2. **Sound decisions still cause problems.** Most stories here are a well-considered decision meeting a limit nobody could see from where they stood, and the return to the drawing board. That loop, not the final answer, is the life of an engineer, and it's what the cases teach.
3. **History as order, not as content.** Problems appeared in a sequence, and each solution presupposes the last, so the historical order is the learning order. Old systems get a cursory paragraph, enough to understand what survived. People and dates stay out, except where jargon needs context.
4. **One model, built cumulatively.** A single page-long mental model grows by a few sentences per problem. The finished model is the artifact people carry away; the pages exist to earn each sentence.
5. **Non-technical limits are limits.** Economics, law, user expectation, distribution, and competition moved the field as much as hardware did. They're taught alongside, and only where they changed what engineers build.
6. **Every solution has a misuse.** Each page says how its subject gets adopted by people who don't have its problem, and the wiki carries a toolkit for pushing back well. The mirror pitfall, refusing to adopt, gets equal honesty.
7. **Control versus ease is the axis.** Building is mostly assembling abstractions; optimizing is mostly replacing one with something made for the case. Every case study says which way it moved and what justified it.
8. **Nothing is permanent.** Dependencies, data, prices, requirements, and reasons drift (the kinds are listed in appendix B). Maintenance is most of the job, and the wiki itself is subject to the same rule.
9. **Blunt and honest.** See section 8.
10. **Stack-agnostic.** General models transfer. The wiki names no employer or product; concreteness comes from cases with a primary source, not from a private system nobody else can check.
11. **Short, except the story.** The story gets the length it needs to put the reader in someone's shoes. Everything else on a page is at most a screen; most sections are one to three lines, and sections a topic doesn't need are omitted rather than padded.

## 3. Structure

### 3.1 The spine

Fourteen problems, read in order, numbered 0–13. Each is one page.

| # | Problem | What survived |
| --- | --- | --- |
| 0 | Humans need representations before they need machines | Every representation is a choice with an edge; finding the edge is the reader's job, not the page's |
| 1 | One machine, one program | The memory hierarchy; cost is set by where the data is |
| 2 | One machine, many programs | Processes, threads, scheduling, files; waiting is where time goes |
| 3 | Programs too big for one head | Abstraction as the core skill; DSA as reusable shapes; control vs ease |
| 4 | Data outlives programs | Schemas, transactions, indexes; the store follows the access pattern |
| 5 | Machines need to talk | Protocols as contracts; the round trip as the unit of cost; retries |
| 6 | Anyone can publish | Request/response; the browser as a runtime; client state vs server truth |
| 7 | Strangers on the network | Trust boundaries, identity, least privilege |
| 8 | Too many users, too much data | Copies and splits; consistency vs availability; precompute; approximate |
| 9 | Buying computers is too slow | Rented compute; cost as a design variable; capex to opex |
| 10 | Many people, one codebase | Version control as a system; review; practices live in tools |
| 11 | Software that must not go down | SLOs; logs, metrics, traces; instrument for unknown questions |
| 12 | Machines that learn from data | Learned transformations; inference as a round trip; trust at a new boundary |
| 13 | Everything still exists at once | Adoption lag, path dependence, drift; judgment about which limit binds |

Page 0 is a different kind of page from 1–13: it's a preface, not a problem an engineer hits while building. It doesn't get the full page shape (section 7) — just Problem, What survived, Names, Connections. Its job is to foreshadow, in one page, that every representation the wiki hands out from here on (decimal, bits, request/response, consistency models) is a choice with an edge the reader hasn't found yet, the same way naturals gave way to negatives, irrationals, and complex numbers, decimal gave way to binary in machines, and bits now have qubits beside them for some problems. It states this once and moves on; it does not re-teach it on every later page.

### 3.2 Reference pages

- **`the-model.md`** — the finished cumulative model (section 4). Entry point for experienced readers: find the sentence you doubt, go to its problem. The other entry point, for everyone: start at the page you already know best; its connections show you what you don't.
- **`forces.md`** — the non-technical drivers (section 5), one paragraph each, with resources.
- **`pushback.md`** — the trade-off and pushback toolkit (section 6).

### 3.3 The graph

Every page has a **Connections** section: one line per edge, of the form *learning this is also learning X, because Y*. The "because" is the content. Edges may point at pages that don't exist; those dangling links are the frontier and are how the wiki grows. The README carries a Mermaid diagram of the spine plus the denser connections. Expected hubs: data, DSA, trust, latency, cost.

### 3.4 The lens

Four questions, stated once on the README and implied everywhere: what do we have (data, and its dimensions: shape, size, location, velocity, trust, cost to obtain); what can we do with it (store, move, transform, find, decide, show, protect); how, and within what limits (the ladder of means; limits that are physical/economic and limits that are policy/legal); and why (the value chain from data to business outcome, and the fact that the why moves). The chain also runs backwards: what users come to expect at the interface pulls new practice into the backend, from AJAX making backends into API servers, to mobile producing GraphQL, to live collaboration producing CRDTs, to chat producing streaming APIs.

The four questions are also the prompt to use when out of your depth, with a colleague or with Claude Code: *I have this data, I want this verb, what are the means, and which limit will bind?*

## 4. The model

Living text. Each numbered addition belongs to the spine page of the same number. Edit it there and here in the same change.

**Opening.** Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

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
13. None of this replaced what came before; every era still runs somewhere, and some of it is there because it was first or lucky, not because it was right. Adoption is slow because switching costs are paid now by the adopter and the benefits arrive later, mostly to someone else. Nothing stays put: dependencies, data, prices, requirements, and the reasons behind them all drift, and what was rightly hand-built becomes a commodity someone else maintains. Keeping a system true to its purpose while everything around it moves is as much the job as building it. Engineering judgment is mostly knowing which limit binds now and which will lift next, and the commonest failure is adopting a solution to a problem you don't have.

## 5. Forces

The recurring non-technical drivers. Each gets a paragraph and two or three resources in `forces.md`, and appears on spine pages only where it changed what engineers build (the guardrail).

| Force | One line | Shows up in |
| --- | --- | --- |
| Marginal cost | When copying is free, value moves to what surrounds the copy | Open source, SaaS |
| Network effects | Value grows with users; the winner takes most | Social, marketplaces, developer platforms |
| Who pays vs who benefits | Externalities invite regulation | GDPR, accessibility law, PCI |
| Distribution and platform power | Whoever controls the path to users controls the margin | App stores, thin native shells, defaults |
| Switching costs and lock-in | Why adoption is slow and moats are deep | Migrations, egress pricing, data gravity |
| Capex to opex | Changes who can start and how fast | Cloud, serverless |
| User expectation ratchets | A bar raised anywhere is raised everywhere | SPAs → APIs, mobile → GraphQL, feeds → cursor pagination, collaboration → WebSockets/CRDTs, chat → streaming |
| Incentives inside the org | You build what you're measured on | Conway's law |

Composite concepts such as a moat are defined in `forces.md` and taught on the spine page where a case shows them working.

## 6. Pitfalls and pushback

Each spine page has a **Where it gets misapplied** section: one to three ways its subject is adopted without its problem, with sources, and the mirror pitfall where relevant.

`pushback.md` holds the toolkit, phrased as questions because they're also the questions to ask Claude Code when out of your depth:

1. What problem do we have today, measured?
2. Which limit is binding, and which does this move?
3. What's the total cost: learning, operating, hiring, migrating, lock-in, and the option we give up?
4. Is it reversible? Two-way doors get tried; one-way doors get argued.
5. Who's recommending it, and what do they gain?
6. What's the boring alternative, and specifically why is it insufficient?
7. What does the case that made this famous have in common with us?
8. Can we try it small, with a date to decide?

And how to deliver: in writing, with numbers, with an alternative attached, and with "not now" kept separate from "never." The aim is a decision everyone can live with.

## 7. Page shape

Sections in order. Lengths are limits, not targets; omit what a topic doesn't have.

| Section | Length | Notes |
| --- | --- | --- |
| **Problem** | 2–3 sentences | The limit that was hit |
| **The story** | As long as it needs | Third person. Someone faces the problem without knowing the answer, or with only a vague idea. They make reasonable calls, at least one well-considered decision causes a new problem, and they go back to the drawing board until they reach a solution with staying power. Show the confusion, the guesses, and the people they ask. May be fiction, labelled as such; may be real. One or two "before reading on" pauses that ask the reader what they'd try |
| **It really happened** | 1–2 short cases | When the story is fiction, the real case it mirrors, with primary sources, so the reader sees that their reasoning matched what real engineers did. Say which way the case moved on control vs ease |
| **What survived** | 1 paragraph | The abstraction the story earned, stated precisely |
| **Why it happened** | 1–3 items | "X exists because…", with a source each; may say "honestly: partly luck"; often absent |
| **Where it lives today** | 1–2 lines | Concrete, but grounded in a documented public system, not a private one |
| **Where it gets misapplied** | 1–3 items | With sources; include the mirror pitfall when it applies |
| **Open, as of writing** | 1–2 lines | Only for a problem not yet closed: genuinely unsettled questions, dated. Framed as a question, not an answer. Usually absent — most pages describe a problem that's already been solved |
| **Connections** | 1 line each | "Learning this is also learning X, because Y." Dangling links allowed |
| **Resources** | 3–5 | Ordered start-here → go-deeper → reference. Prefer free, durable, primary |
| **Names you'll hear** | 1 line each | Only where jargon is a person's name or a historical accident. Usually absent |
| **Go and look** | 1 line, optional | An invitation to find the subject in something you've built ("trace a request; count the round trips"). No answer, no check |
| **The model so far** | The cumulative text | Full model to this point, this page's addition marked |

## 8. Voice

Blunt and honest, plain sentences, no hype.

The aim of the stories is to make great engineers feel human: the reader should finish a page believing they could have got there themselves. So the people in them are uncertain, guess, get things wrong for good reasons, ask for help, and recover. Nobody is a genius and nobody is a fool.

- Say when a winner won by luck or timing. Don't invent a rationale afterwards.
- Distinguish the reported reason from the likely reason. Engineering blogs are marketing; postmortems are edited; talks flatter the speaker. Link them anyway and say so.
- Name the money: who paid, who profited, what that did to the technology.
- Say "we don't know" when we don't.
- Don't grade the past by today's knowledge; most "mistakes" were reasonable under the limits of the time.
- Causal chains are told whole. The LLM chain, for example, has luck (gaming GPUs), a real cause (scale), a distribution event (a chat box), and a market dynamic (fear of missing out); an honest account keeps all four.

## 9. Conventions

- Files: `README.md`, `SPEC.md`, `the-model.md`, `forces.md`, `pushback.md`, and `NN-short-title.md` for spine pages (`01-one-machine-one-program.md` …). Kebab-case.
- Links: relative Markdown links. A link to a page that doesn't exist is deliberate and marks the frontier; don't "fix" it by removing it.
- Every page carries `Last reviewed: YYYY-MM-DD`. The wiki drifts too.
- The README holds: purpose in three sentences, the lens, the reading order, the Mermaid map, and the honesty rules.
- The repo is the wiki. It renders on GitHub and in editor previews; Obsidian shows the graph from the links. No site generator unless someone wants one.
- Progress is personal and local. A `progress.md` at the root is gitignored; each person keeps their own checklist of pages read and links followed in their clone. The repo tracks no one's progress.
- Anyone may edit. Changes to the model are reviewed by at least one other person, because the model is the thing everyone carries.

## 10. Decisions (resolved 2026-09-15)

1. **The model on each page is accumulated.** Every spine page ends with the full model to that point, the new sentences marked. The duplication is accepted for the reading experience; edits to a sentence are made on its page, in `the-model.md`, and in every later page's copy, in one change.
2. **"Go and look" prompts are in.** One optional line per page, no answers, no checks.
3. **No personal trails in the repo.** Progress is a local, gitignored checklist (section 9).

## 11. Build order

1. `README.md`, `the-model.md`, `forces.md`, `pushback.md`, and a `.gitignore` for `progress.md`.
2. Spine page 8 (scale) in full, as the sample of voice and depth; review before continuing.
3. Page 0, then pages 1–7, 9–13.
4. Verify every external link and every claim attributed to a source before it lands.

---

## Appendix A. Seed content by spine page

The material the first version of each page is written from. Cases and pitfalls each need a primary source verified before landing. "Ladder" is the control-vs-ease direction the case moved. Connections are one-line edges; the "because" is written on the page.

### 0. Humans need representations before they need machines
Reduced page shape only (Problem, What survived, Names, Connections) — see section 3.1. No Cases, Pitfalls, or Go and look; this page foreshadows, it doesn't argue a case.
- **Names:** Gödel (incompleteness); Turing (the halting problem, the same limit reached again in computation).
- **Connections:** → every later page, since each one hands out a representation past its edge · → DSA (Turing-completeness, page 3) · → the AI page (page 12, where the ground itself — the training data — is the thing that moves).

### 1. One machine, one program
- **Cases:** Why is reading a megabyte from memory faster than one disk seek, and what does that do to design? → "Latency numbers every programmer should know" (Dean). Google choosing cheap commodity machines → the GFS paper. Ladder: GFS is down-justified (hand-built storage at a scale nothing sold could serve).
- **Pitfalls:** Micro-optimizing CPU while the data is on the network; buying bigger machines before measuring where time goes.
- **Names:** Moore's law; Amdahl's law.
- **Connections:** → latency (the memory hierarchy is the whole story) · → DSA (cache-friendliness often beats big-O) · → cloud (it's still someone's computer) · → cost.
- **Go and look:** find the equivalent of a `GetItem` on a precomputed row in something you've built, and the equivalent of a scan; time both.

### 2. One machine, many programs
- **Cases:** How do you hold ten thousand open connections on one machine? → the C10K problem (Kegel), and the event-loop answer that became nginx and Node. Ladder: up (an OS abstraction, non-blocking I/O, replaced hand-managed thread pools).
- **Pitfalls:** Threads for everything; "async" everywhere with no I/O to wait on; ignoring the scheduler and blaming the language.
- **Names:** none needed.
- **Connections:** → languages & runtimes (single-threaded event loop vs threads vs processes) · → latency (waiting, not computing) · → reliability (what happens when a process dies).
- **Go and look:** find something running on managed serverless compute and watch for a cold start; that's the scheduler made visible.

### 3. Programs too big for one head
- **Cases:** When does the language become the bottleneck? → Twitter's move from Ruby to the JVM; Facebook compiling PHP (HipHop, then HHVM). Ladder: both down-justified, after measurement, at a scale most teams never reach. Counter-case: most teams that "outgrew" their language hadn't measured.
- **Pitfalls:** Framework churn; rewriting a working system in the new thing (Spolsky, "Things You Should Never Do, Part I"); not-invented-here; Knuth's "premature optimization" quote, given in full because it's usually cut to the wrong half.
- **Names:** Dijkstra; Turing-complete; second-system effect (Brooks); Hyrum's law; "worse is better" (Gabriel).
- **Connections:** → DSA (the standard library is free algorithms) · → hardware (what "compiled" and "garbage collected" cost) · → tooling (package managers, build systems, type checkers) · → collaboration (types are documentation for the next person).
- **Go and look:** find a type definition that's hand-mirrored across a language boundary in something you've built; that's an abstraction boundary maintained by a person instead of a compiler.

### 4. Data outlives programs
- **Cases:** How do you generate unique IDs across many database shards? → Instagram's sharded ID scheme (Postgres). Counter-case: Stack Overflow serving very large traffic from a handful of SQL servers. Ladder: Stack Overflow went down (hand-tuned SQL, no ORM) and stayed there deliberately.
- **Pitfalls:** NoSQL for "web scale" and then rebuilding joins in application code; many teams wrote about going back to Postgres. Never measuring what the ORM generates.
- **Names:** Boyce–Codd; ACID; CAP (Brewer), introduced here or at 8.
- **Connections:** → data (shape and access pattern decide the store) · → DSA (B-trees, LSM trees, hash indexes) · → hardware (disk vs memory vs network) · → trust (who can read which row: the tenancy boundary) · → cost.
- **Go and look:** find a table or collection you've worked with and ask whether its keys were chosen for how the data is written or how it's read; they're rarely the same answer.

### 5. Machines need to talk
- **Cases:** Why did Netflix put servers inside ISPs? → Open Connect; the round trip as the cost. Ladder: down-justified (a hand-built CDN when the scale made renting one worse).
- **Why it happened:** once data moves cheaply, distribution is free; open source and SaaS both follow (see forces).
- **Pitfalls:** Chatty APIs (many round trips where one would do); retries without idempotency; trusting the network to be reliable.
- **Names:** TCP/IP; OSI (as the "better designed" loser); REST (Fielding's dissertation).
- **Connections:** → DSA (TCP is a state machine; routing is shortest-path; buffers are queues) · → trust (TLS; who am I talking to) · → latency (round trips) · → data (serialization, formats on the wire).
- **Go and look:** pick a number on a screen you use daily and trace how many network hops produced it.

### 6. Anyone can publish
- **Cases:** Why did the page stop reloading? → Gmail and XMLHttpRequest; the browser becoming a runtime. How does Figma do multiplayer in a browser? → their engineering posts on multiplayer and their own engine. Ladder: Figma down-justified.
- **Why it happened:** shipping one server beats shipping a million installs; native shells survive where platforms control distribution. The backwards chain: SPAs → APIs; mobile → GraphQL (Facebook's news feed); feeds → cursor pagination; collaboration → WebSockets/CRDTs; chat → streaming.
- **Pitfalls:** A SPA for a page of text; state duplicated in three places; ignoring accessibility until it's a lawsuit.
- **Names:** AJAX; DOM; CRDT.
- **Connections:** → networking (HTTP is the contract) · → trust (the client is untrusted by definition) · → scale (feeds and pagination) · → languages (JavaScript won because it shipped in the only browser; ten days of design, decades of consequences).
- **Go and look:** find a piece of state cached client-side in something you've built and ask whether it's a second source of truth by accident or by design.

### 7. Strangers on the network
- **Cases:** What should a server store so it can check your password without knowing it? → the LinkedIn 2012 breach (unsalted hashes) as the cautionary case. Trust the library? → Heartbleed.
- **Why it happened:** harms from data fall on people other than the collector, so law steps in: GDPR, and what it made engineers build (deletion pipelines, data inventories).
- **Pitfalls:** Security theater; rolling your own crypto; a checklist instead of a threat model; the mirror: treating every control as friction and shipping without any.
- **Names:** Diffie–Hellman; RSA; Byzantine (as in fault tolerance); Merkle tree; zero trust.
- **Connections:** → auth (identity is data with the strictest trust axis) · → networking (tokens travel; where they leak) · → AI (prompt injection is a trust-boundary failure) · → vendors (what you trust when you use one).
- **Go and look:** find where a permission or role is decided in something you've built, and check whether it's derived server-side or accepted from the client; that's the tenancy boundary.

### 8. Too many users, too much data
- **Cases:** How do you build a home timeline for hundreds of millions of users? → Twitter's fan-out-on-write vs fan-out-on-read and the celebrity hybrid. YouTube's early scaling talk ("cheat on precision", approximate counts). Amazon's Dynamo paper for consistency trade-offs. Ladder: all down-justified; the page should say what scale justified them.
- **Pitfalls:** Microservices before the team or the load exists (Segment, "Goodbye Microservices"; Prime Video's consolidation, presented with the disagreement it caused). "You are not Google" (Nova) as the general argument. Sharding a database that fits on one machine.
- **Names:** CAP (Brewer); Paxos and Raft; Lamport clocks; eventual consistency.
- **Connections:** → data (copies disagree) · → databases (replication, sharding) · → latency and cost (fast and cheap are the same fight) · → the web (feeds pulled precomputation into the backend).
- **Go and look:** find something precomputed for a first paint in a system you use, and something loaded lazily beside it; that split is fan-out-on-write in miniature.

### 9. Buying computers is too slow
- **Cases:** When does owning hardware beat renting? → Dropbox's Magic Pocket (down-justified at exabyte scale) vs Netflix all-in on AWS (up-justified; engineering spent on what AWS doesn't sell). Prime Video 2023 as a pure cost story. Why does AWS charge so much for egress? → data gravity as a priced switching cost; honestly, also profit.
- **Why it happened:** capex to opex; subscription aligns vendor revenue with retention; the moat (appendix C).
- **Pitfalls:** Kubernetes for a three-person team; serverless for a workload that runs constantly; "cloud is cheaper" without a bill to prove it; the mirror: refusing the cloud and running a data center for a startup.
- **Names:** SaaS/PaaS/IaaS; capex/opex; "innovation tokens" (McKinley).
- **Connections:** → hardware · → networking · → cost · → trust (IAM) · → vendors (every vendor is a rung someone else built).
- **Go and look:** pull up a real cloud bill (your own team's, or a published one) and find one line item that's a design decision wearing a price tag.

### 10. Many people, one codebase
- **Cases:** How do thousands of people change one codebase without coordinating? → the Linux kernel workflow and why git exists (2005, after BitKeeper; kept for the jargon). Why does "everything is a service" exist? → the Bezos API mandate (a memo; kept because the jargon comes from it). Why did Google open-source Kubernetes? → to commoditize the layer where AWS had the moat (Spolsky, "Strategy Letter V").
- **Pitfalls:** Cargo-culting process from big companies (the "Spotify model" Spotify didn't use as described); tooling adopted for the résumé; the mirror: no version control, still seen.
- **Names:** git (the name); DAG; Conway's law; DevOps.
- **Connections:** → DSA (a content-addressed DAG; hashes as identity) · → vendors (GitHub, Jira, CI) · → trust (signed commits; review as a control) · → writing (commit messages, PR descriptions, ADRs).
- **Go and look:** find a practice your team follows that's encoded in a file rather than in memory (a lint config, a CI file, a CONTRIBUTING doc), and one that still only lives in someone's head.

### 11. Software that must not go down
- **Cases:** How many nines, and who decides? → Google's error budgets (SRE book). A bad deploy losing $440M in 45 minutes → Knight Capital 2012. A typo taking down a region → the 2017 S3 outage. Postmortems are edited; say so.
- **Pitfalls:** Dashboards nobody reads; alerts everyone mutes; three observability vendors; 99.999% for a dashboard nobody opens at night.
- **Names:** SLO/SLA/SLI; "nines"; blameless postmortem.
- **Connections:** → operating systems (what fails and how) · → scale (partial failure) · → collaboration (incidents are a team practice) · → cost (reliability is bought).
- **Go and look:** find where "working" is actually defined for something you maintain — a test, a dashboard, an on-call runbook — and who decided that definition.

### 12. Machines that learn from data
- **Cases:** Why did GPUs suddenly matter? → AlexNet/ImageNet 2012 (gaming hardware, repurposed; partly luck). Recommendations are a data problem → the Netflix Prize. The transformer → "Attention Is All You Need". The full LLM chain from section 8, told whole. These are settled: they describe what happened, not where things are heading.
- **Pitfalls:** An LLM where a regex, a SQL query, or a lookup table would do; agents for deterministic workflows.
- **Names:** Bayesian; gradient descent; transformer; token; "attention".
- **Connections:** → data (it's all training and context) · → math (linear algebra, probability, "is this anomaly real?") · → latency and cost (tokens are the new round trip) · → trust (injection, exfiltration) · → tooling (coding agents as a means).
- **Open, as of writing:** does a foundation-model company have a moat? The 2023 "no moat" memo raised the question; where a moat would actually sit — distribution, integrations, memory, something else — is argued, not settled, and this page should say so rather than pick a side. Provider drift (model deprecations and retirements) belongs here too: it's a live property of the field, not a fixed fact to state once.

### 13. Everything still exists at once
- **Cases:** Why is IPv4 still here? → IPv6's decades-long adoption. Python 2→3 taking twelve years. COBOL still clearing payments. Y2K as the cost of a reasonable assumption.
- **Luck and path dependence:** JavaScript's ten days; TCP/IP over OSI; x86 on compatibility; React partly on Facebook's name; databases and frameworks that won because a popular tutorial chose them. "Why did X win?" has three honest answers: it was better, it was first, or it was lucky.
- **Drift:** appendix B, in full, lives on this page.
- **Pitfalls:** The hype cycle as a shape (with the note that Gartner's version is a marketing artifact whose shape is real); blockchain-for-everything (2017–18) as the reference bandwagon; the mirror: the innovator's dilemma, and staying on Python 2.
- **Names:** Gartner hype cycle; technical debt (Cunningham's original metaphor, and how the term itself drifted); bit rot.
- **Connections:** → every hub; this page is where the graph's loops close.
- **Go and look:** find something you maintain with a stale `last reviewed` date, or that should have one and doesn't.

## Appendix B. Kinds of drift

Named so they can be noticed. Page 13 carries the list; other pages mention the kind that applies.

| Kind | What moves | Example |
| --- | --- | --- |
| Dependency | Library versions, deprecations, behaviour under you | A minor upgrade changing defaults |
| Data | Schemas; for ML, the input distribution | "Hidden Technical Debt in ML Systems" |
| Infrastructure | Deployed reality vs declared config | Terraform drift |
| Contract | Two sides of an interface evolving separately | API consumers breaking silently |
| Provider | Prices, quotas, model deprecations | Cloud price changes; model retirements |
| Requirement | The why moving while the system stays | Features nobody uses any more |
| Knowledge | Docs, runbooks, this wiki | Stale READMEs |
| Security | A world that changed around an unchanged system | New CVEs in old dependencies |
| Organizational | The team's shape, and Conway's law following it | Ownership gaps after departures |

Resources: *Software Engineering at Google* (Hyrum's law; deprecation chapters, free online); "Hidden Technical Debt in ML Systems"; Cunningham's original technical-debt note; Wardley on evolution (genesis → custom → product → commodity) as the model of the ladder itself drifting.

## Appendix C. Worked example: a moat

The template for any business concept: define it in `forces.md`, teach it where a spine case shows it working, connect it, and end with one question the reader can ask of their own work.

**Definition (for `forces.md`).** A moat is whatever makes a company's position hard to attack after competitors have copied the product. Products are copyable; moats are the things around the product that aren't: the cost of leaving (switching costs), value that grows with users (network effects), unit costs that fall with size (scale), control of how customers are reached (distribution), or something no one else can get (a cornered resource). Most are built, or destroyed, by engineering decisions, which is why engineers should be able to name them.

**Cases, on the spine.** Page 9: why AWS charges for egress (data gravity priced as a switching cost; also profit). Page 10: why Google open-sourced Kubernetes (commoditize the layer where AWS had the moat; open source as moat-breaker, then as moat-builder once an ecosystem forms). Page 12, flagged as open rather than settled: the 2023 "no moat" memo asked whether foundation-model quality alone protects anybody, and where a moat in that space would actually sit — distribution, integrations, memory — is argued rather than resolved. Page 13: a moat seen from the customer's side is a migration tax.

**Connections.** → trust (reliability and accuracy become a brand) · → data (history is the stickiest data) · → cloud & cost (lock-in is priced deliberately) · → collaboration (open source, standards, and APIs are moat strategy whether or not anyone says so).

**Resources.** Helmer, *7 Powers*; Morningstar's moat framework; Spolsky, "Strategy Letter V"; the Google "no moat" memo; Ben Thompson, Aggregation Theory.

**Names.** "Moat" is Buffett's term. "7 Powers" is Helmer's taxonomy.

**Go and look.** Pick a product you use that has real competitors and name which of the five moat types, if any, it's actually built. Most products have none yet; that's worth noticing too.

## Appendix D. Seeds for `pushback.md`

**Resources.** McKinley, "Choose Boring Technology"; Nova, "You Are Not Google"; Bezos's 2015 shareholder letter (one-way and two-way doors); Brooks, "No Silver Bullet"; Spolsky, "Things You Should Never Do, Part I"; Segment, "Goodbye Microservices"; Prime Video's 2023 post with the disagreement it caused; the hype cycle, noted as a marketing artifact with a real shape; Christensen, *The Innovator's Dilemma*, for the mirror pitfall.

**Names.** Second-system effect (Brooks); Hyrum's law; "worse is better" (Gabriel); innovation tokens (McKinley); one-way door (Bezos).

**Control vs ease, as a reading.** Down, justified: Dropbox Magic Pocket, Stack Overflow's SQL, Figma's engine, Twitter to the JVM. Up, justified: Netflix on AWS, self-hosted to managed databases. Down, too early: not-invented-here, optimizing before measuring. Never down: paying the abstraction tax forever because nobody measured it (ORM queries at scale). Wardley's evolution axis says the right rung moves over time.

## Appendix E. Seed connections (the graph's first edges)

Fourteen starting nodes: networking, auth & identity, latency & performance, languages & runtimes, DSA, databases & storage, data, trust & security, git & collaboration, vendors & tooling, cloud & infrastructure, AI & LLMs, math & statistics, hardware, cost. Spine pages own most of them; the rest (auth, latency, math, vendors, tooling) start as dangling links until someone writes them.

- networking → DSA (state machines, queues, retries, routing as graphs) · → trust (TLS) · → latency (round trips) · → data (serialization)
- auth → trust · → networking (tokens travel) · → DSA (hashing, signatures) · → data (identity) · → vendors (Cognito, OAuth providers)
- latency → languages (event loops vs threads) · → DSA (complexity; read- vs write-heavy) · → databases (indexes, caches, rollups) · → hardware (memory hierarchy) · → cost
- languages → latency · → DSA · → hardware · → tooling
- DSA → hardware (cache-friendliness) · → math
- databases → data · → DSA · → hardware · → latency · → trust (tenancy) · → cost
- data → databases · → AI · → math · → trust (privacy, ownership)
- trust → auth · → networking · → data · → AI (injection) · → vendors
- git → DSA (content-addressed DAG) · → vendors · → trust (signed commits, review) · → writing
- vendors → cost · → trust · → cloud · → git
- cloud → hardware · → networking · → cost · → trust (IAM) · → vendors
- AI → data · → math · → latency & cost (tokens) · → trust · → tooling (Claude Code)
- math → AI · → DSA · → data (distributions; "is this anomaly real?") · → latency (percentiles, not averages)
- hardware → latency · → DSA · → cloud · → cost
- cost → everything
