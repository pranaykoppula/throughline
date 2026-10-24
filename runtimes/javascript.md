# JavaScript

Last reviewed: 2026-10-24

A concept page: a language designed in a hurry for small scripts, which became the most widely deployed programming language in the world, quirks included.

## Problem

JavaScript was built to add small bits of behaviour to web pages, and it shipped in the browser everyone used. Because the browser was the only place to run code in a web page, it became the language for everything on the web, and later on servers too. Decisions made quickly for small scripts became permanent, because changing them would break millions of pages.

## The story

In 2009 Zara Ahmed built the shopping cart for a clothing retailer's website. JavaScript calculated the running total as customers added items, read quantities from the page, and showed a discount when the cart passed fifty pounds. She'd learned the language in a weekend; it was forgiving, it ran in every browser, and it let her build in days what would have taken weeks with page reloads.

The forgiveness was the problem. Quantities read from the page arrived as text, and when Zara added the delivery charge, `"2" + 3` gave `"23"`, so a customer was shown a delivery charge of twenty-three pounds. A check for an empty discount code used `==`, which considered `0`, `""` and `false` all equal to each other, so a code of `0` was treated as no code at all. Adding prices produced `59.99000000000001`. Each was a small bug. Each was a quirk of the language behaving exactly as specified.

*Before reading on: the language allowed all of this, and it couldn't be changed without breaking the web. What would you have done?*

Zara stopped relying on the forgiving parts. She converted text to numbers explicitly as soon as it was read from the page, and used `===`, which compares without converting types. She kept prices in whole pence, never in fractions of a pound, because the language's numbers were binary floating point, like every other ([floating point](../math/floating-point.md)). A tool that checked her code for risky patterns ran before every release. A few years later, the team moved the codebase to TypeScript, a typed layer that compiled to plain JavaScript and caught most of these mistakes before anyone ran the code.

Looking back, Zara thought JavaScript's quirks weren't stupid; they'd been reasonable choices for a language meant for ten-line scripts, made in a hurry, and then frozen by success. The lesson was to learn which parts to avoid, and to lean on tools that remembered for her.

## Where it shows up

| Page | The language | Its effect |
| --- | --- | --- |
| [6, Anyone can publish](../06-anyone-can-publish.md) | The only language in the browser | It won by shipping where everyone was, not by design. |
| [Event loops and threads](event-loops-and-threads.md) | A single event loop | One long script freezes the page; the whole language grew up around not blocking. |
| [Type systems](type-systems.md) | Loose types | `"12" + "5"` is `"125"`, which is why typed layers over it became popular. |
| [Floating point](../math/floating-point.md) | Every number is a binary floating-point number | `0.1 + 0.2` isn't `0.3`, as in most languages. |

It shows up elsewhere too: server-side code with Node.js, desktop apps built on web technology, and build tools for almost every website.

What these share is path dependence: the first language in the browser became the language of the web, and everything after it had to work around its first week.

## It really happened

Zara is fictional. Brendan Eich designed JavaScript at Netscape in May 1995, in about ten days, under pressure to ship it in the next browser release. The language was standardised as ECMAScript in 1997, and its early decisions, such as type conversion with `==` and a single number type, were kept because changing them would have broken existing pages. Later versions added stricter options alongside the old behaviour rather than replacing it. Microsoft released TypeScript in 2012, and Node.js, in 2009, took the browser's event loop to the server.

## What it is

JavaScript is a dynamically typed language with first-class functions, built around a single-threaded event loop, and the only language browsers run natively alongside WebAssembly. Its early design favoured forgiveness: automatic type conversion, loose equality, and one floating-point number type. Modern practice avoids those parts with strict equality, explicit conversion, linting and, often, TypeScript, while the language itself stays backwards compatible with pages written in 1997.

## Where it gets misapplied

- **Trusting implicit conversion.** `"2" + 3`, `==`, and values that are falsy without being false.
- **Money as floating-point.** Use whole units, like pence or cents, or a decimal library.
- **Heavy computation on the main thread.** It freezes the page; use workers.
- **The mirror:** writing it off as a toy. It runs most of the world's interfaces, and modern JavaScript with good tools is a capable language.

## Connections

- Learning this is also learning [type systems](type-systems.md), because its loose types are the reason TypeScript exists.
- Learning this is also learning [event loops and threads](event-loops-and-threads.md), because the browser's single loop shaped the whole language.
- Learning this is also learning [floating point](../math/floating-point.md), because every JavaScript number is one.
- Learning this is also learning [build systems and package managers](../tooling/build-systems.md), because modern JavaScript is rarely shipped as written; it's bundled, compiled and minified.
- Learning this is also learning [software supply chain](../vendors/supply-chain.md), because its package ecosystem is one of the largest and most fragile.

## Resources

1. [MDN's JavaScript guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) (start here). <!-- verify -->
2. Allen Wirfs-Brock and Brendan Eich, "JavaScript: The First 20 Years" (2020) (go deeper: the history, from the people who made it).
3. The [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/intro.html) (reference). <!-- verify -->

## Names you'll hear

- **ECMAScript:** the language's official standard name.
- **`==` and `===`:** equality with and without type conversion.
- **Truthy, falsy:** values treated as true or false in conditions, such as `0` and `""`.
- **Node.js:** JavaScript on the server.
- **TypeScript:** a typed superset that compiles to JavaScript.
- **Bundler:** a tool that combines many files and packages into what the browser downloads.

## Go and look

Open your browser's console and type `"2" + 3`, then `"2" * 3`, then `0.1 + 0.2`. Then find one place in a codebase you know where one of those could happen by accident.
