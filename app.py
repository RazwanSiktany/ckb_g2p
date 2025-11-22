import streamlit as st
import sys
import os

# Import the library
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

# --- CUSTOM CSS FOR FONT & RTL ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic&display=swap');

    /* Apply font to input text areas */
    .stTextArea textarea {
        font-family: 'Calibri', 'Noto Naskh Arabic', sans-serif !important;
        font-size: 14px !important;
        direction: rtl; /* Input should be RTL for Kurdish */
    }

    /* Apply font to output code blocks/text areas */
    div[data-testid="stText"] {
        font-family: 'Calibri', sans-serif !important;
        font-size: 14px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("🗣️ Central Kurdish G2P")

st.markdown("""
Convert Central Kurdish (Sorani) text into **Syllabified IPA** (International Phonetic Alphabet).
This tool is optimized for Text-to-Speech (TTS) datasets.
""")

# Kurdish Description (Cleaned - No English mixing inside sentences)
st.markdown("""
<div style="direction: rtl; text-align: right; font-family: 'Noto Naskh Arabic', sans-serif;">
ئەم ئەپڵیکەیشنە دەقی کوردی دەگۆڕێت بۆ فۆنێم و بڕگەکان. ئەمەش سوودی هەیە بۆ سیستەمەکانی دروستکردنی دەنگ.
</div>
""", unsafe_allow_html=True)

# Sidebar Config
st.sidebar.header("⚙️ Configuration")

use_stress = st.sidebar.checkbox("Enable Stress (ˈ)", value=True)
use_pauses = st.sidebar.checkbox("Enable Pauses (|)", value=True)
do_normalize = st.sidebar.checkbox("Enable Normalization", value=True)

# Initialize Converter
@st.cache_resource
def get_converter(stress, pauses, norm):
    return Converter(use_stress=stress, use_pause_markers=pauses, normalize=norm)

converter = get_converter(use_stress, use_pauses, do_normalize)

# Input Area
text_input = st.text_area(
    "Enter Kurdish Text (دەقی کوردی بنووسە):", 
    value="سڵاو، ناوی من ئازادە. ساڵی 1991 لە دایک بووم.",
    height=150
)

if st.button("Syllabify Text (گۆڕین)", type="primary"):
    if text_input.strip():
        try:
            ipa_output = converter.syllabify(text_input)
            st.subheader("🔤 IPA Output")

            # Output Area (Force LTR for IPA, but keep font settings)
            st.markdown(f'<textarea readonly style="width:100%; height:200px; font-family:Calibri; font-size:14px; direction:ltr; border-radius:5px; border:1px solid #ccc; padding:10px;">{ipa_output}</textarea>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text.")

# Footer
st.markdown("---")
st.markdown("Developed by **Razwan M. Haji** | [GitHub](https://github.com/RazwanSiktany/ckb_g2p) | [PyPI](https://pypi.org/project/ckb-g2p/)")
