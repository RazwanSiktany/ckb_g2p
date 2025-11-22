# src/ckb_g2p/syllabifier.py

from .constants import IPA_VOWELS


class Syllabifier:
    """
    Responsible for splitting a list of IPA phonemes into syllables
    based on Central Kurdish phonotactics (Maximum Onset Principle).
    """

    def is_valid_onset(self, cons_list: list) -> bool:
        """
        Checks if a cluster of consonants is a valid onset in Kurdish.
        Valid onsets:
        1. Single Consonant (C)
        2. Consonant + Glide (Cw, Cj)
        """
        if len(cons_list) == 0:
            return False # Hiatus (handled separately)
        if len(cons_list) == 1:
            return True
        if len(cons_list) == 2:
            c1, c2 = cons_list
            # Allow Complex Onset ONLY if 2nd char is a Glide (w, j)
            if c2 in ['w', 'j']:
                return True

        # Any cluster > 2 or CC where C2 is not glide is invalid
        return False

    def syllabify_phonemes(self, ipa_list: list, apply_stress: bool = False, stress_position: str = 'final') -> str:
        """
        Input:  ['n', 'a', 'm', 'a', 'm']
        Output: "na.ˈmam" (if stress=True, position='final')
        Output: "ˈna.mam" (if stress=True, position='initial')
        """
        vowel_indices = [i for i, p in enumerate(ipa_list) if p in IPA_VOWELS]

        if not vowel_indices:
            return " ".join(ipa_list)

        syllables = []
        start_index = 0

        for i in range(len(vowel_indices) - 1):
            current_v_idx = vowel_indices[i]
            next_v_idx = vowel_indices[i + 1]

            between_cons = ipa_list[current_v_idx + 1: next_v_idx]

            # --- IMPROVED SYLLABIFICATION LOGIC ---
            if self.is_valid_onset(between_cons):
                # Valid Onset (e.g. 'k', 'w') -> a.kwa
                split_point = current_v_idx + 1
            else:
                # Invalid Onset (e.g. 'k', 't') -> ak.ta
                split_point = next_v_idx - 1

            syllables.append("".join(ipa_list[start_index: split_point]))
            start_index = split_point

        syllables.append("".join(ipa_list[start_index:]))

        # --- UPDATED STRESS LOGIC ---
        if apply_stress and syllables:
            if stress_position == 'initial':
                syllables[0] = "ˈ" + syllables[0]
            else:
                syllables[-1] = "ˈ" + syllables[-1]

        return ".".join(syllables)
