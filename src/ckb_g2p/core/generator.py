from itertools import product


class Generator:
    """
    Generates possible phoneme sequences for ambiguous inputs.
    Handles the w/u and y/î distinctions.
    """

    def __init__(self):
        # Define ambiguity rules
        # Key: The default symbol from GraphemeParser
        # Value: List of possible phonemes it could actually be
        self.ambiguities = {
            'w': ['w', 'u'],  # 'و' can be Glide (w) or Short Vowel (u)
            'j': ['j', 'iː']  # 'ی' can be Glide (j) or Long Vowel (iː)
        }

    def generate_candidates(self, tokens: list) -> list:
        """
        Takes a list of tokens and returns a list of all possible pronunciations.

        Example: ['k', 'w', 'r', 'd']
        Returns: [
            ['k', 'w', 'r', 'd'],  # kwrd (Invalid)
            ['k', 'u', 'r', 'd']   # kurd (Valid)
        ]
        """
        # 1. Identify positions that can vary
        possibilities = []
        for token in tokens:
            if token in self.ambiguities:
                possibilities.append(self.ambiguities[token])
            else:
                possibilities.append([token])

        # 2. Cartesian product to generate all combinations
        # This is fast for Kurdish words (rarely > 2-3 ambiguous vowels per word)
        return list(product(*possibilities))