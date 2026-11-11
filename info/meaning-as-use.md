# Meaning as use

Last reviewed: 2026-11-04

A concept page in the information family: an interface means whatever the people using it rely on, not what its documentation says. With enough users, every behaviour anyone can observe becomes part of the promise, whether or not anyone made it.

## Problem

Designers of an API, a file format, a protocol or a user interface write down what it promises, and then feel free to change everything else. But users don't read the promise; they read the behaviour. They notice that results come back in a certain order, that an error message says certain words, that a field is never empty, and they build on it, often without knowing they have. So the real interface is larger than the documented one, nobody can see its edges, and a change that keeps every written promise can still break thousands of people.

## The story

In 2016 Rui Teixeira led the team behind the public API of a parcel delivery company in Lisbon. Online shops used it to show their customers where a parcel was: collected, sorted, out for delivery, delivered. Rui was proud of how carefully the API had been designed. Every field was documented. The documentation said plainly that the list of tracking events for a parcel came "in no guaranteed order", and that clients should sort them by their time stamps. Anything not promised, the team was free to change. That was the point of having a contract.

That autumn the team moved tracking data to a new database that could handle the Christmas peak. They checked that every documented field was still present and correct, and it was. The next morning, support was flooded. Shops all over Europe were telling their customers that parcels had been delivered before they were collected, or were "out for delivery" after they'd arrived. The old database had always returned events in time order, as a side effect of how it was indexed. The new one didn't. Hundreds of shops had simply displayed the list as it came, or taken the last event as the current status. A few were also reading the text of error messages, looking for the words "not found", which the new system phrased differently.

Rui's first reaction was that the shops had ignored the documentation. Then a large customer's developer said, quite reasonably, that in three years the events had never once come back in any other order.

*Before reading on: the change kept every promise in the documentation, and it broke hundreds of customers. Who was right, and what would you have changed?*

Rui accepted that the API meant what it did, not what it said. The ordering went back the same day, and this time it was written into the documentation as a promise, since half the customers depended on it anyway. Error responses got stable codes that clients could check, with a note that the human-readable message could change, and the old wording stayed for a year while the team contacted every client that still matched against it.

Then the team changed how they made changes. Before switching any system, they sent a copy of real traffic to both the old and the new versions and compared every response, field by field and in order, not just the documented parts. Before removing or changing a behaviour, they measured who actually used it. And for behaviour they deliberately didn't want to promise, they made the absence of a promise visible. In the test environment that shops used while building their integrations, unpromised details such as the order of fields and the wording of messages were shuffled on purpose, so nobody could come to rely on them without noticing.

Looking back, Rui thought the documentation had been a statement of what he hoped the API meant. Its users had been writing the other half of the definition every day, by using it. With enough of them, nothing observable was private any more.

## Where it shows up

| Page | The interface | What its users made it mean |
| --- | --- | --- |
| [JavaScript](../runtimes/javascript.md) | Zara's quirks, such as `"2" + 3` | The web came to depend on them, so they were frozen by success and can never be fixed. |
| [3, Programs too big for one head](../03-programs-too-big-for-one-head.md) | A module's hidden behaviour behind its interface | With enough users, every observable behaviour is depended on by someone. |
| [Serialization formats](../data/serialization.md) | Jonas's messages between services | Every message was a contract, whether or not anyone wrote it down. |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | Ines's old and new payment systems, run side by side | Each nightly mismatch was an undocumented rule the old system had come to mean. |
| [Language](language.md) | "Make the test pass reliably" | The words meant something different to the agent that acted on them from what the person meant. |

It shows up elsewhere too: spreadsheets that keep historical bugs for compatibility, operating systems with special cases for old programs, network protocols that can't change because boxes in the middle of the internet depend on their old shape, user interfaces whose button positions users know by heart, and prompts that behave differently when the model behind them is upgraded.

What these share is that meaning is made by use. The designer's description is one party's view of an interface; the users' habits are the other, and once there are enough of them, theirs wins. Changing a widely used interface is less like editing a document and more like changing a language that people already speak.

## It really happened

