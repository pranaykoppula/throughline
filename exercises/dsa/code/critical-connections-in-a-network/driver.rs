use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace().map(|x| x.parse::<i32>().unwrap());
    let n = it.next().unwrap();
    let m = it.next().unwrap() as usize;
    let edges: Vec<Vec<i32>> = (0..m).map(|_| vec![it.next().unwrap(), it.next().unwrap()]).collect();
    let mut out: Vec<(i32, i32)> = Solution::critical_connections(n, edges)
        .iter()
        .map(|e| (e[0].min(e[1]), e[0].max(e[1])))
        .collect();
    out.sort();
    let mut text = String::new();
    for (a, b) in out {
        text.push_str(&format!("{} {}\n", a, b));
    }
    print!("{}", text);
}
