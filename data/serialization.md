# Serialization formats

Last reviewed: 2026-10-24

A concept page: turning data into bytes that another program, written by someone else, can turn back into the same data.

## Problem

Data inside a program is a web of objects in memory. To send it over a network or save it to disk, it has to become a flat sequence of bytes, and the program on the other side has to agree on exactly what those bytes mean. The agreement outlives both programs, and the two sides change at different times.

## The story

In 2007 Jonas Becker worked at a logistics company whose systems were all written in Java. When one service needed to send data to another, such as a shipment, a customer or an invoice, it used the language's built-in serialization. Hand it any object, and it produced bytes; hand the bytes to the other side, and out came the same object. No formats to design, no parsing to write. It was the obvious choice, and it worked on the first try.

Two years later it started to hurt. The billing team added a field to the invoice class and deployed on a Tuesday. The warehouse service, which hadn't been redeployed, could no longer read any invoice at all, and stopped. The fix was to deploy every service that touched invoices at the same moment, which meant every change to a shared class became a company-wide event scheduled weeks ahead. A partner company asked to receive shipment data, and Jonas had to explain that the format was, in effect, "whatever Java does with our classes", which their Python systems couldn't read.

Then, in 2015, a security researcher showed that Java's built-in deserialization could be made to run arbitrary code if an attacker controlled the bytes. Several of Jonas's services accepted serialized objects from the network. He spent a very long week finding them all.

*Before reading on: the format had been free to adopt, and it tied every service to every other, locked out partners, and let strangers run code. What would you have chosen instead?*

Jonas moved the services, one interface at a time, to an explicit format with a written schema. Every message type was described in a file that both sides shared: each field had a name, a type and a number. The rules for changing it were simple and strict. You could add a new field with a new number, and old readers would ignore it. You could stop using a field, but never reuse its number. Services could now be deployed in any order, because each could read messages written by older or newer versions. The partner generated a Python reader from the same schema file. And because parsing only ever produced plain data, never live objects, a malicious message could at worst be rejected.

Looking back, Jonas thought the built-in format had felt free because its cost was deferred. Every message between services was a contract, whether or not anyone wrote it down. The format just decided whether the contract was visible, versioned, and safe to read from strangers.

## Where it shows up

| Page | The format | The lesson |
| --- | --- | --- |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Everything on the wire | Both sides must agree on what the bytes mean, though they can't see each other. |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | A partner bank's file format, changed with two weeks' notice | Contract drift: two sides of an interface changing separately. |
| [Input validation](../auth/input-validation.md) | Parsing input from outside | A format that can carry code is a format strangers can attack. |
| [Round trips](../latency/round-trips.md) | What goes in each exchange | Size and shape of the payload are the other half of a request's cost. |
| [State machines](../dsa/state-machines.md) | Parsers | Reading a format is usually a state machine consuming one piece at a time. |

It shows up elsewhere too: file formats that outlive the programs that wrote them, configuration files, database storage formats, and APIs between companies.

What these share is that a format is an agreement between parties who change at different times. The good ones say how they're allowed to change.

## It really happened

Jonas is fictional; his week in 2015 wasn't unusual. In 2015 researchers at FoxGlove Security published working attacks using Java deserialization against widely used software including WebLogic, WebSphere, JBoss and Jenkins, and vendors spent months patching ([one record](https://www.tenable.com/blog/critical-oracle-weblogic-server-flaw-still-not-patched)). Google had released Protocol Buffers, its internal schema-based format with numbered fields, as open source in 2008. The costliest disagreement about what numbers mean may be NASA's Mars Climate Orbiter, lost in 1999 because one team's software produced thruster data in pound-force seconds and the navigation software read it as newton-seconds. The units were never written into the interface.

## What it is

Serialization turns in-memory data into bytes; deserialization turns them back. A format, such as JSON, XML, CSV, Protocol Buffers or Avro, is the agreement about how. Text formats are readable and loose; schema-based binary formats are compact and strict. What matters most over time is how a format handles change, so that old and new versions of a program can read each other's data, and whether reading untrusted bytes can only ever produce data, not run code.

## Where it gets misapplied

- **Language-native serialization between services.** Jonas's first design: free on day one, then tying every deploy together and unsafe with untrusted input.
- **No versioning rules.** Renaming or reusing fields breaks every reader that wasn't changed at the same moment.
- **Units and meanings left implicit.** A field called `amount` with no currency, or `impulse` with no unit.
- **The mirror:** a heavy schema system for a script that writes one file read by one program. JSON is fine.

## Connections

- Learning this is also learning [input validation](../auth/input-validation.md), because parsing is where strangers' bytes first meet your code.
- Learning this is also learning [migrations](migrations.md), because changing a format that's already stored is a migration.
- Learning this is also learning [state machines](../dsa/state-machines.md), because parsers are state machines.
- Learning this is also learning [round trips](../latency/round-trips.md), because a compact format makes each exchange cheaper.
- Learning this is also learning [type systems](../runtimes/type-systems.md), because a schema is a type that crosses a boundary between programs.

## Resources

1. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapter 4, "Encoding and Evolution" (start here: exactly this page).
2. The Protocol Buffers documentation on updating message types (go deeper: compatibility rules spelled out).
3. NASA, Mars Climate Orbiter Mishap Investigation Board Phase I Report (1999) (reference).

## Names you'll hear

- **Serialize, deserialize, marshal:** turning data into bytes and back.
- **Schema:** the written description of a format.
- **Backward and forward compatibility:** new code reading old data, and old code reading new data.
- **JSON, Protocol Buffers, Avro:** a text format, and two schema-based binary ones.
- **Deserialization vulnerability:** a format that lets bytes choose what code runs.

## Go and look

Find one message or file that two of your programs exchange and ask what happens if one side adds a field and deploys first. If nobody knows, try it somewhere safe.
