use std::io::Read;

include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace();
    let mut cache = LFUCache::new(it.next().unwrap().parse().unwrap());
    let mut out = String::new();
    while let Some(op) = it.next() {
        let k: i32 = it.next().unwrap().parse().unwrap();
        if op == "get" {
            out.push_str(&format!("{}\n", cache.get(k)));
        } else {
            let v: i32 = it.next().unwrap().parse().unwrap();
            cache.put(k, v);
        }
    }
    print!("{}", out);
}
