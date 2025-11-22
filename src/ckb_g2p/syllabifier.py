# src/ckb_g2p/syllabifier.py

from .constants import IPA_VOWELS


class Syllabifier:
    """
    Responsible for splitting a list of IPA phonemes into syllables.
    """

    def is_valid_onset(self, cons_list: list) -> bool:
        if len(cons_list) == 0: return False
        if len(cons_list) == 1: return True
        if len(cons_list) == 2:
            c1, c2 = cons_list
            if c2 in ['w', 'j']: return True
        return False

    def syllabify_phonemes(self, ipa_list: list, apply_stress: bool = False, stress_position: str = 'final') -> str:
        vowel_indices = [i for i, p in enumerate(ipa_list) if p in IPA_VOWELS]

        if not vowel_indices:
            return " ".join(ipa_list)

        syllables = []
        start_index = 0

        for i in range(len(vowel_indices) - 1):
            current_v_idx = vowel_indices[i]
            next_v_idx = vowel_indices[i + 1]
            between_cons = ipa_list[current_v_idx + 1: next_v_idx]

            if self.is_valid_onset(between_cons):
                split_point = current_v_idx + 1
            else:
                split_point = next_v_idx - 1

            syllables.append("".join(ipa_list[start_index: split_point]))
            start_index = split_point

        syllables.append("".join(ipa_list[start_index:]))

        if apply_stress and syllables:
            if stress_position == 'initial':
                syllables[0] = "ˈ" + syllables[0]
            else:
                syllables[-1] = "ˈ" + syllables[-1]

        return ".".join(syllables)