Rui is fictional; the law has a name. Hyrum Wright, an engineer at Google, put it like this: with a sufficient number of users of an API, it does not matter what you promise in the contract; all observable behaviours of your system will be depended on by somebody. The idea is old in philosophy. In *Philosophical Investigations* (1953), Ludwig Wittgenstein argued that for a large class of cases, the meaning of a word is its use in the language, not a definition held somewhere.

Engineering has many examples. Excel treats 1900 as a leap year, which it wasn't. Lotus 1-2-3 made that mistake first, and Microsoft copied it so that spreadsheets would calculate dates the same way in both. It has never been fixed, because fixing it would change results that existing spreadsheets depend on ([Microsoft support](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year) <!-- verify -->). Joel Spolsky reported that Windows 95 detected the game SimCity, which used memory after releasing it, and ran its memory allocator in a special mode so the game kept working ([Spolsky, "How Microsoft Lost the API War"](https://www.joelonsoftware.com/2004/06/13/how-microsoft-lost-the-api-war/)). When TLS 1.3 was being deployed around 2017, network equipment that had only ever seen older versions broke on the new one, so the final standard made TLS 1.3 connections look like TLS 1.2 to anything in the middle. Its designers then adopted Rui's last idea: GREASE (RFC 8701, 2020) has clients send random meaningless values in places reserved for future use, so that nobody can build equipment that depends on those places being empty ([RFC 8701](https://www.rfc-editor.org/rfc/rfc8701)).

## What it is

Meaning as use is the idea that what a sign means is settled by how it's used, not by a definition. In software it's known as Hyrum's law, or the law of implicit interfaces: the effective contract of a widely used interface is everything users can observe, including ordering, timing, error text and bugs. The practical consequences are to make important implicit behaviour explicit and promise it, to make unpromised behaviour visibly unreliable (random ordering, changing values, deliberate variation in test environments), to measure what users depend on before changing it, to compare old and new systems on real traffic, and to treat deprecation as a long migration, not an edit.

## Where it gets misapplied

- **"It's not in the contract."** True, and no help to anyone whose system just broke. With enough users, the contract is the behaviour.
- **Parsing human-readable text.** Error messages, log lines and web pages change; clients that read them make every wording change a breaking one.
- **Testing only the documented parts during a migration.** Rui's team checked every field and missed the order.
- **The mirror:** freezing everything forever. Some behaviour has to change, and preserving every bug turns a system into a museum of accidents. Promise what matters, make the rest visibly unpromised, and change it with warning.

## Connections

- Learning this is also learning [JavaScript](../runtimes/javascript.md), because the web's dependence on its quirks is this law at the scale of a whole platform.
- Learning this is also learning [serialization formats](../data/serialization.md), because a format is an interface between programs, and unwritten parts of it get depended on too.
- Learning this is also learning [migrations](../data/migrations.md), because changing a system that others depend on means keeping old and new behaviour alive together for a while.
- Learning this is also learning [language](language.md), because an interface is a language its users speak, and its meaning is set by them as much as by its designers.
- Learning this is also learning [measures and targets](measures-and-targets.md), because both are about a sign drifting from what someone meant by it, once other people start relying on it.

## Resources

1. Hyrum Wright, ["Hyrum's Law"](https://www.hyrumslaw.com/) (start here: one paragraph). <!-- verify -->
2. Titus Winters, Tom Manshreck and Hyrum Wright, [*Software Engineering at Google*](https://abseil.io/resources/swe-book), the chapters on Hyrum's law and deprecation (go deeper: free online). <!-- verify -->
3. Ludwig Wittgenstein, *Philosophical Investigations* (1953), with Ray Monk, *How to Read Wittgenstein* (2005) as a companion (the philosophical original).

## Names you'll hear

- **Hyrum's law, law of implicit interfaces:** every observable behaviour will be depended on by someone.
- **Contract, API surface:** what an interface promises, and everything it exposes.
- **Bug-for-bug compatibility:** preserving known faults because users rely on them.
- **Protocol ossification:** a protocol losing the ability to change because things in the network depend on its old shape.
- **GREASE:** deliberately sending random values so that unused parts of a protocol stay usable.
- **Deprecation:** announcing that a behaviour will go away, then helping users move off it.

## Go and look

Pick an interface you own, such as an API, a file format or a command-line tool. List three behaviours it has that you never promised: an order, a default, a message. Then find out whether anyone relies on them. The answer is usually yes.
