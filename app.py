import streamlit as st
import sys
import os

# Import the library
# If running locally from repo, we add src to path
try:
    from ckb_g2p import Converter
except ImportError:
    sys.path.insert(0, os.path.abspath("src"))
    from ckb_g2p import Converter

# Page Config
st.set_page_config(
    page_title="Central Kurdish G2P",
    page_icon="🗣️",
    layout="centered"
)

# Header
st.title("🗣️ Central Kurdish G2P")
st.markdown("""
Convert Central Kurdish (Sorani) text into **Syllabified IPA** (International Phonetic Alphabet).
This tool is optimized for Text-to-Speech (TTS) datasets.

* Powered by `ckb-textify` for normalization.
* Handles **Palatalization** (Heavy vs Light Ch/J).
* Handles **Stress** and **Pauses**.
""")

# Sidebar Config
st.sidebar.header("⚙️ Configuration")

use_stress = st.sidebar.checkbox(
    "Enable Stress Marking (ˈ)", 
    value=True,
    help="Adds primary stress marks. Detects negative verbs (Initial stress) vs Nouns (Final stress)."
)

use_pauses = st.sidebar.checkbox(
    "Enable Pause Markers (|)", 
    value=True,
    help="Converts punctuation into IPA pause boundaries (| and ||)."
)

do_normalize = st.sidebar.checkbox(
    "Enable Normalization", 
    value=True,
    help="Uses ckb-textify to convert numbers (1991), symbols ($), and Latin text to Kurdish phonemes."
)

# Initialize Converter
@st.cache_resource
def get_converter(stress, pauses, norm):
    return Converter(use_stress=stress, use_pause_markers=pauses, normalize=norm)

converter = get_converter(use_stress, use_pauses, do_normalize)

# Input Area
text_input = st.text_area(
    "Enter Kurdish Text:", 
    value="سڵاو، ناوی من ئازادە. ساڵی 1991 لە دایک بووم.",
    height=150
)

if st.button("Syllabify Text", type="primary"):
    if text_input.strip():
        try:
            # Run Conversion
            ipa_output = converter.syllabify(text_input)

            # Display Results
            st.subheader("🔤 IPA Output")

            # Using text_area for wrapping output and easy copying
            st.text_area(
                label="Result", 
                value=ipa_output, 
                height=200, 
                label_visibility="collapsed"
            )

            # Analysis Expander
            with st.expander("ℹ️ Detailed Analysis"):
                st.markdown(f"**Normalization Active:** `{do_normalize}`")
                st.markdown(f"**Stress Active:** `{use_stress}`")
                st.markdown(f"**Pause Markers:** `{use_pauses}`")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text.")

# Footer
st.markdown("---")
st.markdown("Developed by **Razwan M. Haji** | [GitHub Repo](https://github.com/RazwanSiktany/ckb_g2p) | [ckb-textify](https://ckb-textify.streamlit.app/)")
