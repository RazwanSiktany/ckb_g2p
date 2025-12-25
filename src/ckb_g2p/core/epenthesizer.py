from ckb_g2p.utils.config import get_phoneme_features


class Epenthesizer:
    """
    Inserts the short vowel /ɪ/ (Bizroka) to break illegal consonant clusters.
    Follows Central Kurdish phonotactics:
    1. No Initial CC clusters (e.g., 'bra' -> 'bɪra').
    2. Final CC is allowed ONLY if sonority falls (e.g., 'kurd' [r->d] is OK).
    3. Final CC with rising sonority is split (e.g., 'agr' -> 'agɪr').
    """

    def __init__(self):
        self.features = get_phoneme_features()

    def get_sonority(self, p: str) -> int:
        return self.features.get(p, {}).get('sonority', 0)

    def is_vowel(self, p: str) -> bool:
        return self.get_sonority(p) == 7

    def apply(self, phonemes: tuple) -> tuple:
        if not phonemes:
            return tuple()

        plist = list(phonemes)

        # Pass 1: Handle Initial Clusters (Start of word)
        # Sorani Kurdish strictly forbids CC at start.
        if len(plist) >= 2:
            c1, c2 = plist[0], plist[1]
            if not self.is_vowel(c1) and not self.is_vowel(c2):
                # Exception: 'Cw' or 'Cj' might be valid onsets
                # But strict rule prefers bɪra
                if self.get_sonority(c2) < 6:  # If C2 is not a glide
                    plist.insert(1, 'ɪ')

        # Pass 2: Handle Medial/Triple Clusters
        # Logic: Iterate through the list. If we find CCC, decide where to break.
        i = 0
        while i < len(plist) - 2:
            # Look at a window of 3 characters
            c1 = plist[i]
            c2 = plist[i + 1]
            c3 = plist[i + 2]

            # Check if all are consonants (Sonority < 7)
            if not self.is_vowel(c1) and not self.is_vowel(c2) and not self.is_vowel(c3):
                s1 = self.get_sonority(c1)
                s2 = self.get_sonority(c2)

                # Analyze C1-C2 (The first pair)
                # If C1-C2 is a Valid Coda (Falling Sonority), we prefer NOT to break it.
                # Example: 'rds' (r-d-s). r(5)>d(1). Keep 'rd' together.
                # Example: 'dst' (d-s-t). d(1)<s(3). Bad coda. Break 'd-s'.

                if s1 > s2:
                    # Valid Coda C1-C2.
                    # We accept C1C2 as the coda of the previous syllable.
                    # We assume the break happens AFTER C2.
                    # So we don't insert between C1 and C2.
                    # We just continue to the next position to check C2-C3.
                    pass
                else:
                    # Invalid Coda C1-C2 (Rising or Flat/Low).
                    # We MUST break C1-C2.
                    # d-s-t -> d-ɪ-s-t
                    plist.insert(i + 1, 'ɪ')
                    i += 1  # Skip the inserted char

            i += 1

        # Pass 3: Handle Final Clusters (End of word)
        # Allow CC only if Sonority(C1) >= Sonority(C2)
        if len(plist) >= 2:
            last = plist[-1]
            prev = plist[-2]

            # If we end in CC (and prev is not vowel, to distinguish VCC from VVC? No, simple check)
            if not self.is_vowel(last) and not self.is_vowel(prev):
                s_last = self.get_sonority(last)
                s_prev = self.get_sonority(prev)

                # Check for Sonority Violation
                # Rising: g-r (1-5) -> agɪr
                if s_last > s_prev:
                    plist.insert(len(plist) - 1, 'ɪ')
                # Flat and low (Stop-Stop): k-t -> kɪt
                elif s_last == s_prev and s_last < 5:
                    plist.insert(len(plist) - 1, 'ɪ')

        return tuple(plist)