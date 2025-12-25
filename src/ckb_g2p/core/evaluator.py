from ckb_g2p.utils.config import get_phoneme_features


class Evaluator:
    """
    Evaluates phoneme candidates using Sonority Sequencing Principle (SSP).
    Implements the 'Optimality Theory' approach: Score all, pick the one with lowest penalty.
    """

    def __init__(self):
        self.features = get_phoneme_features()

    def get_sonority(self, phoneme: str) -> int:
        """Returns sonority score (1-7). Defaults to 0 if unknown."""
        return self.features.get(phoneme, {}).get('sonority', 0)

    def calculate_penalty(self, candidate: tuple) -> int:
        """
        Calculates a 'badness' score for a candidate sequence.
        Lower is better.
        """
        penalty = 0
        n = len(candidate)
        sonorities = [self.get_sonority(p) for p in candidate]

        # 1. CRITICAL: Must have at least one Vowel (Sonority 7)
        # Prevents 'kwrd' (all consonants/glides)
        vowel_count = sum(1 for s in sonorities if s == 7)
        if vowel_count == 0:
            penalty += 1000

        # 2. Prefer Vowels over Glides (Maximizing Nuclei)
        # If we have a choice between 'u' (7) and 'w' (6), pick 'u'.
        # We give a small reward (negative penalty) for every full vowel.
        penalty -= (vowel_count * 10)

        # 3. Check for Hiatus (Vowel-Vowel Clashes)
        # Kurdish prefers CVC or CVG (Glide), not CVV (Hiatus).
        # Example: 'kɛw' (V-G) is better than 'kɛu' (V-V).
        for i in range(n - 1):
            if sonorities[i] == 7 and sonorities[i + 1] == 7:
                penalty += 50  # Strong penalty for adjacent vowels

        # 4. Sonority Sequencing Principle (SSP)
        # A syllable peak should ideally be Sonority 7 (Vowel).
        # If a Peak is only Sonority 6 (Glide), penalize it slightly.
        # This fixes 'g-w-r' (Peak w) vs 'g-u-r' (Peak u).
        for i in range(1, n - 1):
            prev_s = sonorities[i - 1]
            curr_s = sonorities[i]
            next_s = sonorities[i + 1]

            # If current is a local peak (higher than neighbors)
            if curr_s >= prev_s and curr_s >= next_s:
                # If the peak is a Glide (6) instead of a Vowel (7), penalize
                if curr_s == 6:
                    penalty += 20

        # 5. Word Final Checks
        if n > 1:
            last_s = sonorities[-1]
            prev_s = sonorities[-2]

            if last_s == 6:  # Ends in Glide (e.g. 'j' or 'w')
                if prev_s == 7:
                    # Ending in Vowel+Glide (e.g. 'ew') is GOOD (Diphthong)
                    penalty -= 5
                else:
                    # Ending in Consonant+Glide (e.g. 'kw') is BAD (should likely be 'ku')
                    penalty += 20

            elif last_s == 7:  # Ends in Vowel (e.g. 'iː')
                # Generally acceptable
                penalty -= 5

        return penalty

    def select_best(self, candidates: list) -> tuple:
        """Returns the candidate with the lowest penalty score."""
        if not candidates:
            return tuple()

        scored_candidates = []
        for cand in candidates:
            score = self.calculate_penalty(cand)
            scored_candidates.append((score, cand))

        # Sort by score (ascending)
        scored_candidates.sort(key=lambda x: x[0])

        return scored_candidates[0][1]