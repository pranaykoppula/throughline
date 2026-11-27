struct Solution;
include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_line(&mut s).unwrap();
    let s = s.trim_end_matches('\n').to_string();
    println!("{}", if Solution::is_number(s) { "true" } else { "false" });
}
