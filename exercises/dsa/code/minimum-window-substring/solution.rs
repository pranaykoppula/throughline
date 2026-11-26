impl Solution {
    pub fn min_window(s: String, t: String) -> String {
        let s = s.as_bytes();
        // How many of each event the window still needs; negative means spare.
        let mut need = [0i32; 128];
        for &c in t.as_bytes() {
            need[c as usize] += 1;
        }
        let mut missing = t.len(); // total events still needed, repeats included
        let (mut best_start, mut best_len, mut left) = (0usize, usize::MAX, 0usize);
        for right in 0..s.len() {
            // Taking in one more event.
            let c = s[right] as usize;
            if need[c] > 0 {
                missing -= 1;
            }
            need[c] -= 1;
            // While the window has everything, shrink it from the left.
            while missing == 0 {
                if right - left + 1 < best_len {
                    best_start = left;
                    best_len = right - left + 1;
                }
                let g = s[left] as usize;
                need[g] += 1;
                if need[g] > 0 {
                    missing += 1;
                }
                left += 1;
            }
        }
        if best_len == usize::MAX {
            String::new()
        } else {
            String::from_utf8(s[best_start..best_start + best_len].to_vec()).unwrap()
        }
    }
}
