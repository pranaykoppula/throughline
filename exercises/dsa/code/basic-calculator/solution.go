package main

func calculate(s string) int {
	total := 0  // the running total inside the current brackets
	sign := 1   // the sign in front of the number being read
	number := 0 // the number being read, digit by digit
	saved := [][2]int{} // {total, sign} outside each open bracket
	for i := 0; i < len(s); i++ {
		ch := s[i]
		switch {
		case ch >= '0' && ch <= '9':
			number = number*10 + int(ch-'0')
		case ch == '+' || ch == '-':
			total += sign * number
			number = 0
			sign = 1
			if ch == '-' {
				sign = -1
			}
		case ch == '(':
			// Put the outside aside, and start a fresh total inside.
			saved = append(saved, [2]int{total, sign})
			total, sign = 0, 1
		case ch == ')':
			total += sign * number
			number = 0
			// Fold the bracket's total back into the outside.
			outside := saved[len(saved)-1]
			saved = saved[:len(saved)-1]
			total = outside[0] + outside[1]*total
		}
	}
	return total + sign*number
}
