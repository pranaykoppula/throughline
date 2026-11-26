class Solution {
public:
    string minWindow(string s, string t) {
        // How many of each event the window still needs; negative means spare.
        array<int, 128> need{};
        for (char c : t) need[c]++;
        int missing = t.size();  // total events still needed, repeats included
        int bestStart = 0, bestLen = INT_MAX, left = 0;
        for (int right = 0; right < (int)s.size(); right++) {
            // Taking in one more event.
            if (need[s[right]]-- > 0) missing--;
            // While the window has everything, shrink it from the left.
            while (missing == 0) {
                if (right - left + 1 < bestLen) {
                    bestStart = left;
                    bestLen = right - left + 1;
                }
                if (++need[s[left]] > 0) missing++;
                left++;
            }
        }
        return bestLen == INT_MAX ? "" : s.substr(bestStart, bestLen);
    }
};
