class Solution {
    public String minWindow(String s, String t) {
        // How many of each event the window still needs; negative means spare.
        int[] need = new int[128];
        for (char c : t.toCharArray()) need[c]++;
        int missing = t.length();  // total events still needed, repeats included
        int bestStart = 0, bestLen = Integer.MAX_VALUE, left = 0;
        for (int right = 0; right < s.length(); right++) {
            // Taking in one more event.
            if (need[s.charAt(right)]-- > 0) missing--;
            // While the window has everything, shrink it from the left.
            while (missing == 0) {
                if (right - left + 1 < bestLen) {
                    bestStart = left;
                    bestLen = right - left + 1;
                }
                if (++need[s.charAt(left)] > 0) missing++;
                left++;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLen);
    }
}
