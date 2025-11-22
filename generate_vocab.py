# generate_vocab.py
import json
import sys
import os

sys.path.insert(0, os.path.abspath("src"))
from ckb_g2p.constants import IPA_MAP

def generate_vocab():
    print("Generating vocab.json...")
    unique_phonemes = set(IPA_MAP.values())
    extras = {"t͡ʃ", "d͡ʒ", "ˈ", "|", "||", "ɪ"} 
    unique_phonemes.update(extras)
    sorted_phonemes = sorted(list(unique_phonemes))
    vocab_list = ["<pad>", "<eos>", "<bos>", " "] + sorted_phonemes
    vocab_map = { token: idx for idx, token in enumerate(vocab_list) }

    with open("vocab.json", "w", encoding="utf-8") as f:
        json.dump(vocab_map, f, ensure_ascii=False, indent=4)
    print("Done.")

if __name__ == "__main__":
    generate_vocab()
