use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut text = String::new();
    std::io::stdin().read_to_string(&mut text).unwrap();
    let mut lines = text.split('\n');
    let s = lines.next().unwrap_or("").to_string();
    let p = lines.next().unwrap_or("").to_string();
    println!("{}", Solution::num_distinct(s, p));
}
