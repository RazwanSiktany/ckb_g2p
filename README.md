# Central Kurdish G2P (ckb_g2p)

[![PyPI version](https://badge.fury.io/py/ckb_g2p.svg)](https://badge.fury.io/py/ckb_g2p)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ckb-g2p.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A linguistically accurate **Grapheme-to-Phoneme (G2P)** converter and **Syllabifier** for Central Kurdish (Sorani), designed specifically for modern Text-to-Speech (TTS) pipelines (VITS, FastSpeech2, etc.).

## 🔗 Live Demos & Resources

| Project | Description | Links |
| :--- | :--- | :--- |
| **ckb_g2p** | Phonemizer & Syllabifier | [**Live G2P Demo**](https://ckb-g2p.streamlit.app/) • [GitHub](https://github.com/RazwanSiktany/ckb_g2p) |
| **ckb-textify** | Text Normalizer (Prerequisite) | [**Live Normalizer Demo**](https://ckb-textify.streamlit.app/) • [GitHub](https://github.com/RazwanSiktany/ckb_textify) |

---

## ✨ Key Features

This library handles the complex phonological rules that generic G2P tools miss:

1.  **Context-Aware Palatalization:**
    * Distinguishes between the **Dental Affricates** (standard `چ` / `ج`) and **Postalveolar Affricates** (palatalized `ک` / `گ`).
    * *Example:* `کێوار` → `t͡ʃɛ.wäɾ` (Heavy) vs `چێوار` → `t̪͡ʃ̟ɛ.wäɾ` (Light).
2.  **Schwa (Bizroka) Insertion:**
    * Automatically inserts `/ɪ/` to break illegal consonant clusters based on sonority rules.
    * *Example:* `گرفت` (grft) → `gɪ.ɾɪft`.
3.  **Advanced Syllabification:**
    * Respects complex onsets (e.g., `kw`, `cy`) while splitting others correctly.
    * *Example:* `ووشە` → `wu.ʃa`.
4.  **Prosody & Stress (Configurable):**
    * **Noun/Adj:** Stress on final syllable (`ˈ`).
    * **Negative Verbs:** Stress shifts to initial syllable (e.g., `نەچوو` → `ˈna.t̪͡ʃ̟uː`).
5.  **Foreign Text Support:**
    * Powered by [ckb-textify](https://github.com/RazwanSiktany/ckb_textify). Automatically converts numbers (`1991`), symbols (`$`), and English text to Kurdish phonemes before processing.

---

## 📦 Installation

```bash
pip install ckb_g2p
```

---

## 🚀 Usage

### 1. Basic Usage (Python)

```python
from ckb_g2p import Converter

# Initialize (Default: Stress=OFF, Pauses=ON, Normalization=ON)
converter = Converter()

text = "کوردستان"
ipa = converter.syllabify(text)
print(ipa)
# Output: kuɾ.dɪs.tän
```

### 2. Advanced TTS Configuration

You can toggle specific features to match your TTS model's requirements.

```python
# Initialize with specific TTS options
converter = Converter(
    use_stress=True,        # Mark primary stress (ˈ)
    use_pause_markers=True, # Convert punctuation to | and ||
    normalize=True          # Use ckb-textify to clean text first
)

text = "نەچوو بۆ بازاڕ, لە ساڵی 1991."
ipa = converter.syllabify(text)

print(ipa)
# Output: ˈna.t̪͡ʃ̟uː bo̞ bä.ˈzäɾ | la sä.ˈɫiː ha.ˈzäɾ w no̞.ˈsad w na.ˈwa.du ˈjak ||
```

### Configuration Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `use_stress` | `bool` | `False` | Adds `ˈ` to the stressed syllable. Smartly handles negative verbs. |
| `use_pause_markers` | `bool` | `True` | Converts punctuation to IPA pause boundaries (`|` short, `||` long). |
| `normalize` | `bool` | `True` | Uses `ckb-textify` to convert numbers, symbols, and Latin text before G2P. |

---

## 🗣️ Phoneme Set

To ensure high-quality audio generation, we use precise IPA notation to distinguish allophones:

| Grapheme | Sound Type | IPA | Description |
| :--- | :--- | :--- | :--- |
| **چ** | Standard | `t̪͡ʃ̟` | **Light / Dental:** Tongue touches teeth. |
| **ج** | Standard | `d̪͡ʒ̟` | **Light / Dental:** Tongue touches teeth. |
| **ک** | Palatalized | `t͡ʃ` | **Heavy / Postalveolar:** Like English "Chair". (Before `i`, `e`, `y`) |
| **گ** | Palatalized | `d͡ʒ` | **Heavy / Postalveolar:** Like English "Jack". (Before `i`, `e`, `y`) |

---

## 🤝 Contributing

Contributions are welcome! Whether it's fixing a bug, improving phonological rules, or adding documentation, please feel free to submit a Pull Request on GitHub.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 👨‍💻 Author

Developed by **Razwan M. Haji**.

Special thanks to the open-source community and the contributors of `ckb-textify`, `eng-to-ipa`, and `anyascii`.
