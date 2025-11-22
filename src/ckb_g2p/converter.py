# src/ckb_g2p/converter.py

import re
import csv
import os
from functools import lru_cache
from .constants import IPA_MAP, SORTED_GRAPHEMES
from .phonetics import Phonetics
from .syllabifier import Syllabifier

try:
    from ckb_textify import convert_all
    HAS_TEXTIFY = True
except ImportError:
    HAS_TEXTIFY = False

# --- Load Exceptions Dictionary ---
EXCEPTIONS = {}
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'resources', 'exceptions.csv')

if os.path.exists(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None) # Skip header
        for row in reader:
            if len(row) >= 2:
                # Key: Word, Value: List of IPA symbols
                EXCEPTIONS[row[0].strip()] = row[1].strip().split()

class Converter:
    """
    The main entry point for the G2P conversion.
    """

    def __init__(self, use_stress: bool = False, use_pause_markers: bool = True, normalize: bool = True):
        self.use_stress = use_stress
        self.use_pause_markers = use_pause_markers
        self.should_normalize = normalize
        self.phonetics = Phonetics()
        self.syllabifier_engine = Syllabifier()

        if self.should_normalize and not HAS_TEXTIFY:
            print("Warning: 'normalize' is set to True, but 'ckb-textify' is not installed.")

    @lru_cache(maxsize=5000)
    def text_to_ipa(self, text: str) -> tuple:
        # 0. Check Exceptions Dictionary
        if text in EXCEPTIONS:
            return tuple(EXCEPTIONS[text])

        # 1. Normalize & Disambiguate
        text = self.phonetics.normalize_initial_vowel(text)
        text = self.phonetics.disambiguate_semi_vowels(text)

        ipa_output = []
        i = 0
        length = len(text)

        while i < length:
            char = text[i]
            match_found = False

            # Palatalization
            if char in ['ک', 'گ']:
                context = text[i + 1:] if i + 1 < length else ""
                should_palatalize = False
                if context.startswith(('وێ', 'ێ', 'ی', 'v_i')):
                    should_palatalize = True

                if should_palatalize:
                    if char == 'ک': ipa_output.append('t͡ʃ')
                    else: ipa_output.append('d͡ʒ')
                    i += 1
                    continue

            # Standard Mapping
            for grapheme in SORTED_GRAPHEMES:
                if text[i:].startswith(grapheme):
                    ipa_output.append(IPA_MAP[grapheme])
                    i += len(grapheme)
                    match_found = True
                    break

            if not match_found:
                pass 
                i += 1

        # 2. Bizroka
        result = self.phonetics.insert_bizroka(ipa_output)
        return tuple(result)

    def syllabify_word(self, word: str) -> str:
        # Cache returns tuple, convert to list for syllabifier if needed 
        # (though syllabifier generally iterates, so tuple is fine)
        ipa_list = list(self.text_to_ipa(word))

        stress_pos = 'final'
        if word.startswith(('نە', 'نا')):
            stress_pos = 'initial'

        return self.syllabifier_engine.syllabify_phonemes(
            ipa_list, 
            apply_stress=self.use_stress,
            stress_position=stress_pos
        )

    def syllabify(self, text: str) -> str:
        if self.should_normalize and HAS_TEXTIFY:
            text = convert_all(text)

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
