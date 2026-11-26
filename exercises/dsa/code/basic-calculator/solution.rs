impl Solution {
    pub fn calculate(s: String) -> i32 {
        let mut total: i64 = 0; // the running total inside the current brackets
        let mut sign: i64 = 1; // the sign in front of the number being read
        let mut number: i64 = 0; // the number being read, digit by digit
        let mut saved: Vec<(i64, i64)> = Vec::new(); // (total, sign) outside each open bracket
        for ch in s.chars() {
            match ch {
                '0'..='9' => number = number * 10 + ch.to_digit(10).unwrap() as i64,
                '+' | '-' => {
                    total += sign * number;
                    number = 0;
                    sign = if ch == '+' { 1 } else { -1 };
                }
                '(' => {
                    // Put the outside aside, and start a fresh total inside.
                    saved.push((total, sign));
                    total = 0;
                    sign = 1;
                }
                ')' => {
                    total += sign * number;
                    number = 0;
                    // Fold the bracket's total back into the outside.
                    let (outside, outside_sign) = saved.pop().unwrap();
                    total = outside + outside_sign * total;
                }
                _ => {}
            }
        }
        (total + sign * number) as i32
    }
}
