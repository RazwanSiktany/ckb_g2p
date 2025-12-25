import re
from ckb_g2p.core.grapheme_parser import GraphemeParser
from ckb_g2p.core.generator import Generator
from ckb_g2p.core.evaluator import Evaluator
from ckb_g2p.core.palatalizer import Palatalizer
from ckb_g2p.core.epenthesizer import Epenthesizer
from ckb_g2p.core.syllabifier import Syllabifier
from ckb_g2p.core.preprocessor import Preprocessor
from ckb_g2p.core.cache import LexiconCache

try:
    from ckb_textify.core.pipeline import Pipeline
    from ckb_textify.core.types import NormalizationConfig

    HAS_TEXTIFY = True
except ImportError:
    HAS_TEXTIFY = False


class Converter:
    def __init__(self, use_cache: bool = True, use_pause_markers: bool = True):
        self.preprocessor = Preprocessor()
        self.parser = GraphemeParser()
        self.gen = Generator()
        self.evaluator = Evaluator()
        self.palatalizer = Palatalizer()
        self.epenthesizer = Epenthesizer()
        self.syllabifier = Syllabifier()

        self.use_cache = use_cache
        self.use_pause_markers = use_pause_markers

        if self.use_cache:
            self.cache = LexiconCache()

        self.normalizer = None
        if HAS_TEXTIFY:
            try:
                # 🚀 Best Config for ckb_g2p / TTS
                g2p_config = NormalizationConfig(
                    # --- 1. Enable All Converters ---
                    # G2P cannot pronounce "123" or "$", it needs "sed u bîst..."
                    enable_numbers=True,
                    enable_web=True,
                    enable_phone=True,
                    enable_date_time=True,
                    enable_units=True,
                    enable_currency=True,
                    enable_math=True,
                    enable_technical=True,
                    enable_symbols=True,
                    enable_linguistics=True,

                    # --- 2. Transliteration (Crucial) ---
                    # Converts English/Foreign words to Kurdish sounds (e.g. "Hello" -> "Hêlo")
                    # This prevents the G2P from crashing on Latin characters.
                    enable_transliteration=True,

                    # --- 3. Arabic/Tajweed Handling ---
                    # Converts Arabic Diacritics to explicit Kurdish letters (e.g. Fatha -> 'e')
                    enable_diacritics=True,
                    diacritics_mode="convert",
                    shadda_mode="double",  # "muhemmed" is better phonetically than "muhemed"

                    # --- 4. Input Safety ---
                    # Disable this to not interfer with arabic text before they reach G2P
                    decode_ali_k=False,

                    # --- 5. Cleanliness ---
                    # Emojis usually sound bad in TTS ("Face with tears of joy").
                    # Remove them unless you specifically want them read.
                    emoji_mode="remove",

                    # --- 6. Rhythm & Pauses ---
                    # Phone numbers use a pause marker.
                    # Map it to a Kurdish Comma (،) so the G2P generates a silence/pause phoneme.
                    enable_pause_markers=True,
                    pause_token="،"
                )
                self.normalizer = Pipeline(g2p_config)
            except Exception as e:
                print(f"⚠️ Warning: Could not initialize ckb-textify: {e}")

    def _process_word(self, word: str) -> tuple:
        word = self.preprocessor.normalize_initial_vowel(word)

        if self.use_cache:
            cached = self.cache.get(word)
            if cached: return cached

        tokens = self.parser.tokenize(word)
        candidates = self.gen.generate_candidates(tokens)
        best = self.evaluator.select_best(candidates)
        palatalized = self.palatalizer.apply(best)
        final = self.epenthesizer.apply(palatalized)

        if self.use_cache:
            self.cache.set(word, final)
        return final

    def convert(self, text: str, output_format: str = "ipa", normalize: bool = True) -> list:
        if normalize and self.normalizer:
            text = self.normalizer.normalize(text)

        # Clitic Attachment Rule
        text = re.sub(r'(\S)\s+(و)(?=\s|$)', r'\1\2', text)

        # Tokenize: Split by punctuation and whitespace, preserving them
        # Captures: words, spaces, and punctuation groups like '...' or '?!'
        raw_tokens = re.split(r'([.,!?;:،؛؟]+|\s+)', text)
        # Remove empty strings and purely whitespace tokens (we add spaces manually if needed)
        tokens = [t for t in raw_tokens if t.strip() or re.match(r'[.,!?;:،؛؟]+', t)]

        output = []

        for token in tokens:
            token = token.strip()
            if not token: continue

            # Check for Punctuation (Pause Markers)
            if re.match(r'^[.,!?;:،؛؟]+$', token):
                if self.use_pause_markers:
                    # Short pauses
                    if any(c in token for c in [',', ';', ':', '،', '؛']):
                        output.append("|")
                    # Long pauses
                    else:
                        output.append("||")
                # Add space after punctuation if outputting flat IPA
                if output_format == "ipa": output.append(" ")
                continue

            # Check for numbers (skip if not normalized)
            if re.match(r'^\d+$', token):
                output.append(token)
                if output_format == "ipa": output.append(" ")
                continue

            # Process Word
            phonemes = self._process_word(token)

            if output_format == "syllables":
                syl = self.syllabifier.syllabify(phonemes)
                output.append(syl)
            else:
                output.extend(phonemes)
                output.append(" ")

        # Clean up trailing space for IPA format
        if output_format == "ipa" and output and output[-1] == " ":
            output.pop()

        return output