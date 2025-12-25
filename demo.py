import sys
import os

# Add src to path (ensures it works even if not installed via pip)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ckb_g2p.converter import Converter


def header(text):
    print(f"\n{'=' * 40}")
    print(f" 🔹 {text}")
    print(f"{'=' * 40}")


def main():
    print("\n🚀 Central Kurdish G2P (Graph2Phon) Demo")
    print("   A modern, linguistically accurate G2P engine.")

    # 1. Initialize
    print("\n[Initializing Converter...]")
    converter = Converter(use_cache=True)
    print("✅ Converter Ready (SQLite Cache Active)")

    # 2. Basic Word Conversion
    header("Basic Word Conversion")
    words = [
        ("کوێ", "Basic (Vowel Selection)"),
        ("کێو", "Palatalization (k -> ch)"),
        ("ئاگر", "Epenthesis (Bizroka Insertion)")
    ]

    print(f"{'Input':<15} | {'Output (Syllables)':<20} | {'Feature'}")
    print("-" * 60)

    for w, desc in words:
        result = converter.convert(w, output_format="syllables")[0]
        print(f"{w:<15} | {result:<20} | {desc}")

    # 3. Full Sentence Parsing
    header("Full Sentence Context")
    sentence = "من کوردم و خەڵکی کوردستانم"
    result_sentence = converter.convert(sentence, output_format="syllables")
    print(f"Input:  {sentence}")
    print(f"Output: {' '.join(result_sentence)}")

    # 4. Text Normalization (Numbers)
    header("Text Normalization (ckb-textify)")
    text_num = "ساڵی 1991 لە دایک بووم"
    result_num = converter.convert(text_num, output_format="syllables", normalize=True)

    print(f"Input:  {text_num}")
    # Note: If ckb-textify is missing, it will print digits. If present, it prints phonemes.
    print(f"Output: {' '.join(result_num)}")

    # 5. Advanced Linguistic Features (Unique to this Project)
    header("Advanced Linguistic Features")

    # A. Emphatics Preservation (Your unique requirement)
    emphatic_word = "صەد"
    res_emph = converter.convert(emphatic_word, output_format="syllables")[0]
    print(f"1. Emphatics Preservation:")
    print(f"   Input: '{emphatic_word}' (Sad)")
    print(f"   Output: {res_emph} (Preserves /sˤ/ instead of normalizing to /s/)")

    # B. Stress Logic (Negative Verbs)
    neg_verb = "نەچوو"
    res_neg = converter.convert(neg_verb, output_format="syllables")[0]
    print(f"\n2. Negative Verb Stress:")
    print(f"   Input: '{neg_verb}'")
    print(f"   Output: {res_neg} (Initial stress detected)")

    print("\n✨ Demo Complete!")


if __name__ == "__main__":
    main()