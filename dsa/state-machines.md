# State machines

Last reviewed: 2026-10-24

A concept page: naming every state something can be in, and every allowed way to move between them.

## Problem

Most things a program tracks move through stages: an order is placed, paid, shipped, delivered, perhaps cancelled or refunded. Tracked loosely, with a handful of separate flags, they can end up in combinations that make no sense, and nobody notices until a customer does.

## The story

In 2012 Chloe Bennett worked on the order system at an online furniture shop. Each order had a few yes-or-no fields: paid, shipped, cancelled, refunded. Whatever code needed to change an order set the relevant field. It was simple and flexible, and when a new step came along, such as "awaiting stock", someone added another field.

In the run-up to a sale, the warehouse shipped a sofa to a customer who had cancelled it two days earlier. Then another. Chloe went looking and found forty orders marked both *cancelled* and *shipped*, eleven marked *refunded* but not *paid*, and three that were *paid*, *cancelled* and *awaiting stock* all at once. Each field had been set by some piece of code that was correct on its own terms. The cancellation code set *cancelled*. The warehouse code, which checked *paid* but not *cancelled*, set *shipped*. Nothing anywhere said which combinations were possible, so every combination was.

*Before reading on: every piece of code was right about its own field, and the orders ended up in impossible states. What would you have changed?*

Chloe replaced the fields with one: the order's state. She drew every state an order could really be in on a whiteboard, nine of them, and every arrow between them that the business actually allowed. Placed could go to paid or cancelled. Paid could go to awaiting stock, packing, or cancelled-and-refunded. Shipped could never go back to cancelled; it could only go to delivered or returned. Then she wrote one function that every change went through. Given the current state and the requested move, it either made the move or refused it. The warehouse could no longer ship a cancelled order, because there was no arrow from cancelled to shipped.

She also had the function record every move, with the time and what asked for it. Questions that used to take an afternoon of digging, such as *why was this refunded?*, now took a glance at the order's history.

Looking back, Chloe thought the flags had let everyone describe their own part of an order's life and nobody describe the whole. Drawing the states and arrows had been an afternoon's work, and the arguments it started with the business about which arrows should exist were the most useful conversations she had all year.

## Where it shows up

| Page | The states | What the arrows prevented |
| --- | --- | --- |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | A TCP connection: listening, connecting, established, closing | Both machines always agree on what the next message should be, though they can't see each other. |
| [Consistency](../data/consistency.md) | Copies of a database applying the same changes | If every copy starts in the same state and applies the same moves in the same order, they end in the same state. |
| [6, Anyone can publish](../06-anyone-can-publish.md) | A booking: free, held, booked | The server refused a move from booked to booked, which ended Hannah's double bookings. |

It shows up elsewhere too: parsers reading text one character at a time, traffic lights, user interfaces with modes, workflow and approval systems, and game characters.

What these share is the same discipline: name the states, name the allowed moves, and refuse everything else. It turns a pile of flags into something both people and machines can check.

## It really happened

Chloe is fictional; TCP's state diagram is real and famous. The 1981 specification, RFC 793, defines a connection as a set of named states and the events that move it between them. That's how two machines that can't see each other stay in step ([page 5](../05-machines-need-to-talk.md)). Building reliable replicated systems the same way, by having every copy apply the same commands in the same order to the same starting state, was set out by Leslie Lamport in 1978 and explained in Fred Schneider's tutorial "Implementing Fault-Tolerant Services Using the State Machine Approach" (*ACM Computing Surveys*, 1990) ([copy](https://pdos.csail.mit.edu/archive/6.824-2007/papers/schneider-rsm.pdf)).

## What it is

A state machine is a model of something that is always in exactly one of a fixed set of states, and moves between them only along defined transitions, triggered by events. Making it explicit in code means one place decides whether a move is allowed, impossible states can't be represented, and every move can be recorded. Replicating a state machine, with the same start and the same moves in the same order, is one of the main ways to keep copies consistent.

## Where it gets misapplied

- **A flag for every stage.** Chloe's first design: every combination becomes possible, including the impossible ones.
- **Moves scattered through the code.** If any function can set the state directly, the diagram is a wish, not a rule.
- **A state machine for something with no real stages.** Not everything has a lifecycle; forcing one adds ceremony without safety.
- **The mirror:** a diagram so detailed nobody can read it. If it needs fifty states, it may be several machines.

## Connections

- Learning this is also learning [consistency](../data/consistency.md), because copies that apply the same moves in the same order stay identical.
- Learning this is also learning [graphs](graphs.md), because a state machine is a graph of states and arrows, and graph questions, like "can this state be reached?", apply to it.
- Learning this is also learning [serialization formats](../data/serialization.md), because parsing a format is usually a state machine reading one piece at a time.
- Learning this is also learning [input validation](../auth/input-validation.md), because refusing moves that aren't on the diagram is validating what a request is allowed to do.
- Learning this is also learning [migrations](../data/migrations.md), because moving data into a new design often starts with untangling which states the old data was really in.

## Resources

1. Any introduction to finite state machines; the [Wikipedia article](https://en.wikipedia.org/wiki/Finite-state_machine) is a reasonable start.
2. [RFC 793](https://www.rfc-editor.org/rfc/rfc793) (1981), TCP's original specification, for its state diagram (go deeper). <!-- verify -->
3. Fred Schneider, ["Implementing Fault-Tolerant Services Using the State Machine Approach"](https://pdos.csail.mit.edu/archive/6.824-2007/papers/schneider-rsm.pdf) (1990) (reference).

## Names you'll hear

- **State, transition, event:** where something is, a move it can make, and what triggers the move.
- **Finite state machine (FSM):** one with a fixed number of states.
- **State diagram:** the picture of states and arrows.
- **Replicated state machine:** copies kept identical by applying the same moves in the same order.
- **Event sourcing:** storing the history of moves rather than just the current state.

## Go and look

Find something in a system you work on that has a lifecycle, such as an order, an account or a job, and draw its states and arrows. Then check whether the code enforces your drawing, or merely hopes for it.
