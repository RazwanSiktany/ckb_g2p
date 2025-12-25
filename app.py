import streamlit as st
import sys
import os

# Ensure we can import the library even if not installed via pip
sys.path.insert(0, os.path.abspath("src"))

try:
    from ckb_g2p.converter import Converter
except ImportError:
    st.error("❌ Could not import 'ckb_g2p'. Please ensure the 'src' directory exists.")
    st.stop()

# --- Page Configuration ---
st.set_page_config(
    page_title="Central Kurdish G2P",
    page_icon="🗣️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Layout and Typography ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap');

    /* General Text Area Styling (Base) */
    .stTextArea textarea {
        font-family: 'Calibri', 'Noto Naskh Arabic', sans-serif !important;
        font-size: 20px !important;
    }

    /* Targeting specific text areas by order to handle directionality 
       Input is the 1st text area -> RTL (Kurdish)
       Output is the 2nd text area -> LTR (IPA)
    */

    /* Input Area (1st) */
    .stTextArea:nth-of-type(1) textarea {
        direction: rtl;
        text-align: right;
    }

    /* Output Area (2nd) */
    .stTextArea:nth-of-type(2) textarea {
        direction: ltr;
        text-align: left;
        background-color: #f8f9fa;
        color: #333;
    }

    /* Descriptions in Kurdish */
    .kurdish-text {
        font-family: 'Noto Naskh Arabic', sans-serif;
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.title("🗣️ Central Kurdish G2P")
st.markdown("**Graph2Phon:** A modern, linguistically accurate Grapheme-to-Phoneme engine.")

st.markdown("""
<div class="kurdish-text">
ئەم ئەپڵیکەیشنە دەقی کوردی دەگۆڕێت بۆ فۆنێم و بڕگەکان (IPA). 
بەکاردێت بۆ سیستەمەکانی خوێندنەوەی دەق (TTS) و زیرەکی دەستکرد.
</div>
""", unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Configuration")

# 1. Output Format
output_mode = st.sidebar.radio(
    "Output Format",
    ["Syllabified (Stress)", "Flat IPA (Raw)"],
    index=0,
    help="Syllabified adds dots and stress markers. Flat IPA returns raw phonemes."
)

# 2. Normalization
do_normalize = st.sidebar.checkbox(
    "Normalize Numbers",
    value=True,
    help="Convert numbers (1991) to text (hazar...)"
)

# 3. Pause Markers
use_pauses = st.sidebar.checkbox(
    "Mark Pauses (|)",
    value=True,
    help="Insert | for short pauses and || for long pauses."
)

# 3. Caching Info
st.sidebar.markdown("---")
st.sidebar.info("💡 **Performance:** This app uses an SQLite cache to store processed words for instant retrieval.")

# --- Initialize Engine ---
# Use session_state to hold the converter instance instead of cache_resource
# if pickle issues occur with SQLite connections.
if 'converter' not in st.session_state:
    try:
        # Initialize with default options; arguments are handled at conversion time or init
        # We pass use_pause_markers=True to init, but logic in convert() handles it too.
        # Ideally, we pass it dynamically, but our class architecture sets it in init.
        # Let's instantiate it freshly.
        st.session_state.converter = Converter(use_cache=True, use_pause_markers=True)
    except Exception as e:
        st.error(f"Failed to initialize converter: {e}")
        st.stop()

converter = st.session_state.converter

# Update converter settings based on UI (if the class allows dynamic updates)
# Since 'use_pause_markers' is an attribute, we can update it.
converter.use_pause_markers = use_pauses

# --- Main Interface ---
text_input = st.text_area(
    "Enter Kurdish Text:",
    value="سڵاو، ناوی من ئازادە. ساڵی 1991 لە دایک بووم.",
    height=200,
    placeholder="دەقی کوردی لێرە بنووسە..."
)

# Map UI options to Engine options
format_arg = "syllables" if "Syllabified" in output_mode else "ipa"

if st.button("Convert (گۆڕین)", type="primary"):
    if text_input.strip():
        with st.spinner("Processing..."):
            try:
                # Process line by line to preserve newlines
                input_lines = text_input.split('\n')
                output_lines = []

                for line in input_lines:
                    if not line.strip():
                        output_lines.append("")  # Keep empty lines
                        continue

                    # Call the engine for this line
                    result = converter.convert(
                        line,
                        output_format=format_arg,
                        normalize=do_normalize
                    )

                    # Join results for this line
                    if format_arg == "syllables":
                        line_output = " ".join(result)
                    else:
                        line_output = "".join(result)

                    output_lines.append(line_output)

                # Reassemble the text
                display_text = "\n".join(output_lines)

                st.subheader("🔤 IPA Output")

                # Use text_area for output to allow wrapping (like ckb_textify app)
                st.text_area(
                    label="Output",
                    value=display_text,
                    height=200,
                    label_visibility="collapsed"
                )

                # Stats/Debug info
                total_tokens = sum(len(line.split()) for line in output_lines)
                st.caption(f"Tokens: {total_tokens}")

            except Exception as e:
                st.error(f"Error during conversion: {e}")
    else:
        st.warning("Please enter some text first.")

# --- Footer ---
st.markdown("---")
col_footer_1, col_footer_2, col_footer_3 = st.columns([1, 4, 1])
with col_footer_2:
    st.markdown(
        """
        <div style='text-align: center;'>
            <b>Developed by Razwan M. Haji</b><br>
            <a href="https://github.com/RazwanSiktany/ckb_g2p" target="_blank" style="text-decoration: none;">GitHub Repo</a> | 
            <a href="https://pypi.org/project/ckb-g2p/" target="_blank" style="text-decoration: none;">PyPI Package</a><br>
            <br>
            <small style='color: grey;'>Built with ❤️ for Kurdish Language Technology</small>
        </div>
        """,
        unsafe_allow_html=True
    )