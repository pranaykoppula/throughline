use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).unwrap();
    let mut it = input.split_whitespace();
    let s = it.next().unwrap().to_string();
    let t = it.next().unwrap().to_string();
    println!("{}", Solution::min_window(s, t));
}
