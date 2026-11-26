use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace().map(|x| x.parse::<i64>().unwrap());
    let n = it.next().unwrap() as usize;
    let k = it.next().unwrap() as i32;
    let nums: Vec<i32> = (0..n).map(|_| it.next().unwrap() as i32).collect();
    println!("{}", Solution::split_array(nums, k));
}
