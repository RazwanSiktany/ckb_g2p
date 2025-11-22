# demo.py
import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from ckb_g2p import Converter

def main():
    print("=== Central Kurdish G2P Demo ===\n")
    converter = Converter(use_stress=True, use_pause_markers=True, normalize=True)

    cases = [
        "دەچێنن",
        "کێو",
        "چێو",
        "گیران",
        "جیران",
        "ووشە",
        "بەرز",
        "محمد",
        "نەچوو",
        "سڵاو، ناوم ئازادە",
        "کویز",
        "کوین",
    ]

    print(f"{'Input':<20} | {'Output'}")
    print("-" * 50)
    for text in cases:
        print(f"{text:<20} | {converter.syllabify(text)}")

if __name__ == "__main__":
    main()
