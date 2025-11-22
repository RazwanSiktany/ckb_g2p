# demo.py
import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from ckb_g2p import Converter

def main():
    print("=== Central Kurdish G2P Demo ===\n")

    # 1. Basic Conversion
    print("--- 1. Basic Syllabification ---")
    converter = Converter(use_stress=False, use_pause_markers=True, normalize=True)

    basic_cases = [
        "چێوار",
        "کێوار",
        "گرفت",
        "مامم",
        "بووین",
        "ووشە",
        "سڵاو، ناوی من ئازادە.",
        "ساڵی 1991" # Testing ckb-textify integration
    ]

    print(f"{'Input':<20} | {'Output'}")
    print("-" * 50)
    for text in basic_cases:
        print(f"{text:<20} | {converter.syllabify(text)}")
    print("\n")


    # 2. TTS Mode (Stress & Negative Verbs)
    print("--- 2. TTS Mode (With Stress) ---")
    tts_converter = Converter(use_stress=True, use_pause_markers=True)

    stress_cases = [
        ("کوردستان", "Standard Noun (Final)"),
        ("نەچوو", "Negative Verb (Initial)"),
        ("ناخۆم", "Negative Verb (Initial)"),
        ("دەچم", "Positive Verb (Final)"),
    ]

    print(f"{'Input':<15} | {'Expected Type':<25} | {'Output'}")
    print("-" * 65)
    for text, desc in stress_cases:
        print(f"{text:<15} | {desc:<25} | {tts_converter.syllabify(text)}")

if __name__ == "__main__":
    main()
