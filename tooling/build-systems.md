# Build systems and package managers

Last reviewed: 2026-10-24

A concept page: the machinery that turns source code and other people's packages into a working program, and decides what needs rebuilding.

## Problem

A large program is built from thousands of files and hundreds of packages, and building all of it from scratch can take an hour. Rebuilding only what changed is far faster, but only if the build knows exactly what depends on what. When it guesses wrong, it skips something that needed rebuilding, and the result is a program that doesn't match its own source.

## The story

In 2012 Aiko Tanaka worked on a large desktop application, two million lines of C++ built with a tool that decided what to rebuild by comparing timestamps. If a source file was newer than the compiled file made from it, the source was compiled again. A full build took fifty minutes; most small changes rebuilt in two. It was the way builds had worked for decades.

Strange bugs started appearing that nobody could reproduce. A tester would report a crash; the developer would rebuild from scratch and the crash would vanish. Aiko traced one to its root. A developer had switched branches, which changed a header file's contents but, depending on the order git restored files, left its timestamp older than the compiled files that used it. The build tool saw nothing newer and skipped them. The program contained compiled code from two different versions of the header, mixed together. Other cases came from a build server whose clock had drifted, and from a package that had been quietly updated with the same version number. "Do a clean build" had become the team's answer to every unexplained bug, and clean builds took fifty minutes.

*Before reading on: the build decided what to rebuild from timestamps, and timestamps lied. What could it have used instead?*

Aiko's team moved to a build system that worked differently. Every build step declared exactly what it read and what it produced: these files, these packages, these compiler settings, nothing else. The tool ran each step in isolation, so a step couldn't quietly read a file it hadn't declared. And instead of timestamps it used contents. Each step's inputs were hashed, and if the hash matched one it had seen before, the stored output was reused, from this machine or from a shared cache. Same inputs, same output, every time. External packages were pinned to exact versions with recorded hashes.

The first month was painful, because declaring every dependency exposed dozens nobody knew about. After that, "do a clean build" stopped being advice, because a normal build was already exactly a clean build, only faster. Shared caching meant most developers' builds were mostly downloads of steps someone else had already done.

Looking back, Aiko thought the timestamp approach had been a guess about what changed, and a fast guess is still a guess. Naming each step's inputs by their contents turned the guess into a fact.

## Where it shows up

| Page | The build | The lesson |
| --- | --- | --- |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | Package managers, build systems, type checkers | Abstractions for managing other abstractions, and they break in the same ways. |
| [CI pipelines](ci.md) | Building every change | A fast, correct build is what makes building every change practical. |
| [Software supply chain](../vendors/supply-chain.md) | Packages pulled in automatically | The package manager is the machinery that extends trust to strangers. |
| [Merkle DAGs](../dsa/merkle-dags.md) | Content-addressed caching | Naming outputs by the hash of their inputs, the same idea as git. |

It shows up elsewhere too: container images built in layers, frontend bundlers, data pipelines that recompute only changed tables, and lockfiles.

What these share is that a build is a graph of steps, and getting it both fast and correct depends on knowing every edge and naming every input exactly.

## It really happened

Aiko is fictional. The timestamp approach comes from Make, written by Stuart Feldman at Bell Labs in 1976, reportedly after a colleague lost a morning debugging a program that hadn't been rebuilt after a change. It was a huge improvement, and it's still widely used. Google built its internal build system, Blaze, around declared dependencies and content-based caching, and released a version of it as Bazel in 2015. Package managers made the same move with lockfiles, which record exact versions and hashes so every machine installs the same thing.

## What it is

A build system turns sources into outputs through a graph of steps, rebuilding only what's affected by a change. Correct incremental builds need every step's inputs declared, steps isolated so they can't read undeclared inputs, and change detected by content rather than time. A package manager fetches and installs dependencies; pinning exact versions and hashes makes installs repeatable. Together they decide how fast a team can work, and whether what's built matches what's in the repository.

## Where it gets misapplied

- **Timestamps as truth.** Fast, and wrong whenever clocks or file orders lie.
- **Undeclared dependencies.** Steps that read files nobody listed, so changes to them don't trigger rebuilds.
- **Floating versions.** "Latest" means different machines build different programs.
- **The mirror:** a heavyweight build system for a small project that builds in ten seconds. Use the language's standard tools.

## Connections

- Learning this is also learning [Merkle DAGs](../dsa/merkle-dags.md), because content-addressed caches name outputs by their inputs' hashes.
- Learning this is also learning [graphs](../dsa/graphs.md), because a build is a graph, and the order of steps is a topological sort.
- Learning this is also learning [CI pipelines](ci.md), because a correct, fast build is what CI runs on every change.
- Learning this is also learning [software supply chain](../vendors/supply-chain.md), because the package manager decides what strangers' code gets in.
- Learning this is also learning [caching](../latency/caching.md), because a shared build cache is a cache, with the same staleness questions.

## Resources

1. Andrey Mokhov, Neil Mitchell and Simon Peyton Jones, "Build Systems à la Carte" (2018) (start here: a clear comparison of how build systems decide what to rebuild).
2. The [Bazel](https://bazel.build/) documentation on hermetic builds (go deeper). <!-- verify -->
3. Your package manager's documentation on lockfiles (reference).

## Names you'll hear

- **Incremental build:** rebuilding only what changed.
- **Hermetic build:** a build step that can only see its declared inputs.
- **Build cache, remote cache:** stored outputs reused when inputs match.
- **Lockfile:** exact versions and hashes of every installed package.
- **Dependency graph:** what depends on what.
- **Clean build:** rebuilding everything from scratch, usually to escape an incorrect incremental build.

## Go and look

Time a clean build of a project you work on, then an incremental build after a one-line change. Then find out how the build decides what to rebuild: by time or by content.
