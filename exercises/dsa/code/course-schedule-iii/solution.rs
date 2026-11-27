use std::collections::BinaryHeap;

impl Solution {
    pub fn schedule_course(mut courses: Vec<Vec<i32>>) -> i32 {
        // Consider courses in order of deadline: the earliest deadline first.
        courses.sort_by_key(|c| c[1]);
        let mut taken = BinaryHeap::new(); // durations of the courses kept so far, longest on top
        let mut day = 0; // the day the kept courses finish, taken one after another
        for c in &courses {
            taken.push(c[0]);
            day += c[0];
            if day > c[1] {
                // Too late: drop the longest course kept so far. It frees the most time,
                // and the rest still finish in time because their deadlines are earlier.
                day -= taken.pop().unwrap();
            }
        }
        taken.len() as i32
    }
}
