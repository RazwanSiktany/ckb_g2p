# src/ckb_g2p/phonetics.py

from .constants import VOWELS_WRITTEN, IPA_VOWELS, SONORITY_SCALE


class Phonetics:
    @staticmethod
    def is_written_vowel(char: str) -> bool:
        return char in VOWELS_WRITTEN

    @staticmethod
    def is_ipa_vowel(phoneme: str) -> bool:
        return phoneme in IPA_VOWELS

    @staticmethod
    def get_sonority(phoneme: str) -> int:
        return SONORITY_SCALE.get(phoneme, 0)

    def normalize_initial_vowel(self, text: str) -> str:
        if not text: return text
        first_char = text[0]
        if first_char in VOWELS_WRITTEN and first_char not in ['و', 'ی', 'وو']:
             return "ئ" + text
        if first_char in ['ۆ', 'ێ', 'ە', 'ا']:
            return "ئ" + text
        return text

    def disambiguate_semi_vowels(self, text: str) -> str:
        if not text: return text
        chars = list(text)
        length = len(chars)
        types = [''] * length

        skip_next = False
        for i in range(length):
            if skip_next:
                skip_next = False
                continue
            char = chars[i]

            if char == 'و' and i + 1 < length and chars[i+1] == 'و':
                if i == 0: # Start of word
                    types[i] = 'C'; chars[i+1] = 'v_u'; types[i+1] = 'V'
                else: # Medial
                    chars[i] = 'وو'; types[i] = 'V'; types[i+1] = 'X'
                skip_next = True
                continue

            if char in ['و', 'ی']: types[i] = '?'
            elif char in VOWELS_WRITTEN: types[i] = 'V'
            else: types[i] = 'C'

        if types[0] == '?': types[0] = 'C'

        changed = True
        while changed:
            changed = False
            for i in range(length):
                if types[i] == '?':
                    prev_is_v = False
                    k = i - 1
                    while k >= 0:
                        if types[k] == 'X': k -= 1; continue
                        if types[k] == 'V': prev_is_v = True
                        break
                    next_is_v = False
                    k = i + 1
                    while k < length:
                        if types[k] == 'X': k += 1; continue
                        if types[k] == 'V': next_is_v = True
                        break
                    if prev_is_v or next_is_v:
                        types[i] = 'C'
                        changed = True

        for i in range(length):
            if types[i] == '?':
                prev_type = 'C'
                k = i - 1
                while k >= 0:
                    if types[k] != 'X':
                        prev_type = types[k]
                        break
                    k -= 1
                if prev_type == 'C':
                    types[i] = 'V'
                    if chars[i] == 'و': chars[i] = 'v_u'
                    if chars[i] == 'ی': chars[i] = 'v_i'
                else:
                    types[i] = 'C'

        result = []
        for i in range(length):
            if types[i] != 'X': result.append(chars[i])
        return "".join(result)

    def insert_bizroka(self, ipa_list: list) -> list:
        if not ipa_list: return []

        if len(ipa_list) == 1:
            if not self.is_ipa_vowel(ipa_list[0]):
                ipa_list.append("ɪ")
                return ipa_list

        if len(ipa_list) >= 2:
            c1, c2 = ipa_list[0], ipa_list[1]
            if not self.is_ipa_vowel(c1) and not self.is_ipa_vowel(c2):
                if c2 not in ['w', 'j']:
                    ipa_list.insert(1, "ɪ")

        i = 0
        while i < len(ipa_list) - 1:
            c1 = ipa_list[i]
            c2 = ipa_list[i+1]
            if c1 == c2 and not self.is_ipa_vowel(c1):
                has_following_vowel = False
                if i + 2 < len(ipa_list):
                    if self.is_ipa_vowel(ipa_list[i+2]):
                        has_following_vowel = True
                if not has_following_vowel:
                    ipa_list.insert(i + 1, "ɪ")
                    i += 1 
            i += 1

        i = 0
        while i < len(ipa_list) - 3:
            chunk = ipa_list[i: i + 4]
            if all(not self.is_ipa_vowel(c) for c in chunk):
                ipa_list.insert(i + 2, "ɪ")
                i += 2
            i += 1

        if len(ipa_list) >= 2:
            c_last = ipa_list[-1]
            c_prev = ipa_list[-2]
            if not self.is_ipa_vowel(c_last) and not self.is_ipa_vowel(c_prev):
                s_last = self.get_sonority(c_last)
                s_prev = self.get_sonority(c_prev)
                if s_last > s_prev:
                    ipa_list.insert(-1, "ɪ")
                elif len(ipa_list) >= 3:
                    c_pre_prev = ipa_list[-3]
                    if not self.is_ipa_vowel(c_pre_prev):
                        ipa_list.insert(-2, "ɪ")

        return ipa_list
