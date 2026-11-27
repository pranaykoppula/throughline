use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace().map(|x| x.parse::<i32>().unwrap());
    let n = it.next().unwrap() as usize;
    let courses: Vec<Vec<i32>> = (0..n).map(|_| vec![it.next().unwrap(), it.next().unwrap()]).collect();
    println!("{}", Solution::schedule_course(courses));
}
