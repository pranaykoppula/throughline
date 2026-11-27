# The cable you can't lose

An exercise in the category **what connects to what**. It's LeetCode 1192, [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/), rated Hard.

## The situation

A company runs its servers across several buildings, joined by network cables. Over the years cables were added wherever they were needed, and nobody has a clear picture of which ones matter. Before a contractor digs up a car park, the network team wants a list of every cable whose loss alone would cut some servers off from the rest. Those are the cables that need a second route laid before anyone picks up a spade. The network has a hundred thousand servers.

## The problem

You're given *n* servers, numbered 0 to *n* − 1, and a list of undirected connections between pairs of them. The network is connected. A connection is critical if removing it leaves some server unable to reach some other. Return every critical connection, in any order.

For four servers with connections `0-1`, `1-2`, `2-0` and `1-3`, the only critical connection is `1-3`: the other three form a ring, so losing any one of them leaves a way round.

## The question it asks

"What connects to what, and through which link?" The network is a [graph](../../dsa/graphs.md), and a critical connection is what graph theory calls a bridge: an edge that lies on no cycle. See the row for what connects to what in [choosing a data structure](../../dsa/choosing.md).

## The tempting first answer

Remove each connection in turn, and walk the network to see whether it's still in one piece. It's correct, and it's exactly the question being asked. But each walk visits every server and connection, and there's one walk per connection, so the work grows with the square of the network's size ([growth](../../dsa/growth.md)): for a hundred thousand servers and as many cables, about ten billion steps.

## Hints

<details markdown="1"><summary>Hint 1</summary>

A connection is critical exactly when it isn't part of any loop. A single depth-first walk of the network finds loops: whenever it reaches a server it has already visited, by a connection other than the one it came in on, it has closed a loop.

</details>

<details markdown="1"><summary>Hint 2</summary>

Number the servers in the order the walk first reaches them. For each server, work out the earliest-numbered server that anything below it in the walk can reach by one connection that goes back up. How does that tell you whether the connection into it is on a loop?

</details>

<details markdown="1"><summary>Hint 3</summary>

If nothing below a server *v* can reach back to *v*'s parent or anywhere earlier, then the connection from the parent to *v* is the only way in, and it's critical.

</details>

## Solution

<details markdown="1"><summary>Show the solution</summary>

One depth-first walk, keeping two numbers for each server:

- `found[v]`, when the walk first reached *v*, counting up from 0;
- `low[v]`, the earliest `found` number that *v*, or anything the walk reached from *v*, can touch by one connection back up the walk.

Walk from server 0. At server *u*, for each neighbour *v* other than the one you came from:

1. **If *v* is new,** walk into it. When the walk comes back, `low[u] = min(low[u], low[v])`. Then, if `low[v] > found[u]`, nothing below *v* reaches *u* or earlier, so `u-v` is critical.
2. **If *v* was already reached,** it's earlier in the walk, and this connection closes a loop: `low[u] = min(low[u], found[v])`.

**Why it works:** in a depth-first walk of an undirected graph, every connection that isn't part of the walk's own tree goes from a server back to one of its ancestors. So a loop through the connection `u-v` must come back up from somewhere below *v* to *u* or above, and `low[v]` records the highest that any such route reaches. Robert Tarjan published this method in 1974; it uses the same kind of walk as his 1972 method for finding strongly connected components in directed graphs.

**About the Python version:** the walk goes as deep as the longest chain of servers, and Python stops recursion at about a thousand levels by default. The Python solution keeps its own stack of servers, each with the position of the next connection to try, which is what the recursion does behind the scenes in the other languages.

**Time:** proportional to the servers plus the connections. **Memory:** proportional to the same.

<!-- code:start -->
<div class="code-tabs" markdown="1">

<details markdown="1"><summary>Python</summary>

```python
from typing import List


class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        links = [[] for _ in range(n)]
        for a, b in connections:
            links[a].append(b)
            links[b].append(a)
        found = [-1] * n   # when each server was first reached in the walk
        low = [0] * n      # the earliest server reachable from its subtree by a back route
        bridges = []
        clock = 0
        # A depth-first walk, written with an explicit stack because Python limits recursion.
        for root in range(n):
            if found[root] != -1:
                continue
            found[root] = low[root] = clock
            clock += 1
            stack = [(root, -1, 0)]   # (server, the server we came from, next link to try)
            while stack:
                u, parent, i = stack[-1]
                if i < len(links[u]):
                    stack[-1] = (u, parent, i + 1)
                    v = links[u][i]
                    if v == parent:
                        continue
                    if found[v] == -1:
                        found[v] = low[v] = clock
                        clock += 1
                        stack.append((v, u, 0))
                    else:
                        low[u] = min(low[u], found[v])   # a back route to an earlier server
                else:
                    stack.pop()
                    if parent != -1:
                        low[parent] = min(low[parent], low[u])
                        # Nothing below u reaches back above it: the link is critical.
                        if low[u] > found[parent]:
                            bridges.append([parent, u])
        return bridges
```

</details>

<details markdown="1"><summary>C++</summary>

