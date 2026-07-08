import os
import base64
import streamlit as st
from translations.i18n import t

HOME_IMAGE = "assets/images/home.png"


def _image_base64(path):
    """Read an image file and turn it into text CSS can use as a background."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# =====================================================================
# STYLING (CSS inside the file).
# STATUS: PERMANENT.
# Sets the full-screen fixed background, hides Streamlit's default top bar
# for a clean look, and styles the Begin Game button like a plaque.
# =====================================================================
def _inject_style():
    if not os.path.exists(HOME_IMAGE):
        return  # no image yet — skip the background so the screen still runs

    b64 = _image_base64(HOME_IMAGE)
    st.markdown(
        f"""
        <style>
        /* full-window background image that does NOT scroll */
        .stApp {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* hide Streamlit's top toolbar / menu / footer for a full-screen feel */
        header, #MainMenu, footer {{ visibility: hidden; }}
        .block-container {{ padding-top: 0 !important; }}

        /* Begin Game: transparent, so the pictured plaque shows through and
           only the gold text appears INSIDE the plaque frame. */
        .stButton > button {{
            background: transparent;
            border: none;
            box-shadow: none;
            color: #ead9a8;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 58px;
            letter-spacing: 3px;
            text-transform: uppercase;
            font-weight: 700;
            white-space: nowrap;
            padding: 4px 0;
            text-shadow: 0 2px 4px;
        }}
        .stButton > button:hover {{
            background: transparent;
            border: none;
            color: #f6ecc8;
            text-shadow: 0 2px 4px;
        }}
        .stButton > button:active, .stButton > button:focus {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #f6ecc8 !important;
        }}
        /* the label text sits in a <p> INSIDE the button — this is what
           actually controls the size. Change 58px here to resize the text. */
        .stButton > button p {{
            font-size: 3vw !important;
            font-weight: 700 !important;
            letter-spacing: 3px !important;
            margin: 0 !important;
            text-shadow: 0 2px 2px rgba(0,0,0,0.85),
                         0 4px 8px rgba(0,0,0,0.65) !important;
        }}
        /* language button on the top-right plaque (label stays "EN/AR") */
        .st-key-lang_btn {{
            position: fixed;
            top: 1.5%;        /* plaque up/down */
            right: 1.8%;      /* plaque left/right */
            width: 100px;
            z-index: 10;
        }}
        .st-key-lang_btn .stButton > button p {{
            font-size: 1.3vw !important;   /* small, unlike Begin Game */
            letter-spacing: 2px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# THE HOME SCREEN.
# STATUS: PERMANENT — the real function app.py calls.
# =====================================================================
def render():
    _inject_style()

    # language button on the top-right plaque (label stays "EN/AR")
    if "language" not in st.session_state:
        st.session_state.language = "en"
    if st.button("EN/AR", key="lang_btn"):
        st.session_state.language = "ar" if st.session_state.language == "en" else "en"
        st.rerun()

    # Push the button down so its text lands INSIDE the plaque in the image.
    # Change 70vh to move it: smaller = higher, larger = lower.
    st.markdown("<div style='height:63.5vh'></div>", unsafe_allow_html=True)

    # Center the button over the plaque. Middle number = width. Making the left
    # number smaller / right bigger slides the button LEFT (and vice versa).
    left, mid, right = st.columns([3.2, 2, 3.3])
    with mid:
        if st.button(t("home_start_button", st.session_state.language), use_container_width=True):
            st.session_state.screen = "mode"   # go to mode-select page
            st.rerun()


# =====================================================================
# STANDALONE PREVIEW RUNNER.
# STATUS: PERSONAL + TEMPORARY — only runs when this file is run directly.
# =====================================================================
if __name__ == "__main__":
    st.set_page_config(page_title="Chess Game", page_icon="♟️", layout="wide")
    if "screen" not in st.session_state:
        st.session_state.screen = "home"
    render()
