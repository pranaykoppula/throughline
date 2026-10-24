# Type systems

Last reviewed: 2026-10-24

A concept page: writing down what kind of thing each value is, so a machine can check what people would otherwise have to remember.

## Problem

In a small program, you remember what shape each piece of data has. In a large one, maintained by many people, nobody remembers everything. A function expects a field that someone renamed, a number arrives as a string, and the mistake is found by a user, not by the person who made it. Types make those assumptions explicit and checkable, at a cost in speed and flexibility.

## The story

In 2016 Ikaika Kahale worked on a fast-growing marketplace whose backend was written in Python and frontend in JavaScript, both without type annotations. That had been a deliberate choice. Early on, it let the small team change things quickly, without declaring every shape in advance, and it had helped them reach customers sooner.

By 2016 there were sixty engineers and half a million lines of code. A backend engineer renamed a field in the order data from `ship_date` to `shipping_date` and updated every place in the backend that used it. The frontend, a different codebase, still read `ship_date`. It got nothing, and showed every order's delivery date as blank. Nothing failed loudly. Nobody noticed for two days. A week later, a function that expected a price as a number was passed one as text from a new API, and joined `"12"` and `"5"` into `"125"` instead of adding them.

Ikaika went looking and found the same shapes, an order, a listing, a user, described by hand in four places: two in the backend, one in the frontend, one in the mobile app. Each copy was maintained by a person, and they had drifted.

*Before reading on: the code ran, the tests passed, and the shapes disagreed silently across a boundary. What would you have added?*

Ikaika didn't rewrite anything. Both languages had gained optional type checkers that could be added a file at a time, so he began with the most-used modules and the code at the boundary between frontend and backend. Every order, listing and user shape was written once, as a schema, and the backend's and frontend's types were generated from it, so they couldn't drift apart. The checker ran in the build. Renaming a field now showed every place in both codebases that used it, before anything shipped. It slowed the team slightly when writing new code. Six months later, nobody wanted to go back.

Looking back, Ikaika thought the early choice to skip types had been right for a small team moving fast, and wrong for a large one that couldn't hold the whole system in its heads. What changed wasn't the language. It was how many people needed to agree on the shape of the data.

## Where it shows up

| Page | The shape | Who checked it |
| --- | --- | --- |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | A type hand-mirrored across a language boundary | A person instead of a compiler; this page's Go and look. |
| [Serialization formats](../data/serialization.md) | A schema shared between programs | A type that crosses a boundary, with rules for changing it. |
| [JavaScript](javascript.md) | Values whose kind changes silently | `"12" + "5"` is `"125"`; typed supersets exist because of it. |
| [State machines](../dsa/state-machines.md) | An order's allowed states | A type with exactly those states makes impossible combinations unrepresentable. |

It shows up elsewhere too: API definitions, database schemas, configuration validation, and function signatures in every library.

What these share is page 3's lesson: a type is a boundary enforced by a machine, so people don't have to remember it.

## It really happened

Ikaika is fictional. Dropbox, whose desktop client and backend were largely Python, gradually added the mypy type checker across about four million lines of code and wrote about the experience in 2019 ("Our journey to type checking 4 million lines of Python"). Microsoft released TypeScript in 2012 as a typed layer over JavaScript that compiles to plain JavaScript, so it could be adopted a file at a time. Both bet on *gradual* typing: types added where they help most, without a rewrite.

## What it is

A type system classifies values, such as numbers, strings and records with particular fields, and checks that operations use them consistently. Static typing checks before the program runs; dynamic typing checks, or doesn't, while it runs. Strong types catch mismatches early and document intent; they cost some speed of writing and flexibility. Gradual typing lets a codebase add types incrementally. At boundaries between programs, types generated from a shared schema keep both sides in agreement.

## Where it gets misapplied

- **The same shape defined by hand in several places.** They'll drift; generate them from one source.
- **Types everywhere on day one of a prototype.** Sometimes speed matters more than safety, for now.
- **Escape hatches everywhere.** A codebase full of "any" types has the cost of a type system and little of the benefit.
- **The mirror:** refusing types in a large codebase because they slowed you down when it was small.

## Connections

- Learning this is also learning [serialization formats](../data/serialization.md), because a schema is a type that crosses a boundary.
- Learning this is also learning [JavaScript](javascript.md), because its loose types are why typed layers over it became popular.
- Learning this is also learning [state machines](../dsa/state-machines.md), because a good type can make impossible states impossible to write.
- Learning this is also learning [build systems and package managers](../tooling/build-systems.md), because type checking runs in the build.
- Learning this is also learning [migrations](../data/migrations.md), because adding types to a large codebase is a migration done a file at a time.

## Resources

1. The TypeScript handbook, or mypy's documentation, for adding types to an existing codebase (start here).
2. Dropbox, "Our journey to type checking 4 million lines of Python" (2019) (go deeper: gradual typing at scale).
3. Benjamin Pierce, *Types and Programming Languages* (reference: the theory, in depth).

## Names you'll hear

- **Static, dynamic typing:** checked before running, or while running.
- **Gradual typing:** adding types to parts of a codebase over time.
- **Type annotation:** writing a value's type in the code.
- **Schema, code generation:** a shared description, and types produced from it automatically.
- **"Make impossible states unrepresentable":** designing types so invalid data can't be written.

## Go and look

Find one data shape defined in more than one place in a system you work on. Change a field name in one copy, in a branch, and see what, if anything, catches the mismatch.
