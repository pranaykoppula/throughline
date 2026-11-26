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
