use std::io::Read;

include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace();
    let n: usize = it.next().unwrap().parse().unwrap();
    let words: Vec<String> = (0..n).map(|_| it.next().unwrap().to_string()).collect();
    let search = WordFilter::new(words);
    let q: usize = it.next().unwrap().parse().unwrap();
    let mut out = String::new();
    for _ in 0..q {
        let pref = it.next().unwrap().to_string();
        let suff = it.next().unwrap().to_string();
        out.push_str(&format!("{}\n", search.f(pref, suff)));
    }
    print!("{}", out);
}
