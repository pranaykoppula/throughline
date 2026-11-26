from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)          # how many of each event the window still needs
        missing = len(t)           # total events still needed, repeats included
        best_start, best_len = 0, len(s) + 1
        left = 0
        for right, ch in enumerate(s):
            # Taking in one more event.
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1
            # While the window has everything, shrink it from the left.
            while missing == 0:
                if right - left + 1 < best_len:
                    best_start, best_len = left, right - left + 1
                gone = s[left]
                need[gone] += 1
                if need[gone] > 0:
                    missing += 1
                left += 1
        return s[best_start:best_start + best_len] if best_len <= len(s) else ""
