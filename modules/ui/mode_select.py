import os
import base64
import streamlit as st
from functools import lru_cache
from translations.i18n import t
from modules.bot.stockfish_engine import StockfishEngine


MODE_IMAGE = "assets/images/mode.png"


@lru_cache(maxsize=1)
def _image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# =====================================================================
# STYLING (CSS inside the file).
# STATUS: PERMANENT. Full-screen background + gold gradient button text.
# =====================================================================
def _inject_style():
    if not os.path.exists(MODE_IMAGE):
        return

    b64 = _image_base64(MODE_IMAGE)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        header, #MainMenu, footer {{ visibility: hidden; }}
        .block-container {{ padding-top: 0 !important; }}

        /* transparent buttons — only the gold text shows, on the plaques */
        .stButton > button {{
            background: transparent;
            border: none;
            box-shadow: none;
        }}
        .stButton > button:hover,
        .stButton > button:active,
        .stButton > button:focus {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}
        /* the label text (a <p> inside the button): metallic gold + shadow */
        .stButton > button p {{
            font-size: 1.8vw !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            margin: 0 !important;
            font-family: Georgia, "Times New Roman", serif;
            background: linear-gradient(180deg, #fbeaa0 0%, #e8c56d 45%, #a9791f 100%);
            -webkit-background-clip: text !important;
            background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            filter: drop-shadow(0 2px 2px rgba(0,0,0,0.9))
                    drop-shadow(0 4px 6px rgba(0,0,0,0.5));
        }}
        /* --- each button is positioned INDEPENDENTLY here --- */
        .st-key-btn_back {{
            position: fixed;
            left: 3%;     /* Back: left/right */
            top: 4%;      /* Back: up/down    */
            width: 10vw;
        }}
        .st-key-btn_friend {{
            position: fixed;
            left: 36.7%;    /* friend: left/right (smaller = more left) */
            top: 57%;     /* friend: up/down    (smaller = higher)    */
            transform: translateX(-50%);
            width: 17vw;
        }}
        .st-key-btn_bot {{
            position: fixed;
            left: 64%;    /* AI: left/right */
            top: 58%;     /* AI: up/down    */
            transform: translateX(-50%);
            width: 17vw;
        }}
        /* the "Select Your Opponent" title, re-added at the top */
        .mode-title {{
            position: fixed;
            top: 7%;              /* title up/down */
            left: 50%;
            transform: translateX(-50%);
            font-family: Georgia, "Times New Roman", serif;
            font-size: 2.5vw;     /* title size */
            font-weight: 700;
            white-space: nowrap;
            background: linear-gradient(180deg, #fbeaa0 0%, #e8c56d 45%, #a9791f 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 2px 3px rgba(0,0,0,0.8));
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# THE MODE SELECT SCREEN.
# STATUS: PERMANENT — the real function app.py calls.
# =====================================================================
def render():
    _inject_style()
    lang = st.session_state.get("language", "en")

    # The screen title, re-added at the top (removed from the image).
    st.markdown(f"<div class='mode-title'>{t('mode_title', lang)}</div>", unsafe_allow_html=True)

    # Each button is positioned INDEPENDENTLY by CSS above
    # (the .st-key-btn_friend and .st-key-btn_bot rules). Move each one with its
    # own  left  and  top  values there — they no longer affect each other.

    if st.button(t("back_button", lang), key="btn_back", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()

    if st.button(t("play_with_friend", lang), key="btn_friend", use_container_width=True):
        st.session_state.mode = "friend"
        st.session_state.screen = "game"        # friend -> straight to the board
        st.rerun()

    if st.button(t("play_with_bot", lang), key="btn_bot", use_container_width=True):
        st.session_state.mode = "bot"
        if "preloaded_bot" not in st.session_state:
            st.session_state.preloaded_bot = StockfishEngine()   # load quietly, no spinner

        st.session_state.screen = "difficulty"    # bot -> pick difficulty first
        st.rerun()


# =====================================================================
# STANDALONE PREVIEW RUNNER.
# STATUS: PERSONAL + TEMPORARY — only runs when this file is run directly.
# =====================================================================
if __name__ == "__main__":
    st.set_page_config(page_title="Chess Game", page_icon="♟️", layout="wide")
    if "screen" not in st.session_state:
        st.session_state.screen = "mode"
    render()
