from typing import List


class WordFilter:
    def __init__(self, words: List[str]):
        # One trie of keys "suffix{word", for every suffix of every word.
        # "{" comes straight after "z", so it can't be confused with a letter.
        # Each node remembers the largest index of any word whose key passes through it.
        self.root = {}
        for index, word in enumerate(words):
            for start in range(len(word) + 1):
                node = self.root
                for ch in word[start:] + "{" + word:
                    node = node.setdefault(ch, {})
                    node["index"] = index   # later words overwrite earlier ones

    def f(self, pref: str, suff: str) -> int:
        # A word with this prefix and suffix has the key "suff{pref..." in the trie.
        node = self.root
        for ch in suff + "{" + pref:
            node = node.get(ch)
            if node is None:
                return -1
        return node["index"]
