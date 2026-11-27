use std::io::Read;

struct Solution;
include!("solution.rs");

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut it = s.split_whitespace();
    let rows: usize = it.next().unwrap().parse().unwrap();
    let _cols: usize = it.next().unwrap().parse().unwrap();
    let board: Vec<Vec<char>> = (0..rows).map(|_| it.next().unwrap().chars().collect()).collect();
    let k: usize = it.next().unwrap().parse().unwrap();
    let words: Vec<String> = (0..k).map(|_| it.next().unwrap().to_string()).collect();
    let mut out = Solution::find_words(board, words);
    out.sort();
    let mut text = String::new();
    for w in out {
        text.push_str(&w);
        text.push('\n');
    }
    print!("{}", text);
}
