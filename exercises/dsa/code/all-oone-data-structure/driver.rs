use std::io::Read;

include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace();
    let mut counts = AllOne::new();
    let mut out = String::new();
    while let Some(op) = it.next() {
        match op {
            "inc" => counts.inc(it.next().unwrap().to_string()),
            "dec" => counts.dec(it.next().unwrap().to_string()),
            "max" => out.push_str(&format!("\"{}\"\n", counts.get_max_key())),
            _ => out.push_str(&format!("\"{}\"\n", counts.get_min_key())),
        }
    }
    print!("{}", out);
}
