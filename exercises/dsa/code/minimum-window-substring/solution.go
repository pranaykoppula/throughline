package main

func minWindow(s string, t string) string {
	// How many of each event the window still needs; negative means spare.
	var need [128]int
	for i := 0; i < len(t); i++ {
		need[t[i]]++
	}
	missing := len(t) // total events still needed, repeats included
	bestStart, bestLen, left := 0, len(s)+1, 0
	for right := 0; right < len(s); right++ {
		// Taking in one more event.
		if need[s[right]] > 0 {
			missing--
		}
		need[s[right]]--
		// While the window has everything, shrink it from the left.
		for missing == 0 {
			if right-left+1 < bestLen {
				bestStart, bestLen = left, right-left+1
			}
			need[s[left]]++
			if need[s[left]] > 0 {
				missing++
			}
			left++
		}
	}
	if bestLen > len(s) {
		return ""
	}
	return s[bestStart : bestStart+bestLen]
}
