# Pushback

Last reviewed: 2026-10-24

Every solution on the spine gets adopted by people who don't have its problem. This page is for that moment, whether the proposal is someone else's or your own. The questions are also the ones to ask a colleague or Claude Code when you're out of your depth.

The other failure is just as real: refusing something you do need because change is tiring. The same questions catch both.

## The questions

1. **What problem do we have today, measured?** Not the problem we might have at ten times the users. A number, from this system.
2. **Which limit is binding, and does this move it?** If the database is the bottleneck, a faster web tier changes nothing.
3. **What's the total cost?** Learning it, running it, hiring for it, migrating to it, being locked into it, and the option we give up by spending effort here.
4. **Is it reversible?** Two-way doors get tried. One-way doors get argued.
5. **Who's recommending it, and what do they gain?** Vendors, conference speakers, and résumés all have interests. So do you.
6. **What's the boring alternative, and exactly why isn't it enough?** "It doesn't scale" isn't a reason until question 1 has an answer.
7. **What does the case that made this famous have in common with us?** Their scale, their team, their problem. Usually not much.
8. **Can we try it small, with a date to decide?** A pilot with an end date turns an argument into an experiment.

## How to deliver it

In writing, with numbers, and with an alternative attached. Keep "not now" separate from "never": most good ideas are early, not wrong. Say what would change your mind. The aim is a decision everyone can live with, not a win.

## Control vs ease, as a reading

Most proposals move up or down the ladder: towards building it yourself (more control) or towards renting someone else's (more ease). Reading cases by direction helps.

- **Down, justified:** a hand-built thing at a scale nothing on sale could serve. Dropbox's own storage, Stack Overflow's hand-tuned SQL, Figma's rendering engine, Twitter's move to the JVM.
- **Up, justified:** handing a layer to someone who runs it better, to spend effort on what nobody sells. Netflix on AWS; self-hosted databases moved to managed ones.
- **Down, too early:** not-invented-here, and optimizing before measuring.
- **Never down:** paying an abstraction's cost forever because nobody measured it. ORM queries at scale are the usual example.

The right rung moves over time. What had to be built ten years ago is a product now, and someone else maintains it ([13](13-everything-still-exists-at-once.md)).

## Names you'll hear

- **Second-system effect** (Brooks): the follow-up to a successful system tends to be overdesigned with everything left out of the first.
- **Hyrum's law:** with enough users, every observable behaviour of a system is depended on by somebody.
- **Worse is better** (Gabriel): the simpler, less correct thing often spreads faster and wins.
- **Innovation tokens** (McKinley): a team can afford only a few new technologies at once; spend them where they matter.
- **One-way door** (Bezos): a decision that's expensive or impossible to undo.

## Resources

- Dan McKinley, ["Choose Boring Technology"](https://mcfunley.com/choose-boring-technology) (start here). <!-- verify -->
- Oz Nova, ["You Are Not Google"](https://blog.bradfieldcs.com/you-are-not-google-84912cf44afb). <!-- verify -->
- Jeff Bezos, [2015 letter to shareholders](https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm): one-way and two-way doors. <!-- verify -->
- Fred Brooks, ["No Silver Bullet"](https://www.cs.unc.edu/techreports/86-020.pdf) (1986). <!-- verify -->
- Joel Spolsky, ["Things You Should Never Do, Part I"](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/): on rewrites. <!-- verify -->
- Clayton Christensen, *The Innovator's Dilemma* (1997), for the mirror failure: refusing the new thing until it's too late.
- The Gartner [hype cycle](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle). It's a marketing artifact, but the shape is real. <!-- verify -->

Cases of the misuse itself, such as Segment's microservices and Prime Video's consolidation, are on [page 8](08-too-many-users-too-much-data.md).
