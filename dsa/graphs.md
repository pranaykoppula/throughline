# Graphs

Last reviewed: 2026-10-24

A concept page: things and the connections between them, and the questions you can ask of any network.

## Problem

A great deal of what software tracks is really a network: roads between places, machines connected by cables, programs waiting on each other, people following people, commits built on earlier commits. Stored as tables or lists, the network is hard to reason about. Seen as a graph, a few standard questions answer most problems: what's the shortest path, is there a cycle, what can reach what?

## The story

In 1998 Ruth Nkemelu wrote the route planner for a courier company in Leeds. Each morning drivers got a list of drops, and the planner put them in an order and told each driver the distance between stops. Ruth's first design was straightforward. Every night, a program worked out the driving distance between every pair of addresses the company had ever delivered to and stored them all in a big table. In the morning, looking up a distance was instant.

It worked for a year, while the company knew a few thousand addresses. Then it won a contract with a catalogue retailer, and the address list grew to forty thousand. Forty thousand addresses meant eight hundred million pairs. The nightly job stopped finishing by morning, and the table filled the disk. Worse, when a road closed for repairs, every distance that used it was wrong until the next night's run, and drivers were sent down closed streets.

*Before reading on: the table of every distance had become too big to build and too slow to change. What would you have stored instead?*

Ruth stopped storing answers and started storing the network. Each junction became a point, each stretch of road between junctions a line with a length, about ninety thousand lines for the whole city. When the planner needed a distance, it worked it out on the spot. It started from the first address, and always extended the shortest route found so far, one road at a time, until it reached the second. Kept in a priority queue, the routes still to explore came out in order of length, and a typical query touched a few thousand roads and finished in a fraction of a second. A closed road was one line removed, and every route avoided it immediately.

Looking back, Ruth thought she'd made the classic mistake of storing every answer to a question when she could store the thing the question was about. A table of distances was a picture of the city on one night. The graph was the city.

## Where it shows up

| Page | The graph | The question asked of it |
| --- | --- | --- |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | Jobs and the tape drives they hold and want | Is there a cycle? A cycle is a deadlock. |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Machines and the links between them | What's the shortest path for this packet? That's routing. |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | Commits and the commits they're built on | What's the common ancestor of these two branches? That's how a merge starts. |
| [State machines](state-machines.md) | States and the allowed moves between them | Can this state be reached from that one? |
| [Queues](queues.md) | Any graph, explored level by level | Breadth-first search keeps a queue of places to visit next. |

It shows up elsewhere too: social networks, dependency trees in package managers, build systems deciding what to rebuild, recommendation systems, and maps.

The pages share a small set of questions that turn up in very different clothes: paths, cycles, reachability and ordering. Spotting that a problem is a graph question usually means a well-known algorithm already solves it.

## It really happened

Ruth is fictional; her algorithm isn't. Edsger Dijkstra devised his shortest-path method in 1956 to demonstrate a new computer in Amsterdam, using a map of Dutch cities, and published it in 1959. He later said he'd worked it out in about twenty minutes, sitting at a café, without pencil and paper. Graph theory itself is usually dated to 1736, when Leonhard Euler showed that nobody could walk across each of Königsberg's seven bridges exactly once, by reducing the city to points and lines. Internet routing protocols still run shortest-path algorithms over graphs of routers.

## What it is

A graph is a set of nodes connected by edges, which can have directions and weights. Standard algorithms answer the common questions: breadth-first and depth-first search for reachability, Dijkstra's algorithm and its relatives for shortest paths, cycle detection, and topological sorting for putting dependencies in order. Many problems that don't look like networks become simpler once modelled as one.

## Where it gets misapplied

- **Precomputing every answer.** Ruth's table of all distances. Store the graph and compute what's asked.
- **Building your own graph algorithm.** The standard ones are decades old and well tested; most problems need one of five.
- **A graph database because the data has relationships.** All data has relationships. Use one when the questions are about paths and connections many steps deep.
- **The mirror:** not noticing a problem is a graph at all, and writing nested loops to find what a breadth-first search would find in a few lines.

## Connections

- Learning this is also learning [queues](queues.md), because breadth-first search and Dijkstra's algorithm both run on queues.
- Learning this is also learning [state machines](state-machines.md), because a state diagram is a graph.
- Learning this is also learning [Merkle DAGs](merkle-dags.md), because git's history is a graph with no cycles, where each node is named by its content.
- Learning this is also learning [round trips](../latency/round-trips.md), because routing is choosing paths through a graph of machines, each hop a delay.
- Learning this is also learning [computability](computability.md), because some graph questions, like the shortest route visiting every city, have no known fast answer at all.

## Resources

1. Steven Skiena, *The Algorithm Design Manual*, the graph chapters (start here: organised by the problem you have).
2. Thomas Cormen et al., *Introduction to Algorithms*, the graph algorithms part (go deeper).
3. Edsger Dijkstra, "A Note on Two Problems in Connexion with Graphs" (1959) (reference: three pages).

## Names you'll hear

- **Node, edge, weight:** a point, a connection, and the cost of a connection.
- **Directed, acyclic, DAG:** edges with direction; no cycles; a directed graph without cycles.
- **BFS, DFS:** breadth-first and depth-first search.
- **Dijkstra's algorithm:** shortest paths with non-negative weights.
- **Topological sort:** ordering tasks so each comes after everything it depends on.
- **Travelling salesman problem:** the shortest route through every node, famously hard.

## Go and look

Find one thing in a system you work on that's secretly a graph, such as dependencies between services, packages or tasks, and ask one graph question of it: is there a cycle?
