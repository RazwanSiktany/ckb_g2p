# generate_vocab.py
import json
import sys
import os

sys.path.insert(0, os.path.abspath("src"))
from ckb_g2p.constants import IPA_MAP

def generate_vocab():
    print("Generating vocab.json for TTS training...")

    unique_phonemes = set()
    for ipa_val in IPA_MAP.values():
        unique_phonemes.add(ipa_val)

    # Add special TTS tokens manually
    extras = {"t͡ʃ", "d͡ʒ", "ˈ", "|", "||", "ɪ"} 
    unique_phonemes.update(extras)

    sorted_phonemes = sorted(list(unique_phonemes))

    vocab_list = ["<pad>", "<eos>", "<bos>", " "] + sorted_phonemes

    vocab_map = { token: idx for idx, token in enumerate(vocab_list) }

    output_file = "vocab.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(vocab_map, f, ensure_ascii=False, indent=4)

    print(f"✅ Saved {len(vocab_map)} tokens to {output_file}")

if __name__ == "__main__":
    generate_vocab()
