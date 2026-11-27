import java.util.Arrays;
import java.util.Collections;
import java.util.PriorityQueue;

class Solution {
    public int scheduleCourse(int[][] courses) {
        // Consider courses in order of deadline: the earliest deadline first.
        Arrays.sort(courses, (a, b) -> Integer.compare(a[1], b[1]));
        // Durations of the courses kept so far, longest on top.
        PriorityQueue<Integer> taken = new PriorityQueue<>(Collections.reverseOrder());
        int day = 0;  // the day the kept courses finish, taken one after another
        for (int[] c : courses) {
            taken.add(c[0]);
            day += c[0];
            if (day > c[1]) {
                // Too late: drop the longest course kept so far. It frees the most time,
                // and the rest still finish in time because their deadlines are earlier.
                day -= taken.poll();
            }
        }
        return taken.size();
    }
}
