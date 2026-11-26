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
