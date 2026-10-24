# Data modelling

Last reviewed: 2026-10-24

A concept page: deciding what things exist in your data, what facts are recorded about them, and how they relate, before the code makes it permanent.

## Problem

Every system encodes a picture of the world in its data: what an order is, what a person has, how an event relates to a place. That picture is usually drawn quickly, from the first few cases, and the real world turns out to be more varied. Because data outlives programs, a model that can't represent reality forces every later program to work around it.

## The story

In 2008 Yasmin Farouk built the backend for a startup selling concert tickets. The data model was obvious: an event had a name, a venue, a date and a time, and tickets belonged to an event. It covered every concert in the first year, and the code was simple because the model was.

Then the company signed a music festival. Three days, five stages, and two hundred performances, some of which sold separate tickets and some of which were covered by a weekend pass. The model had no way to say any of it. An event had one date and one venue. The team created a separate "event" for each day, then for each stage, then added a text field called `notes` where they wrote things like "part of weekend pass". Then a touring band wanted one listing for thirty cities. Then a venue changed its name. Each new case was squeezed into the model with another field or another convention, and the code grew conditions to interpret them. Two years later the ticketing code was mostly exceptions, and nobody could answer simple questions, like how many people had tickets for a given night, without a spreadsheet.

*Before reading on: the model had been right for concerts and wrong for everything that came after. How would you have modelled it, knowing only what Yasmin knew in 2008?*

When Yasmin rebuilt it, she started from the real things in the business rather than from the first screen. A *performance* was one act at one place and time. A *venue* was a place, with its own history of names. An *event* was something with a name that grouped performances: a single concert, a festival, a tour. A *ticket product* was what people bought, which could grant entry to one performance or many. Each fact lived in one place. A concert was now just an event with one performance and one ticket product, so the simple case stayed simple. The festival and the tour needed no special fields at all.

She also changed how the team started new features. Before designing tables, they wrote down the questions the business would ask of the data, and two or three awkward real cases that the model had to be able to say.

Looking back, Yasmin thought the first model hadn't been careless. It had been drawn from the only examples she had. The lesson was to model the things in the world, not the first screen that showed them, and to go looking for awkward cases before the data made the model permanent.

## Where it shows up

| Page | The model | What it couldn't say |
| --- | --- | --- |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Walter's tree, shaped for monthly statements | Questions that started from a hospital, not a customer. |
| [Access patterns](access-patterns.md) | Storage shaped by how data is used | The model decides what can be stored; access patterns decide how. |
| [State machines](../dsa/state-machines.md) | Chloe's orders as a set of flags | Which combinations were possible; nine named states could. |
| [Labels and training data](labels.md) | What gets recorded about each example | A model can only learn from what was written down. |

It shows up elsewhere too: names, addresses, currencies, time zones and anything that seemed simple in the first country a product launched in.

What these share is that a data model is a claim about the world, and the world keeps testing it.

## It really happened

Yasmin is fictional. Peter Chen's entity–relationship model (1976) gave the field a way to draw things and their relationships before building tables. Codd's normal forms, from the early 1970s, gave rules for storing each fact once so copies can't disagree ([page 4](../04-data-outlives-programs.md)). Patrick McKenzie's 2010 essay "Falsehoods Programmers Believe About Names" listed dozens of assumptions, such as that people have exactly one name, or a first and last name, or that names don't change, each of which a real person breaks. It started a long series of similar lists, about addresses, time and more.

## What it is

Data modelling identifies the entities in a domain, the attributes recorded about each, and the relationships between them, and then decides how to store them. Good models follow the real-world things rather than one screen or report, store each fact once, separate things that change independently, and are tested against awkward real cases before they're built. The choice of type for each field, such as money, dates or IDs, is part of the model.

## Where it gets misapplied

- **Modelling the first screen.** Yasmin's event with one date.
- **A `notes` field for everything that doesn't fit.** Meaning moves out of the data and into people's heads.
- **Assuming the simple case is universal.** One name, one address, one currency, one time zone.
- **The mirror:** modelling every conceivable future case on day one. An over-general model is hard to use and hard to understand. Look for real awkward cases, not imagined ones.

## Connections

- Learning this is also learning [access patterns](access-patterns.md), because the model decides what can be stored and the patterns decide how it's arranged.
- Learning this is also learning [state machines](../dsa/state-machines.md), because many entities have lifecycles that are part of the model.
- Learning this is also learning [migrations](migrations.md), because changing a model that's already full of data is a migration.
- Learning this is also learning [type systems](../runtimes/type-systems.md), because a schema is the model written down for a machine to check.
- Learning this is also learning [floating point](../math/floating-point.md), because choosing how to store money is a modelling decision.

## Resources

1. Martin Kleppmann, [*Designing Data-Intensive Applications*](https://dataintensive.net/), chapter 2, "Data Models and Query Languages" (start here).
2. Patrick McKenzie, "Falsehoods Programmers Believe About Names" (2010) (go deeper: short and humbling).
3. Peter Chen, "The Entity-Relationship Model: Toward a Unified View of Data" (1976) (reference).

## Names you'll hear

- **Entity, attribute, relationship:** a thing, a fact about it, and how things connect.
- **Schema:** the model written down for the database.
- **Normalisation:** storing each fact once.
- **Denormalisation:** deliberately copying facts for faster reads, accepting the cost of keeping them in step.
- **Domain model:** the model of the business itself, independent of storage.

## Go and look

Pick one central table in a system you work on and find its "notes", "misc" or "extra" field. Read twenty rows of it. Each one is something the model couldn't say.
