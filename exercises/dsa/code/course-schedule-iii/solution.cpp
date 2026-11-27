class Solution {
public:
    int scheduleCourse(vector<vector<int>>& courses) {
        // Consider courses in order of deadline: the earliest deadline first.
        sort(courses.begin(), courses.end(), [](auto& a, auto& b) { return a[1] < b[1]; });
        priority_queue<int> taken;  // durations of the courses kept so far, longest on top
        int day = 0;                // the day the kept courses finish, taken one after another
        for (auto& c : courses) {
            taken.push(c[0]);
            day += c[0];
            if (day > c[1]) {
                // Too late: drop the longest course kept so far. It frees the most time,
                // and the rest still finish in time because their deadlines are earlier.
                day -= taken.top();
                taken.pop();
            }
        }
        return taken.size();
    }
};
