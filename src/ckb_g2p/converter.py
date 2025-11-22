# src/ckb_g2p/converter.py

import re
from .constants import IPA_MAP, SORTED_GRAPHEMES
from .phonetics import Phonetics
from .syllabifier import Syllabifier

# Try to import ckb_textify
try:
    from ckb_textify import convert_all
    HAS_TEXTIFY = True
except ImportError:
    HAS_TEXTIFY = False


class Converter:
    """
    The main entry point for the G2P conversion.
    """

    def __init__(self, use_stress: bool = False, use_pause_markers: bool = True, normalize: bool = True):
        """
        Args:
            use_stress (bool): If True, adds IPA stress marker (ˈ).
            use_pause_markers (bool): If True, converts punctuation to | and ||.
            normalize (bool): If True, uses ckb-textify to clean text.
        """
        self.use_stress = use_stress
        self.use_pause_markers = use_pause_markers
        self.should_normalize = normalize
        self.phonetics = Phonetics()
        self.syllabifier_engine = Syllabifier()

        if self.should_normalize and not HAS_TEXTIFY:
            print("Warning: 'normalize' is set to True, but 'ckb-textify' is not installed.")

    def text_to_ipa(self, text: str) -> list:
        # 1. Normalize & Disambiguate
        text = self.phonetics.normalize_initial_vowel(text)
        text = self.phonetics.disambiguate_semi_vowels(text)

        ipa_output = []
        i = 0
        length = len(text)

        while i < length:
            char = text[i]
            match_found = False

            # --- PALATALIZATION RULE ---
            if char in ['ک', 'گ']:
                context = text[i + 1:] if i + 1 < length else ""
                should_palatalize = False

                if context.startswith('وێ'): should_palatalize = True
                elif context.startswith('ێ'): should_palatalize = True
                elif context.startswith('ی'): should_palatalize = True
                elif context.startswith('v_i'): should_palatalize = True

                if should_palatalize:
                    if char == 'ک':
                        ipa_output.append('t͡ʃ') # Heavy (Chair)
                    else:
                        ipa_output.append('d͡ʒ') # Heavy (Jack)
                    i += 1
                    continue

            # --- Standard Greedy Mapping ---
            for grapheme in SORTED_GRAPHEMES:
                if text[i:].startswith(grapheme):
                    ipa_output.append(IPA_MAP[grapheme])
                    i += len(grapheme)
                    match_found = True
                    break

            # --- Fallback ---
            if not match_found:
                pass 
                i += 1

        # 2. Bizroka Insertion
        ipa_output = self.phonetics.insert_bizroka(ipa_output)
        return ipa_output

    def syllabify_word(self, word: str) -> str:
        """
        Helper: Converts one word to syllabified IPA.
        """
        ipa_list = self.text_to_ipa(word)

        # --- STRESS POSITION LOGIC ---
        stress_pos = 'final'
        # Negative Verbs check
        if word.startswith(('نە', 'نا')):
            stress_pos = 'initial'

        return self.syllabifier_engine.syllabify_phonemes(
            ipa_list, 
            apply_stress=self.use_stress,
            stress_position=stress_pos
        )

    def syllabify(self, text: str) -> str:
        """
        Main Interface.
        """
        # 1. External Normalization (Full Sentence)
        if self.should_normalize and HAS_TEXTIFY:
            # ckb-textify's convert_all handles full text (numbers -> text)
            text = convert_all(text)

        # 2. Split into tokens
        raw_parts = re.split(r'([.,!?;:]+|\s+)', text)
        tokens = [t.strip() for t in raw_parts if t.strip()]

        merged_tokens = []
        i = 0
        while i < len(tokens):
            current_token = tokens[i]
            if current_token == "و":
                if merged_tokens and not re.match(r'^[.,!?;:]+$', merged_tokens[-1]):
                    merged_tokens[-1] += "و"
                else:
                    merged_tokens.append(current_token)
            else:
                merged_tokens.append(current_token)
            i += 1

        processed_output = []
        for token in merged_tokens:
            if re.match(r'^[.,!?;:]+$', token):
                if self.use_pause_markers:
                    if any(c in token for c in [',', ';', ':']):
                        processed_output.append("|")
                    else:
                        processed_output.append("||")
                else:
                    pass
            else:
                processed_output.append(self.syllabify_word(token))

        return " ".join(processed_output)
