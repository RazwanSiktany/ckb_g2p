from ckb_g2p.utils.config import get_mappings


class TrieNode:
    """A single node in the Trie structure."""
    __slots__ = ['children', 'value']  # Optimization to save memory

    def __init__(self):
        self.children = {}
        self.value = None  # Stores the IPA symbol if this is the end of a valid grapheme


class GraphemeParser:
    """
    A high-performance parser that tokenizes Kurdish text into IPA phonemes
    using a Trie for O(L) complexity (where L is the length of the longest grapheme).
    """

    def __init__(self):
        self.root = TrieNode()
        self._build_trie(get_mappings())

    def _build_trie(self, mappings: dict):
        """Populates the Trie from the mappings dictionary."""
        for grapheme, ipa in mappings.items():
            node = self.root
            for char in grapheme:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.value = ipa

    def tokenize(self, text: str) -> list:
        """
        Converts text into a list of IPA symbols.
        Uses greedy matching: finds the longest possible grapheme at the current position.

        Example: "کوو" -> ['k', 'uː'] (matches 'وو' together, not 'و', 'و')
        """
        tokens = []
        i = 0
        n = len(text)

        while i < n:
            node = self.root
            match_len = 0
            match_val = None

            # Look ahead to find the longest matching grapheme
            j = i
            while j < n and text[j] in node.children:
                node = node.children[text[j]]
                j += 1
                if node.value:
                    match_len = j - i
                    match_val = node.value

            if match_len > 0:
                # Found a known grapheme (e.g., 'وو' -> 'uː')
                tokens.append(match_val)
                i += match_len
            else:
                # No match found (unknown char or space), keep original
                tokens.append(text[i])
                i += 1

        return tokens