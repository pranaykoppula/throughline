# Language as compression

Last reviewed: 2026-11-03

A concept page in the information family: why a sentence can carry so much, why it loses so much, and why writing requirements, prompts and handovers is mostly the work of putting back what words leave out.

## Problem

Natural language is astonishingly dense. A short sentence can stand for a whole situation, because the listener fills in everything left unsaid from what they already know. That only works when the listener knows what the speaker knows. Words are also abstractions: every summary keeps a few features and drops the rest. Between people with different contexts, a sentence that felt precise to the writer can be decoded several ways, each of them reasonable.

## The story

In 2017 Daniela Ruiz was the engineering lead at a small company selling office supplies online, with one warehouse in Chicago and customers across the US. After a meeting with the sales team, the product manager wrote the new feature in a single line: *Orders placed before 3pm ship the same day.* Everyone in the meeting nodded. It was clear, short, and exactly what customers wanted to hear.

Daniela's team built it in a week. Two weeks after launch, the complaints began, and they didn't agree with each other. A customer in Los Angeles who ordered at 2pm her time was told her order would ship tomorrow. The team had built 3pm Chicago time, which had already passed. The warehouse manager was furious that orders arriving at 2:55 were being promised same-day, when the last truck left at 3:30 and an order took an hour to pack. To him, *before 3pm* had meant *before 3pm with time to pack it*. And the sales team was getting calls from customers who'd read *ship the same day* as *arrive the next day*.

Then there was the part nobody had written down at all. Daniela found it in the sales team's notes from the original customer call, two pages long: *except hazardous items like toner, which go by ground freight, and except on public holidays*. The one-line requirement was a summary of that call. Writing it had kept the headline and dropped the exceptions, because to the person who'd been on the call they were obvious.

Every person had decoded the sentence correctly, against their own context. The sentence had been compressed for the people who were in the room.

*Before reading on: the requirement was clear to everyone who wrote it, and meant something different to everyone who read it. What would you have added?*

Daniela didn't ask for longer documents. She asked for examples. Before building anything, the team now wrote down five or six concrete cases and what should happen in each, and the warehouse, sales and engineering each signed off on them. *A customer in Los Angeles orders a stapler at 11:50am Pacific time: ships today. A customer orders toner at 9am: ships today by ground freight, arrives in five days. An order arrives at 2:40pm Central: ships tomorrow.* Disagreements that a sentence had hidden showed up in the first example. She also had the engineer who'd build a feature say it back in their own words to whoever asked for it, before starting. And each requirement linked to the notes it summarised, so the exceptions could be found without anyone having to remember them.

Looking back, Daniela thought the product manager's sentence hadn't been careless. It was what language is for: saying a lot in a few words to people who already share the context. The trouble was that requirements are read by people who weren't there. Writing them well meant decompressing on purpose: concrete examples, stated assumptions, and a link back to the original.

## Where it shows up

| Page | The words | What they left out |
| --- | --- | --- |
| [Information](information.md) | A code word in a telegram | Meaning, which lived in a codebook the new agent didn't share. |
| [Compression](compression.md) | A briefing slide's headline | The caveat lower down, which was the whole point. |
| [Coding agents](../tooling/coding-agents.md) | "Make the test pass reliably" | The goal behind the check, which the agent had no way to know. |
| [Commit messages and design records](../writing/commit-messages.md) | "fix" | Why, which only the author knew, and then nobody did. |
| [Serialization formats](../data/serialization.md) | A field called `impulse` | The unit, assumed by both sides and different for each. |

It shows up elsewhere too: in prompts to language models, which fill every gap with the most typical reading; in contracts; in handovers between shifts; in user interface labels; and in every ticket titled "Fix the login thing".

What these share is that words are lossy, context-dependent compression. They work beautifully between people who share a context, and fail quietly between people who don't. The fixes are the same across all of them: concrete examples, stated assumptions, a fixed vocabulary for things that matter, and saying it back.

## It really happened

Daniela is fictional. Her company's problem is the oldest in software, and aviation has paid the most for it. On 27 March 1977, at Tenerife, two Boeing 747s collided on a fog-bound runway and 583 people died, the deadliest accident in aviation history. Among its causes was ambiguous language on the radio: the KLM crew's "we are now at takeoff" could mean "waiting at the takeoff position" or "taking off now", and the tower's reply, "OK… stand by for takeoff", was partly blocked by another transmission. Afterwards, aviation tightened its standard phrases so that critical words carry only one meaning; "takeoff" is now generally used only when giving or acknowledging a takeoff clearance ([one account](https://aerocorner.com/blog/tenerife-1977/)). Pilots also read back critical instructions word for word, which is Thomas's telegraph repetition from [information](information.md), applied to speech.

Software's versions are gentler. Eric Evans's *Domain-Driven Design* (2003) argued for a "ubiquitous language", a single vocabulary that developers and the business use with the same meanings. "Specification by example" made Daniela's concrete cases a practice. Language models made the problem more visible than ever: a short prompt is decompressed by a model with no shared context but the world's average, so it gets the most typical reading, not the intended one.

## What it is

Natural language transmits meaning efficiently by leaving most of it implicit, relying on shared context to fill the gaps. That makes it a powerful compression scheme between people who share context, and an unreliable one between people who don't. Words are also abstractions: each summary or category keeps some features and discards others. Precise communication across contexts restores what was left out: examples instead of only rules, explicit assumptions, controlled vocabulary for critical terms, read-back to confirm understanding, and links to the fuller original.

## Where it gets misapplied

- **One-line requirements.** Clear to the author, ambiguous to everyone else.
- **Summaries that replace their source.** The exceptions live in the source; keep a link to it.
- **Longer documents as the fix.** More words don't add shared context. Examples and read-back do.
- **The mirror:** specifying everything formally, all the time. Most conversations work fine in plain language; save the precision for what's expensive to get wrong.

## Connections

- Learning this is also learning [information](information.md), because meaning depends on a shared codebook, and language's codebook is everything the speakers already know.
- Learning this is also learning [compression](compression.md), because a summary is lossy compression with the writer's idea of what matters.
- Learning this is also learning [data modelling](../data/modelling.md), because modelling a domain starts with agreeing what its words mean.
- Learning this is also learning [tokens and context windows](../ai/tokens.md), because a prompt is compressed language decoded by a reader who knows only what's in the window.
- Learning this is also learning [commit messages and design records](../writing/commit-messages.md), because writing for a future reader is writing for someone outside your context.
- Learning this is also learning [power and predictability](../dsa/power-and-predictability.md), because the ladder of formal languages began as Chomsky's theory of grammar for human ones.

## Resources

1. Gojko Adzic, *Specification by Example* (2011) (start here: concrete examples as the cure for ambiguous requirements).
2. Eric Evans, *Domain-Driven Design* (2003), the chapter on ubiquitous language (go deeper).
3. The Tenerife accident report and the many analyses of it, such as the Flight Safety Foundation's (reference: what ambiguous language costs when the stakes are highest).

## Names you'll hear

- **Shared context, common ground:** what both parties already know, which language relies on.
- **Ubiquitous language:** a single, agreed vocabulary for a domain.
- **Specification by example:** requirements written as concrete cases.
- **Read-back:** repeating an instruction to confirm it was understood.
- **Curse of knowledge:** finding it hard to imagine not knowing what you know, which is why authors can't see their own gaps.

## Go and look

Take one requirement or ticket you're working on and write three concrete examples of what should happen. Show them to whoever wrote it. Count how many they'd change.
