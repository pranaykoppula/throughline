impl Solution {
    pub fn is_number(s: String) -> bool {
        // Kinds of character: 0 digit, 1 sign, 2 dot, 3 e or E, 4 anything else.
        let kind = |c: u8| match c {
            b'0'..=b'9' => 0,
            b'+' | b'-' => 1,
            b'.' => 2,
            b'e' | b'E' => 3,
            _ => 4,
        };
        // States: 0 start, 1 sign, 2 digits, 3 dot with no digits before it,
        // 4 dot after digits, 5 digits after the dot, 6 e, 7 sign after e, 8 digits after e.
        // MOVES[state][kind] is the next state, or -1 when the text can't be a number.
        const MOVES: [[i32; 5]; 9] = [
            [2, 1, 3, -1, -1],
            [2, -1, 3, -1, -1],
            [2, -1, 4, 6, -1],
            [5, -1, -1, -1, -1],
            [5, -1, -1, 6, -1],
            [5, -1, -1, 6, -1],
            [8, 7, -1, -1, -1],
            [8, -1, -1, -1, -1],
            [8, -1, -1, -1, -1],
        ];
        let mut state = 0i32;
        for &c in s.as_bytes() {
            state = MOVES[state as usize][kind(c)];
            if state == -1 {
                return false;
            }
        }
        // Only some states are the end of a whole number.
        matches!(state, 2 | 4 | 5 | 8)
    }
}
