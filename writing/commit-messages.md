# Commit messages and design records

Last reviewed: 2026-10-24

A concept page: writing down why, for the person who'll need to know years from now.

## Problem

Code says what a program does. It rarely says why it does it that way, which alternatives were considered, or what would break if it changed. The people who knew leave or forget. Someone later finds a strange line, can't tell whether it's a mistake or a necessity, and either leaves it forever or removes it and finds out.

## The story

In 2015 Arjun Mehta joined a company that processed insurance claims, and in his first month he found a line that made no sense. Before a claim's amount was saved, it was rounded down to the nearest ten pence, but only for claims from one region, only between April and June. He looked at the history. The line had been added in 2009 by someone long gone, with the commit message "fix".

Arjun asked around. Nobody knew. It looked like a bug that had survived by accident, and it was short-changing customers. He removed it, wrote a test, and shipped it with a clear message. Three weeks later, a partner company that received the claims rejected a whole quarter's worth from that region. Their system, built around a regional tax rule from 2009, expected amounts in exact ten-pence steps during that period, and had always got them. The line had been a necessary workaround. The only record of why had been the single word "fix".

*Before reading on: the code was right, its reason was lost, and the next person reasonably removed it. What would have saved Arjun three weeks?*

The fix for that line took an afternoon: he put it back, with a comment explaining the partner's rule and a link to their specification. The bigger change was a habit, which he argued for at the next team meeting. Commit messages would explain why, not just what: the problem, the reason for this approach, and anything a future reader might wrongly think was a mistake. Pull request descriptions would say what alternatives had been considered. And for decisions that shaped the system, a choice of database, a rule about money, a workaround for a partner, the team would write a one-page decision record: the context, the decision, the alternatives and the consequences. Those pages were stored with the code and never deleted, only superseded.

Within a year, new engineers were reading the decision records in their first week, and "why is this here?" questions were usually answered by searching the history rather than asking around.

Looking back, Arjun thought "fix" had been an honest message from someone in a hurry who knew exactly what they meant. The trouble was that commit messages aren't for the person writing them. They're for whoever comes later, and that person knows nothing.

## Where it shows up

| Page | The record | What it saved, or cost |
| --- | --- | --- |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | A commit explaining a tax rule from 2004 | A new developer found why an odd line existed, years later, in minutes. |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | Comments from 1979 and 1998 in the payments code | Two people Ines never met, explaining their decisions across decades. |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | Types and module boundaries | Documentation for the next person, enforced by a machine. |
| [Data modelling](../data/modelling.md) | Why the model is shaped as it is | A model's reasons are as important as its tables. |

It shows up elsewhere too: runbooks, incident reviews, code comments, API documentation, and the README of every project.

What these share is that the reasons behind a system decay faster than the system itself, unless someone writes them down where the next person will look.

## It really happened

Arjun is fictional; his line has a famous principle attached. G. K. Chesterton wrote in 1929 about a fence across a road: a reformer who sees no use for it shouldn't be allowed to remove it until they've found out why it was put there. Engineers call it Chesterton's fence. Michael Nygard proposed lightweight "architecture decision records" in a 2011 post, "Documenting Architecture Decisions", and the format has been widely adopted. The Linux kernel's contribution guidelines ask that every change explain the problem it solves and why, because thousands of maintainers depend on reading the history.

## What it is

Commit messages, pull request descriptions and decision records are the written history of why a system is the way it is. A good commit message states the problem, why this change solves it, and anything surprising. A decision record captures the context, the decision, the alternatives considered and the consequences, kept with the code and superseded rather than deleted. Together they let future maintainers change the system with understanding instead of guessing.

## Where it gets misapplied

- **"Fix", "update", "changes".** Messages that tell the future reader nothing.
- **Explaining what, not why.** The diff already shows what changed.
- **Documentation stored somewhere else.** A wiki page nobody can find, or that describes a system that's since changed.
- **The mirror:** a long essay for a typo fix. Match the explanation to how surprising the change is.

## Connections

- Learning this is also learning [CI pipelines](../tooling/ci.md), because the history that pipelines and reviews produce is only useful if it explains itself.
- Learning this is also learning [data modelling](../data/modelling.md), because the reasons behind a model need recording as much as the model.
- Learning this is also learning [migrations](../data/migrations.md), because knowing why the old shape existed is the first step to changing it safely.
- Learning this is also learning [Merkle DAGs](../dsa/merkle-dags.md), because git's history is permanent, so what you write in it stays.
- Learning this is also learning [coding agents](../tooling/coding-agents.md), because an agent reads the history and comments as context, and makes better changes when they explain why.

## Resources

1. Chris Beams, ["How to Write a Git Commit Message"](https://cbea.ms/git-commit/) (start here). <!-- verify -->
2. Michael Nygard, ["Documenting Architecture Decisions"](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) (2011) (go deeper). <!-- verify -->
3. The Linux kernel's ["Submitting patches"](https://www.kernel.org/doc/html/latest/process/submitting-patches.html) guide, on describing changes (reference). <!-- verify -->

## Names you'll hear

- **Commit message:** the explanation attached to each change in version control.
- **ADR:** architecture decision record.
- **Chesterton's fence:** don't remove something until you know why it's there.
- **git blame:** the tool showing which change last touched each line.
- **Runbook:** written steps for operating a system, especially during incidents.

## Go and look

Run `git log` on a file you work on and read the last ten messages. Count how many tell you why the change was made. Then write your next one as if for someone who joins in five years.
