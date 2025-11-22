# src/ckb_g2p/constants.py

# 1. Define Written Vowels (Central Kurdish Script)
VOWELS_WRITTEN = {'ا', 'ە', 'و', 'ۆ', 'وو', 'ی', 'ێ'}

# 2. IPA Mapping
IPA_MAP = {
    # Vowels
    "ا": "ä", "ە": "a", "ۆ": "o̞", "ێ": "ɛ", "وو": "uː",
    "v_i": "iː", "v_u": "u",

    # Consonants
    "ئ": "ʔ", "ب": "b", "پ": "p", "ت": "t", "د": "d", 
    "ح": "ħ", "خ": "x", "ر": "ɾ", "ڕ": "r", "ز": "z", "ژ": "ʒ", 
    "س": "s", "ش": "ʃ", "ع": "ʕ", "غ": "ɣ", "ف": "f", "ڤ": "v", 
    "ق": "q", "ڵ": "ɫ", "ل": "l", "م": "m", "ن": "n", "ه": "h", "ھ": "h",
    "و": "w", "ی": "j", "ي": "j",
    "ۊ": "ẅ", "ث": "θ", "ذ": "ð", "ص": "sˤ", "ض": "dˤ",
    "ط": "tˤ", "ظ": "ðˤ", "ء": "ʔ", "ى": "aː",
    "ئا": "ʔä", "لا": "laː", "ؤ": "ʊʔ",
    "ك": "k", "ک": "k", "گ": "g",

    # --- PRECISE MAPPINGS FOR STANDARD CH/J ---
    "چ": "t̪͡ʃ̟",  
    "ج": "d̪͡ʒ̟",
}

SORTED_GRAPHEMES = sorted(IPA_MAP.keys(), key=len, reverse=True)

IPA_VOWELS = {
    "ä", "a", "o̞", "ɛ", "uː", "iː", "u", "ɪ", "aː", "ʔä", "ʊʔ"
}

SONORITY_SCALE = {
    # Obstruents (1)
    "p": 1, "b": 1, "t": 1, "d": 1, "k": 1, "g": 1, "q": 1, "ʔ": 1,
    "tˤ": 1, "dˤ": 1,

    # "Heavy" Postalveolar (English-like)
    "t͡ʃ": 1, "d͡ʒ": 1,

    # "Light" Dental
    "t̪͡ʃ̟": 1, "d̪͡ʒ̟": 1,

    # Fricatives (2)
    "f": 2, "v": 2, "s": 2, "z": 2, "ʃ": 2, "ʒ": 2, "x": 2, "ɣ": 2,
    "h": 2, "ħ": 2, "ʕ": 2, "θ": 2, "ð": 2, "sˤ": 2, "ðˤ": 2,

    # Nasals (3)
    "m": 3, "n": 3,

    # Liquids (4)
    "l": 4, "ɫ": 4, "r": 4, "ɾ": 4,

    # Glides (5)
    "w": 5, "j": 5,

    # Vowels (6)
    "ä": 6, "a": 6, "o̞": 6, "ɛ": 6, "uː": 6, "iː": 6, "u": 6, "ɪ": 6, "aː": 6
}
