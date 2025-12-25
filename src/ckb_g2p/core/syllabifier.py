from ckb_g2p.utils.config import get_phoneme_features


class Syllabifier:
    def __init__(self):
        self.features = get_phoneme_features()

    def get_sonority(self, p: str) -> int:
        return self.features.get(p, {}).get('sonority', 0)

    def is_vowel(self, p: str) -> bool:
        return self.get_sonority(p) == 7

    def is_negative_verb(self, phonemes: list) -> bool:
        """
        Checks for negative prefixes: 'na' (نە/نا) or 'ma' (مە).
        """
        if len(phonemes) < 2:
            return False

        p0, p1 = phonemes[0], phonemes[1]

        # Check 'n' + Vowel (na, nä)
        if p0 == 'n' and self.is_vowel(p1):
            return True

        # Check 'm' + Vowel (ma)
        if p0 == 'm' and self.is_vowel(p1):
            return True

        return False

    def is_valid_onset(self, chunk: list) -> bool:
        """
        Old Project Rule:
        - Single Consonant: OK
        - Two Consonants: OK ONLY if second is Glide (w/j).
        Example: 'xwa' (xw) OK. 'bra' (br) NO (needs epenthesis usually).
        """
        if len(chunk) == 0: return False
        if len(chunk) == 1: return True
        if len(chunk) == 2:
            c1, c2 = chunk
            # Check if C2 is a glide (w or j)
            # We check specific phonemes because sonority 6 includes w/j
            if c2 in ['w', 'j']:
                return True
        return False

    def syllabify(self, phonemes: tuple, apply_stress: bool = True) -> str:
        if not phonemes:
            return ""

        plist = list(phonemes)
        nuclei = [i for i, p in enumerate(plist) if self.is_vowel(p)]

        if not nuclei:
            return "".join(plist)

        syllables = []
        start = 0

        for i in range(len(nuclei) - 1):
            curr_n = nuclei[i]
            next_n = nuclei[i + 1]

            # Consonants between vowels
            intervocalic = plist[curr_n + 1: next_n]
            n_cons = len(intervocalic)

            # Use Old Project Logic for splitting
            split_point = curr_n + 1  # Default split after first vowel (V.CV)

            if n_cons > 1:
                # Try to maximize onset, but respect Kurdish rules
                # If we have VCCV (e.g., bas.ti or xwa.ti?)
                # We check the chunk immediately before the next vowel

                # Check if the last 2 consonants form a valid onset (Cw/Cj)
                potential_onset = intervocalic[-2:]
                if self.is_valid_onset(potential_onset):
                    # Split before the cluster (V.CCV) -> e.g., 'da.xwa'
                    split_point = next_n - 2
                else:
                    # Default split: VC.CV (Split middle or 1 char before next vowel)
                    split_point = next_n - 1

            syl_chunk = plist[start:split_point]
            syllables.append("".join(syl_chunk))
            start = split_point

        syllables.append("".join(plist[start:]))

        if apply_stress and syllables:
            if self.is_negative_verb(plist):
                syllables[0] = "ˈ" + syllables[0]
            else:
                syllables[-1] = "ˈ" + syllables[-1]

        return ".".join(syllables)