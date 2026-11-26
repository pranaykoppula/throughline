package main

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
