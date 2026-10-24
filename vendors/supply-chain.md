# Software supply chain

Last reviewed: 2026-10-24

A concept page: the code you didn't write, written by people you've never met, running with all the power of the code you did.

## Problem

Almost every program is mostly other people's code: libraries, frameworks, tools, and the libraries those depend on. Each one is a decision to trust its authors, its future authors, and everyone who can publish a new version. Most of that trust is extended automatically, by tools, without anyone looking.

## The story

In 2016 Felix Wagner led a small team building a cryptocurrency wallet app in JavaScript. Like every JavaScript project, it depended on packages, and those packages depended on others. By the time Felix counted, the app pulled in over eight hundred of them, nearly all written by strangers. The build was set to accept new minor versions of each dependency automatically, so the app picked up bug fixes and security patches without anyone having to do anything. It was a reasonable policy, and widely recommended.

That March, a developer unpublished a tiny package of eleven lines that padded strings to a given length, after a dispute with the package registry. Thousands of projects, including Felix's, had it buried deep in their dependencies. Their builds failed within hours. The registry restored the package and changed its rules. Felix's team added a lockfile, so builds used exactly the versions they'd last tested, and moved on, rattled but unharmed.

Two years later, a small, popular package deep in the app's dependencies changed hands. Its original author had stopped maintaining it, and a stranger offered to take it over; the author, glad of the help, agreed. The new maintainer added a dependency, and a later version of that dependency contained code that did nothing at all, except inside one specific wallet app, where it tried to steal users' keys. It wasn't Felix's app, but it was one very like it, and he read the analysis with growing alarm. His app's dependency tree included the same package.

*Before reading on: the danger wasn't a bug, it was a trusted package passing to someone untrustworthy, and arriving through automatic updates. What would you have changed?*

Felix changed how the team trusted code rather than which code it trusted. The lockfile stayed, so nothing new arrived unreviewed. Updates became a weekly, deliberate job: a person read the list of changed packages, looked closely at any that had new maintainers or new dependencies, and checked the changes in anything that ran during installation. They cut the dependency tree by a third, removing packages that did trivial things. For the code that touched users' keys, they allowed only a short, named list of dependencies, each pinned and reviewed. It was slower and a little tedious. It was also the only way to know what was actually in the app.

Looking back, Felix thought the habit he'd had to break was treating "installed from the registry" as if it meant "checked by someone". Mostly it meant written by a stranger, often a tired volunteer, and published by whoever currently held the keys.

## Where it shows up

| Page | The trusted code | What happened |
| --- | --- | --- |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | OpenSSL | Secured much of the web on about $2,000 a year in donations, until Heartbleed. Everyone trusted it; almost nobody paid for it. |
| [Prompt injection](../ai/prompt-injection.md) | Text you didn't write, entering your system and being acted on | The supply-chain problem in a new form, for language models. |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | Dependency drift | A library upgrade quietly changing how it rounded. Code under you changes even when yours doesn't. |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | Review before merge | Felix's weekly review is Sofia's rule, applied to code from outside. |

It shows up elsewhere too: container base images, build tools, browser extensions, and the plug-ins in every editor.

What these share is trust extended to people you can't see, through tools that don't ask you first. The defences are the same: know what you depend on, pin it, review what changes, and depend on less.

## It really happened

Felix is fictional; the events weren't. In March 2016 the removal of the eleven-line `left-pad` package from npm broke builds across the JavaScript world, and npm changed its unpublishing rules. In 2018 the popular `event-stream` package was handed to a new maintainer who added a dependency carrying code aimed at a specific bitcoin wallet app. In March 2024 Andres Freund, a Microsoft engineer, noticed that SSH logins on his machine took half a second longer than they should, investigated, and found a backdoor in the widely used xz compression library. Someone using the name "Jia Tan" had spent about two years becoming one of its maintainers before inserting it. It was caught before reaching most stable systems ([Elastic's analysis](https://www.elastic.co/security-labs/500ms-to-midnight)). He found it with [profiling](../tooling/profiling.md), more or less by accident.

## What it is

The software supply chain is everything that goes into running your code: dependencies and their dependencies, build tools, package registries, base images, and the people who maintain and publish them. Each link is trusted with the same power as your own code. Managing it means knowing what's there (an inventory), fixing versions (lockfiles), reviewing changes, preferring fewer and better-maintained dependencies, and checking where packages really came from.

## Where it gets misapplied

- **Automatic updates with no review.** Felix's first policy: patches arrive quickly, and so does anything else.
- **Hundreds of tiny dependencies.** Each one is a stranger with publishing rights to your app.
- **Trusting popularity.** Widely used isn't the same as well maintained; xz was everywhere and had one exhausted maintainer.
- **The mirror:** never updating. Pinned, unreviewed, years-old dependencies collect known vulnerabilities instead.

## Connections

- Learning this is also learning [least privilege](../auth/least-privilege.md), because code that doesn't need network or file access shouldn't have it, even if a dependency would like it.
- Learning this is also learning [code signing](../auth/code-signing.md), because signatures are how you check a package came from who it claims.
- Learning this is also learning [build systems and package managers](../tooling/build-systems.md), because they're the machinery that extends this trust automatically.
- Learning this is also learning [input validation](../auth/input-validation.md), because a dependency is input from strangers that runs as code.
- Learning this is also learning [profiling](../tooling/profiling.md), because the xz backdoor was found by someone measuring half a second nobody else noticed.

## Resources

1. [OpenSSF](https://openssf.org/) guides on securing dependencies (start here). <!-- verify -->
2. Elastic Security Labs, ["500ms to midnight: XZ A.K.A. liblzma backdoor"](https://www.elastic.co/security-labs/500ms-to-midnight) (go deeper: the anatomy of a patient attack).
3. Russ Cox, "Our Software Dependency Problem" (2019) (reference: how to think about what you depend on).

## Names you'll hear

- **Dependency, transitive dependency:** a package you use, and the packages it uses.
- **Lockfile:** a record of the exact versions installed, so builds are repeatable.
- **SBOM:** software bill of materials, an inventory of what's in a build.
- **Typosquatting:** publishing malicious packages with names close to popular ones.
- **Provenance:** evidence of where and how a package was built.
- **Maintainer takeover:** a package passing, by request or by force, to someone new.

## Go and look

Count the dependencies, including indirect ones, in a project you work on. Pick one you've never heard of, and find out who maintains it and when it was last updated.