```cpp
class Solution {
    vector<vector<int>> links, bridges;
    vector<int> found, low;  // when each server was first reached; earliest reachable by a back route
    int clock = 0;

    void walk(int u, int parent) {
        found[u] = low[u] = clock++;
        for (int v : links[u]) {
            if (v == parent) continue;
            if (found[v] == -1) {
                walk(v, u);
                low[u] = min(low[u], low[v]);
                // Nothing below v reaches back above it: the link is critical.
                if (low[v] > found[u]) bridges.push_back({u, v});
            } else {
                low[u] = min(low[u], found[v]);  // a back route to an earlier server
            }
        }
    }

public:
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        links.assign(n, {});
        for (auto& e : connections) {
            links[e[0]].push_back(e[1]);
            links[e[1]].push_back(e[0]);
        }
        found.assign(n, -1);
        low.assign(n, 0);
        for (int i = 0; i < n; i++)
            if (found[i] == -1) walk(i, -1);
        return bridges;
    }
};
```

</details>

<details markdown="1"><summary>Java</summary>

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    private List<Integer>[] links;
    private int[] found, low;  // when each server was first reached; earliest reachable by a back route
    private int clock = 0;
    private final List<List<Integer>> bridges = new ArrayList<>();

    @SuppressWarnings("unchecked")
    public List<List<Integer>> criticalConnections(int n, List<List<Integer>> connections) {
        links = new List[n];
        for (int i = 0; i < n; i++) links[i] = new ArrayList<>();
        for (List<Integer> e : connections) {
            links[e.get(0)].add(e.get(1));
            links[e.get(1)].add(e.get(0));
        }
        found = new int[n];
        low = new int[n];
        Arrays.fill(found, -1);
        for (int i = 0; i < n; i++)
            if (found[i] == -1) walk(i, -1);
        return bridges;
    }

    private void walk(int u, int parent) {
        found[u] = low[u] = clock++;
        for (int v : links[u]) {
            if (v == parent) continue;
            if (found[v] == -1) {
                walk(v, u);
                low[u] = Math.min(low[u], low[v]);
                // Nothing below v reaches back above it: the link is critical.
                if (low[v] > found[u]) bridges.add(List.of(u, v));
            } else {
                low[u] = Math.min(low[u], found[v]);  // a back route to an earlier server
            }
        }
    }
}
```

</details>

<details markdown="1"><summary>Go</summary>

```go
func criticalConnections(n int, connections [][]int) [][]int {
	links := make([][]int, n)
	for _, e := range connections {
		links[e[0]] = append(links[e[0]], e[1])
		links[e[1]] = append(links[e[1]], e[0])
	}
	found := make([]int, n) // when each server was first reached in the walk
	low := make([]int, n)   // the earliest server reachable from its subtree by a back route
	for i := range found {
		found[i] = -1
	}
	clock := 0
	bridges := [][]int{}
	var walk func(u, parent int)
	walk = func(u, parent int) {
		found[u], low[u] = clock, clock
		clock++
		for _, v := range links[u] {
			if v == parent {
				continue
			}
			if found[v] == -1 {
				walk(v, u)
				low[u] = min(low[u], low[v])
				// Nothing below v reaches back above it: the link is critical.
				if low[v] > found[u] {
					bridges = append(bridges, []int{u, v})
				}
			} else {
				low[u] = min(low[u], found[v]) // a back route to an earlier server
			}
		}
	}
	for i := 0; i < n; i++ {
		if found[i] == -1 {
			walk(i, -1)
		}
	}
	return bridges
}
```

</details>

<details markdown="1"><summary>Rust</summary>

```rust
impl Solution {
    pub fn critical_connections(n: i32, connections: Vec<Vec<i32>>) -> Vec<Vec<i32>> {
        let n = n as usize;
        let mut links = vec![Vec::new(); n];
        for e in &connections {
            links[e[0] as usize].push(e[1] as usize);
            links[e[1] as usize].push(e[0] as usize);
        }
        let mut found = vec![usize::MAX; n]; // when each server was first reached in the walk
        let mut low = vec![0usize; n]; // the earliest server reachable from its subtree by a back route
        let mut clock = 0;
        let mut bridges = Vec::new();
        for i in 0..n {
            if found[i] == usize::MAX {
                Self::walk(i, usize::MAX, &links, &mut found, &mut low, &mut clock, &mut bridges);
            }
        }
        bridges
    }

    fn walk(
        u: usize,
        parent: usize,
        links: &Vec<Vec<usize>>,
        found: &mut Vec<usize>,
        low: &mut Vec<usize>,
        clock: &mut usize,
        bridges: &mut Vec<Vec<i32>>,
    ) {
        found[u] = *clock;
        low[u] = *clock;
        *clock += 1;
        for &v in &links[u] {
            if v == parent {
                continue;
            }
            if found[v] == usize::MAX {
                Self::walk(v, u, links, found, low, clock, bridges);
                low[u] = low[u].min(low[v]);
                // Nothing below v reaches back above it: the link is critical.
                if low[v] > found[u] {
                    bridges.push(vec![u as i32, v as i32]);
                }
            } else {
                low[u] = low[u].min(found[v]); // a back route to an earlier server
            }
        }
    }
}
```

</details>

</div>
<!-- code:end -->

</details>

## Where people slip

- **Skipping the parent and calling it a loop.** The connection you came in on leads straight back to the parent; it isn't a second route. Skip it.
- **Testing `>=` instead of `>`.** `low[v] >= found[u]` is the test for a critical *server* (an articulation point); for a critical *connection* it's strictly greater.
- **Recursing too deep.** A long chain of servers overflows the call stack in languages with small limits; walk with an explicit stack.

## Related

- The other exercise in this category: [the rescue boat's first chance](swim-in-rising-water.md) (LeetCode 778).
- Concept pages: [graphs](../../dsa/graphs.md), [growth](../../dsa/growth.md).
- More practice of the same shape: finding critical servers (articulation points), and strongly connected components in directed graphs.
