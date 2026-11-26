use std::io::Read;

include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut finder = MedianFinder::new();
    let mut out = String::new();
    let mut it = s.split_whitespace();
    while let Some(op) = it.next() {
        if op == "add" {
            let x: i32 = it.next().unwrap().parse().unwrap();
            finder.add_num(x);
        } else {
            out.push_str(&format!("{:.5}\n", finder.find_median()));
        }
    }
    print!("{}", out);
}
