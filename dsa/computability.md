# Computability

Last reviewed: 2026-10-24

A concept page: some questions about programs can't be answered by any program, and recognising them saves years.

## Problem

It's tempting to ask a tool to check programs for us: will this ever crash, is this malicious, does this loop finish, are these two programs the same? Some of these questions have been proven impossible to answer correctly for every program. Tools still help, but only by giving up on being complete, or on being always right.

## The story

In 2003 Viktor Novak joined a company selling antivirus software. His first project sounded ambitious and straightforward: build a scanner that could look at any program and decide whether it was malicious, without needing a list of known viruses. Detect bad behaviour, not just bad signatures.

He worked on it for eight months. Each version caught more. Each also missed something new: code that decrypted itself only when run, code that waited a month before acting, code that did something harmless unless a particular date came round. For every rule he added, he could see how to write a program that slipped past it. He started to wonder whether he was bad at this.

An older colleague with a mathematics background listened to him one evening and asked whether he'd heard of the halting problem. Alan Turing had proved, in 1936, that no program can correctly decide, for every program and input, whether it will finish running. A few years after that, it had been shown that the same impossibility applied to *any* non-trivial question about what a program does, whether it eventually prints something, or deletes a file, or sends data away. And in the 1980s someone had proved the virus version directly: no program can detect every possible virus. Viktor hadn't been failing at a hard problem. He'd been trying to solve an impossible one.

*Before reading on: a perfect detector was impossible. What could Viktor still usefully build?*

It was oddly freeing. Viktor stopped aiming for a scanner that was always right about everything and chose which way to be wrong. The scanner would flag anything suspicious, accepting some false alarms, and pass flagged programs to a second stage. That stage ran them for a limited time in an isolated sandbox and watched what they actually did. A program that didn't finish in the time limit wasn't declared safe or dangerous. It was simply treated as unknown and held. Signature lists stayed, because they were fast and certain for the known cases. The product got much better, not because it solved the problem, but because it stopped pretending it could.

Looking back, Viktor thought knowing what was impossible had been the most practical thing he'd learned. It told him which kind of mistake to choose, and to put a time limit on everything.

## Where it shows up

| Page | The impossible question | What people do instead |
| --- | --- | --- |
| [0, Representations](../00-representations.md) | Gödel's and Turing's limits | Every formal system, even logic itself, has an edge. |
| [Graphs](graphs.md) | The shortest route through every city | No known fast exact answer; good approximations are used instead. |
| [Prompt injection](../ai/prompt-injection.md) | Reliably telling instructions from data in text | Limit what a fooled model can do. |
| [Input validation](../auth/input-validation.md) | Spotting every malicious input | Allow-lists, separate channels, and least privilege, instead of trying to recognise all bad input. |

It shows up elsewhere too: type checkers that reject some correct programs to never accept a wrong one, static analysers with false alarms, timeouts on everything, and the impossibility of proving a large program bug-free by testing.

What these share is a choice forced by mathematics: for hard questions about programs, a tool can be sound, complete, or fast, and must give up at least one.

## It really happened

Viktor is fictional; the results he learned are real. Alan Turing proved the halting problem undecidable in 1936. Henry Rice proved in 1953 that every non-trivial property of what programs compute is undecidable. Fred Cohen, who coined the term "computer virus", showed in the 1980s that no algorithm can detect all possible viruses. Antivirus products work anyway, combining signatures, heuristics and sandboxing, and accept false alarms and misses as the price. Many problems that are decidable are still believed to have no fast solution; whether they do, the P versus NP question, is one of the great open problems in mathematics.

## What it is

Computability theory studies which problems can be solved by any algorithm at all. Some, like the halting problem and, by Rice's theorem, most questions about a program's behaviour, are undecidable: no algorithm answers them correctly for every input. Complexity theory asks which solvable problems can be solved efficiently. In practice, tools facing these limits choose to be sound, never missing a problem but raising false alarms, or complete, never raising false alarms but missing some, or they bound the work with time limits.

## Where it gets misapplied

- **Promising perfect detection.** "Catches all malware", "finds every bug": impossible claims, usually from people selling something.
- **No time limits.** Analysis or execution that might never finish needs a cut-off.
- **Treating "unknown" as "safe".** When a tool can't decide, that's a third answer, not a pass.
- **The mirror:** giving up because a perfect answer is impossible. Imperfect tools catch most real problems.

## Connections

- Learning this is also learning [graphs](graphs.md), because many famously hard problems are graph problems.
- Learning this is also learning [type systems](../runtimes/type-systems.md), because a type checker is a sound but incomplete answer to "is this program correct?"
- Learning this is also learning [prompt injection](../ai/prompt-injection.md), because reliably separating instructions from data in text has no known solution.
- Learning this is also learning [input validation](../auth/input-validation.md), because recognising all bad input is hopeless; defining good input isn't.
- Learning this is also learning [floating point](../math/floating-point.md), because representations having edges is the same theme, one level down.

## Resources

1. Charles Petzold, *The Annotated Turing* (start here: Turing's 1936 paper, explained line by line).
2. Michael Sipser, *Introduction to the Theory of Computation* (go deeper).
3. Fred Cohen, "Computer Viruses: Theory and Experiments" (1987) (reference).

## Names you'll hear

- **Halting problem:** deciding whether a program finishes; undecidable.
- **Rice's theorem:** every non-trivial question about what a program computes is undecidable.
- **Turing-complete:** able to compute anything computable, which most languages are, and which is why these limits apply to them.
- **Sound, complete:** never missing a true problem, and never reporting a false one.
- **P versus NP:** whether every problem whose answer is quick to check is also quick to solve.

## Go and look

Find a tool you use that analyses code, such as a linter, type checker or security scanner, and find out which way it chooses to be wrong: false alarms, or missed problems.
