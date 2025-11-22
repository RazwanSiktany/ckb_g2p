# Central Kurdish G2P (ckb_g2p)

[![PyPI version](https://img.shields.io/pypi/v/ckb_g2p)](https://pypi.org/project/ckb-g2p/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ckb-g2p.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A linguistically accurate **Grapheme-to-Phoneme (G2P)** converter and **Syllabifier** for Central Kurdish (Sorani). 

Designed specifically for training modern **Text-to-Speech (TTS)** models (VITS, FastSpeech2, Glow-TTS) by providing robust phonetization, stress marking, and syllable boundaries.

## (کوردی) دەربارەی پڕۆژە

ئەم پڕۆژەیە ئامرازێکی پێشکەوتووە بۆ گۆڕینی دەقی کوردی (سۆرانی) بۆ فۆنێم و بڕگە. بەتایبەت دیزاین کراوە بۆ سیستەمەکانی دروستکردنی دەنگ  و ڕاهێنانی مۆدێلەکانی زیرەکی دەستکرد.


---

## 🌟 Why Use This?

Generic G2P tools often fail on Kurdish phonology. `ckb_g2p` solves these specific challenges:

| Feature | Problem in Generic Tools | Solution in `ckb_g2p`                                                                                                           |
| :--- | :--- |:--------------------------------------------------------------------------------------------------------------------------------|
| **Palatalization** | Treats all 'k' and 'g' the same. | Distinguishes **Heavy** (Postalveolar `t͡ʃ`, `d͡ʒ`) vs **Light** (Dental `t̪͡ʃ̟`, `d̪͡ʒ̟`) based on vowel context.              |
| **Schwa Insertion** | Fails on clusters like "grft". | Automatically inserts **Bizroka** (`/ɪ/`) to fix illegal consonant clusters (`gɪ.ɾɪft`).                                        |
| **Geminate Consonants** | Merges double letters. | Preserves true geminates or splits them if phonologically required (e.g., `dat̪͡ʃɛnn` → `da.t̪͡ʃ̟ɛ.ˈnɪn`).                      |
| **Stress (Prosody)** | Ignores stress. | Smartly assigns stress (`ˈ`). Handles **Negative Verb** shifts (`nachu` → `ˈna.t̪͡ʃ̟uː`) vs Nouns (`kurd` → `kurd`).            |
| **Complex Onsets** | Incorrectly splits clusters. | Respects valid onsets like `kw` and `cy` (`wusha` → `wu.ʃa`).                                                                   |

## 🔗 Live Demos

* **G2P Playground:** [ckb-g2p.streamlit.app](https://ckb-g2p.streamlit.app/)
* **Text Normalizer:** [ckb-textify.streamlit.app](https://ckb-textify.streamlit.app/)

---

## 📦 Installation

```bash
pip install ckb_g2p
```

**Dependencies:** This library automatically installs `ckb-textify` for normalizing numbers (`1991` → `hazar...`), dates, and symbols.

---

## 🚀 Usage

### Basic Conversion
```python
from ckb_g2p import Converter

# Default: Normalization=ON, Pauses=ON, Stress=OFF
converter = Converter()

text = "کوردستان"
ipa = converter.syllabify(text)
print(ipa)
# Output: kuɾ.dɪs.tän
```

### TTS-Ready Output (With Stress)
For training TTS models, you want explicit stress markers and pause tokens.

```python
# Enable stress marking
converter = Converter(use_stress=True, use_pause_markers=True)

# Handles negative verbs correctly (Stress on first syllable)
text = "نەچوو بۆ بازاڕ, لە ساڵی 1991."
ipa = converter.syllabify(text)

print(ipa)
# Output: ˈna.t̪͡ʃ̟uː bo̞ bä.ˈzäɾ | la sä.ˈɫiː ha.ˈzäɾ w no̞.ˈsad w na.ˈwa.du ˈjak ||
```

### Configuration Options

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `use_stress` | `bool` | `False` | Adds primary stress marker (`ˈ`) to the appropriate syllable. |
| `use_pause_markers` | `bool` | `True` | Converts punctuation to IPA boundaries (`\|` short, `\|\|` long). |
| `normalize` | `bool` | `True` | Uses `ckb-textify` to convert numbers/symbols to text before processing. |

---

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

---

## 🛠️ Customizing Pronunciation

If the rule-based engine fails on a specific word (e.g., a foreign name), you can manually override it by editing `src/ckb_g2p/resources/exceptions.csv` inside the package or locally mapping exceptions before processing.




---

## 🤝 Contributing

Contributions are welcome! 
1. Fork the repository.
2. Create a feature branch.
3. Submit a Pull Request.

## 👨‍💻 Author

Developed by **Razwan M. Haji**.

Special thanks to the open-source community and the contributors of `ckb-textify`.
