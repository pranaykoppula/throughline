from typing import List


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # A trie of the words: each node is a dict of next letters, and "$" marks a whole word.
        root = {}
        for w in words:
            node = root
            for ch in w:
                node = node.setdefault(ch, {})
            node["$"] = w
        rows, cols = len(board), len(board[0])
        found = []

        def walk(r: int, c: int, parent: dict) -> None:
            ch = board[r][c]
            node = parent.get(ch)
            if node is None:
                return              # no word continues this way: stop here
            if "$" in node:
                found.append(node.pop("$"))   # report each word once
            board[r][c] = "#"       # don't reuse this square in the same word
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                    walk(nr, nc, node)
            board[r][c] = ch
            if not node:
                parent.pop(ch)      # every word down here is found: prune the branch

        for r in range(rows):
            for c in range(cols):
                walk(r, c, root)
        return found
