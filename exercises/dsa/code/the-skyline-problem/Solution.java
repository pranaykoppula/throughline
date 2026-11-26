import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.TreeSet;

class Solution {
    public List<List<Integer>> getSkyline(int[][] buildings) {
        // Every place the outline can change: a building's left or right edge.
        TreeSet<Integer> edges = new TreeSet<>();
        for (int[] b : buildings) {
            edges.add(b[0]);
            edges.add(b[1]);
        }
        List<List<Integer>> skyline = new ArrayList<>();
        // {height, right edge} of buildings that have started; tallest on top.
        PriorityQueue<int[]> standing = new PriorityQueue<>((p, q) -> Integer.compare(q[0], p[0]));
        int i = 0;
        for (int x : edges) {
            // Buildings that start here join the heap (the input is sorted by left edge).
            while (i < buildings.length && buildings[i][0] <= x) {
                standing.add(new int[] {buildings[i][2], buildings[i][1]});
                i++;
            }
            // The tallest might have ended already; drop it only when it's on top.
            while (!standing.isEmpty() && standing.peek()[1] <= x) {
                standing.poll();
            }
            int height = standing.isEmpty() ? 0 : standing.peek()[0];
            if (skyline.isEmpty() || skyline.get(skyline.size() - 1).get(1) != height) {
                skyline.add(List.of(x, height));
            }
        }
        return skyline;
    }
}
