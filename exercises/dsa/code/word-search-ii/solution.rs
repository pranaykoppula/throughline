#[derive(Default)]
struct TrieNode {
    next: [Option<Box<TrieNode>>; 26],
    word: Option<String>, // set when a whole word ends here
}

impl Solution {
    pub fn find_words(board: Vec<Vec<char>>, words: Vec<String>) -> Vec<String> {
        // A trie of the words.
        let mut root = TrieNode::default();
        for w in words {
            let mut node = &mut root;
            for b in w.bytes() {
                node = node.next[(b - b'a') as usize].get_or_insert_with(Default::default);
            }
            node.word = Some(w);
        }
        let mut board: Vec<Vec<u8>> = board.into_iter().map(|row| row.into_iter().map(|c| c as u8).collect()).collect();
        let mut found = Vec::new();
        for r in 0..board.len() {
            for c in 0..board[0].len() {
                Self::walk(&mut board, r, c, &mut root, &mut found);
            }
        }
        found
    }

    fn walk(board: &mut Vec<Vec<u8>>, r: usize, c: usize, parent: &mut TrieNode, found: &mut Vec<String>) {
        let ch = board[r][c];
        let slot = (ch - b'a') as usize;
        let node = match parent.next[slot].as_mut() {
            Some(node) => node,
            None => return, // no word continues this way: stop here
        };
        if let Some(w) = node.word.take() {
            found.push(w); // report each word once
        }
        board[r][c] = b'#'; // don't reuse this square in the same word
        let (rows, cols) = (board.len() as i32, board[0].len() as i32);
        for (dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let (nr, nc) = (r as i32 + dr, c as i32 + dc);
            if nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr as usize][nc as usize] != b'#' {
                Self::walk(board, nr as usize, nc as usize, node, found);
            }
        }
        board[r][c] = ch;
        if node.word.is_none() && node.next.iter().all(|n| n.is_none()) {
            parent.next[slot] = None; // every word down here is found: prune the branch
        }
    }
}
