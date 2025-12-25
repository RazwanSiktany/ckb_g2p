class Preprocessor:
    """
    Handles text normalization rules from the old project,
    specifically inserting glottal stops for initial vowels.
    """

    def __init__(self):
        # Vowels that cannot start a word without a glottal stop
        self.initial_vowels = {'ا', 'ە', 'ۆ', 'ێ'}
        # 'و' and 'ی' are excluded because they can be glides (w/y) at the start

    def normalize_initial_vowel(self, text: str) -> str:
        """
        Ensures words starting with naked vowels get a glottal stop.
        Example: "ازاد" -> "ئازاد"
        Matches old project logic: phonetics.normalize_initial_vowel
        """
        if not text:
            return text

        first_char = text[0]

        # Rule: If starts with written vowel (except w/y/uu), prepend 'ئ'
        if first_char in self.initial_vowels:
            return "ئ" + text

        return text