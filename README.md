# Central Kurdish G2P (Graph2Phon)


[![PyPI version](https://img.shields.io/pypi/v/ckb_g2p)](https://pypi.org/project/ckb-g2p/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ckb-g2p.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A modern, high-performance, and linguistically accurate **Grapheme-to-Phoneme (G2P)** converter and **Syllabifier** for Central Kurdish (Sorani).

Designed specifically for training modern **Text-to-Speech (TTS)** models (VITS, FastSpeech2, Glow-TTS) by providing robust phonetization, stress marking, and syllable boundaries.

## (کوردی) دەربارەی پڕۆژە

ئەم پڕۆژەیە ئامرازێکی پێشکەوتووە بۆ گۆڕینی دەقی کوردی (سۆرانی) بۆ فۆنێم و بڕگە. بەتایبەت دیزاین کراوە بۆ سیستەمەکانی دروستکردنی دەنگ  و ڕاهێنانی مۆدێلەکانی زیرەکی دەستکرد.

خێراییەکی زۆر بەرزی هەیە و هەموو یاسا دەنگییەکانی زمانی کوردی (وەک پاڵاتەڵایزەیشن، بزرۆکە، و فۆکەس) لەخۆدەگرێت.

## 🔗 Live Demos

* **G2P Playground:** [ckb-g2p.streamlit.app](https://ckb-g2p.streamlit.app/)
* **Text Normalizer:** [ckb-textify.streamlit.app](https://ckb-textify.streamlit.app/)

## 🌟 Why Graph2Phon?

Generic G2P tools often fail on Kurdish phonology. `ckb-g2p` (v3) combines architectural speed with linguistic depth to solve these challenges:

| Feature | Problem in Generic Tools | Solution in `ckb-g2p` |
| :--- | :--- | :--- |
| **Palatalization** | Treats all 'k' and 'g' the same. | Distinguishes **Heavy** (Postalveolar `t͡ʃ`, `d͡ʒ`) vs **Light** (Dental `t̪͡ʃ̟`, `d̪͡ʒ̟`) based on vowel context (e.g. `kwê` → `chwê`). |
| **Schwa Insertion** | Fails on clusters like "grft". | Automatically inserts **Bizroka** (`/ɪ/`) to fix illegal consonant clusters (`gɪ.ɾɪft`) using Sonority Sequencing Principles. |
| **Stress (Prosody)** | Ignores stress. | Smartly assigns stress (`ˈ`). Handles **Negative Verb** shifts (`nachu` → `ˈna.t̪͡ʃ̟uː`) vs Nouns (`kurd` → `kuɾd`). |
| **Ambiguity** | Confuses `w` (u/w) and `y` (i/y). | Uses a generator-evaluator pipeline to pick the most phonotactically valid pronunciation. |
| **Dialect Support** | Normalizes all sounds. | Preserves emphatic consonants (`sˤ`, `tˤ`, `zˤ`) critical for authentic pronunciation. |

## 🚀 Installation

### From PyPI
```bash
pip install ckb-g2p
```

### From Source
```bash
git clone [https://github.com/RazwanSiktany/ckb_g2p.git](https://github.com/RazwanSiktany/ckb_g2p.git)
cd ckb_g2p
pip install -e .
```

## 💻 Usage

### Command Line Interface (CLI)
You can use the tool directly from your terminal:

```bash
# Basic usage (Syllabified)
ckb-g2p "سڵاو کوردستان"
# Output: sɪ.ˈɫäw kuɾ.dɪs.ˈtän

# Raw IPA (No stress, no syllable markers)
ckb-g2p "سڵاو" --format ipa --no-stress
# Output: sɪɫäw

# Batch Processing (Great for datasets)
ckb-g2p -i input.txt -o output.txt
```

### Python API
```python
from ckb_g2p.converter import Converter

# Initialize (loads cache by default)
converter = Converter()

# 1. Basic Syllabification
text = "من کوردم"
ipa = converter.convert(text, output_format="syllables")
print(ipa) 
# Output: ['mɪn', 'kuɾ.ˈdɪm']

# 2. TTS-Ready Output (with Pauses)
# Note: Punctuation is automatically converted to pauses (| and ||)
text = "سڵاو، ناوت چییە؟"
ipa_list = converter.convert(text, output_format="syllables")
print(" ".join(ipa_list))
# Output: sɪ.ˈɫäw | näwt ˈt͡ʃiː.ja ||
```

## 🗣️ Phoneme Inventory

We use a precise IPA set to capture allophonic variations critical for natural speech synthesis.

### Consonants (Key Distinctions)
| Grapheme | IPA | Type | Description |
| :--- | :--- | :--- | :--- |
| **چ** | `t̪͡ʃ̟` | **Light (Dental)** | Standard "ch". Tongue tip touches teeth. |
| **ک** | `t͡ʃ` | **Heavy (Postalveolar)** | Palatalized /k/ before front vowels (i, e, y). Like English "Chair". |
| **ج** | `d̪͡ʒ̟` | **Light (Dental)** | Standard "j". Tongue tip touches teeth. |
| **گ** | `d͡ʒ` | **Heavy (Postalveolar)** | Palatalized /g/ before front vowels. Like English "Jack". |
| **ڵ** | `ɫ` | **Velarized** | "Dark L", distinct from clear `l`. |
| **ڕ** | `r` | **Trill** | Rolled R, distinct from tap `ɾ`. |
| **ص** | `sˤ` | **Emphatic** | Emphatic 'S' (Sad), preserved for dialectal accuracy. |

## ⚡ Performance & Caching

Graph2Phon uses a local SQLite database (`lexicon.db`) to store processed words. 
* **First Run:** Calculates phonemes (~1-5ms per word).
* **Second Run:** Fetches from cache (<0.1ms per word).

To disable caching:
```python
converter = Converter(use_cache=False)
```

## 🛠️ Configuration & Exceptions

The engine is driven by a YAML configuration file located at `src/ckb_g2p/data/phonology.yaml`.

**Manual Overrides:**
If the rule-based engine fails on a specific word (e.g., a foreign name), add it to `src/ckb_g2p/resources/exceptions.csv`


## 🤝 Contributing
Contributions are welcome! Please run the test suite before submitting a PR:

```bash
pip install pytest
pytest
```

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.

## 👨‍💻 Author
Developed by **Razwan M. Haji**.