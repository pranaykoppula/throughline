use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    println!("{}", Solution::calculate(s.trim_end_matches(['\n', '\r']).to_string()));
}
