use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace().map(|x| x.parse::<i64>().unwrap());
    let n = it.next().unwrap() as usize;
    let buildings: Vec<Vec<i32>> = (0..n).map(|_| (0..3).map(|_| it.next().unwrap() as i32).collect()).collect();
    let mut out = String::new();
    for p in Solution::get_skyline(buildings) {
        out.push_str(&format!("{} {}\n", p[0], p[1]));
    }
    print!("{}", out);
}
