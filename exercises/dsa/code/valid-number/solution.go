package main

func isNumber(s string) bool {
	// Kinds of character: 0 digit, 1 sign, 2 dot, 3 e or E, 4 anything else.
	kind := func(c byte) int {
		switch {
		case c >= '0' && c <= '9':
			return 0
		case c == '+' || c == '-':
			return 1
		case c == '.':
			return 2
		case c == 'e' || c == 'E':
			return 3
		}
		return 4
	}
	// States: 0 start, 1 sign, 2 digits, 3 dot with no digits before it,
	// 4 dot after digits, 5 digits after the dot, 6 e, 7 sign after e, 8 digits after e.
	// moves[state][kind] is the next state, or -1 when the text can't be a number.
	moves := [9][5]int{
		{2, 1, 3, -1, -1},
		{2, -1, 3, -1, -1},
		{2, -1, 4, 6, -1},
		{5, -1, -1, -1, -1},
		{5, -1, -1, 6, -1},
		{5, -1, -1, 6, -1},
		{8, 7, -1, -1, -1},
		{8, -1, -1, -1, -1},
		{8, -1, -1, -1, -1},
	}
	state := 0
	for i := 0; i < len(s); i++ {
		state = moves[state][kind(s[i])]
		if state == -1 {
			return false
		}
	}
	// Only some states are the end of a whole number.
	return state == 2 || state == 4 || state == 5 || state == 8
}
