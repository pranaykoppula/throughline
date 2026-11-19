# Data systems

Last reviewed: 2026-11-19

A family index. What happens to data once it outlives the program that made it: how it's shaped, written down, copied, split and moved, and what you promise people while it's doing any of those.

## In reading order

In the order the spine first needs them, with pages that lean on each other kept together.

1. [Access patterns](access-patterns.md): how data is read and written decides how it should be stored. First needed on [page 1](../01-one-machine-one-program.md).
2. [Data modelling](modelling.md): deciding what things exist in your data, what facts are recorded about them, and how they relate, before the code makes it permanent. First needed on [page 4](../04-data-outlives-programs.md).
3. [Consistency](consistency.md): copies that disagree, and what you promise while they do. First needed on [page 4](../04-data-outlives-programs.md).
4. [Serialization formats](serialization.md): representing data as bytes that another program, written by someone else, can turn back into the same data. First needed on [page 5](../05-machines-need-to-talk.md).
5. [Pagination](pagination.md): showing a long, changing list a piece at a time without skipping, repeating, or slowing down. First needed on [page 6](../06-anyone-can-publish.md).
6. [Replication](replication.md): keeping copies of data on more than one machine, and deciding what happens when the main one fails. First needed on [page 8](../08-too-many-users-too-much-data.md).
7. [Partitioning](partitioning.md): splitting data across machines when one machine can't hold or serve it all. First needed on [page 8](../08-too-many-users-too-much-data.md).
8. [Data gravity](data-gravity.md): the more data you have in one place, the harder it is to move, and the more everything else moves towards it. First needed on [page 9](../09-buying-computers-is-too-slow.md).
9. [Migrations](migrations.md): changing the shape or home of data that a running system depends on, without stopping it. First needed on [page 13](../13-everything-still-exists-at-once.md).
