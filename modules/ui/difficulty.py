import os
import base64
import streamlit as st
from functools import lru_cache
from translations.i18n import t

DIFF_IMAGE = "assets/images/select.png"


@lru_cache(maxsize=1)
def _image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _dialog_css():
    b64 = _image_base64(DIFF_IMAGE) if os.path.exists(DIFF_IMAGE) else ""
    selected = st.session_state.get("difficulty")
    highlight = ""
    if selected:
        highlight = (
            f".st-key-diff_{selected} button p {{"
            f" filter: drop-shadow(0 0 10px rgba(255,225,130,0.95)) !important; }}"
        )

    st.markdown(
        f"""
        <style>
        [data-testid="stDialog"] {{ background: transparent !important; }}
        div[role="dialog"] > div {{ background: transparent !important; }}

        /* the popup = the ornate image; position: relative makes it the frame
           the buttons are placed inside */
        div[role="dialog"] {{
            position: relative !important;
            width: 860px !important;
            max-width: 94vw !important;
            height: 573px !important;
            background-image: url("data:image/png;base64,{b64}");
            background-size: 100% 100%;
            background-repeat: no-repeat;
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0 !important;
        }}
        div[role="dialog"] button[aria-label="Close"] {{ display: none !important; }}

        /* buttons: transparent, gold gradient text, never wrap */
        div[role="dialog"] .stButton > button {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}
        div[role="dialog"] .stButton > button p {{
            font-size: 26px !important;
            font-weight: 700 !important;
            margin: 0 !important;
            white-space: nowrap !important;
            font-family: Georgia, "Times New Roman", serif;
            background: linear-gradient(180deg, #fbeaa0 0%, #e8c56d 45%, #a9791f 100%);
            -webkit-background-clip: text !important;
            background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            filter: drop-shadow(0 2px 2px rgba(0,0,0,0.8));
        }}

        /* the title */
        .diff-title {{
            position: absolute;
            left: 50%;
            /* move the title DOWN: increase 40px (negative value = up) */
            transform: translateX(-48%) translateY(-10px);
            white-space: nowrap;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 30px;
            font-weight: 550;
            background: linear-gradient(180deg, #fbeaa0 0%, #e8c56d 45%, #a9791f 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 2px 2px rgba(0,0,0,0.8));
        }}

        /* --- the three cards, each placed by CSS (own left / top) --- */
        .st-key-diff_easy, .st-key-diff_medium, .st-key-diff_hard {{
            position: absolute;
            top: 64%;
            transform: translateX(-50%);
            width: 150px;
        }}
        .st-key-diff_easy   {{ left: 23.5%; transform: translateX(calc(-50% - 5px)); }}   /* EASY */
        .st-key-diff_medium {{ left: 50%; }}   /* MEDIUM: left/right */
        .st-key-diff_hard   {{ left: 77.5%; }}   /* HARD: left/right   */

        /* CONFIRM */
        .st-key-diff_confirm {{
            position: absolute;
            left: 50%;
            top: 80%;
            transform: translateX(calc(-50% - 2px));
            width: 190px;
        }}
        {highlight}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.dialog(" ", width="large")
def _dialog():
    _dialog_css()
    lang = st.session_state.get("language", "en")

    # everything below is placed by the CSS above (no spacers, no columns)
    st.markdown(f"<div class='diff-title'>{t('difficulty_title', lang)}</div>", unsafe_allow_html=True)

    if st.button(t("difficulty_easy", lang), key="diff_easy", use_container_width=True):
        st.session_state.difficulty = "easy"
        st.session_state.screen = "game"
        st.rerun()
    if st.button(t("difficulty_medium", lang), key="diff_medium", use_container_width=True):
        st.session_state.difficulty = "medium"
        st.session_state.screen = "game"
        st.rerun()
    if st.button(t("difficulty_hard", lang), key="diff_hard", use_container_width=True):
        st.session_state.difficulty = "hard"
        st.session_state.screen = "game"
        st.rerun()

    if st.button(t("difficulty_confirm", lang), key="diff_confirm", use_container_width=True):
        if "difficulty" not in st.session_state:
            st.session_state.difficulty = "medium"
        st.session_state.screen = "game"
        st.rerun()


def open_dialog():
    """Call this from another screen to pop the difficulty dialog open."""
    _dialog()


# =====================================================================
# STANDALONE PREVIEW RUNNER.
# =====================================================================
if __name__ == "__main__":
    st.set_page_config(page_title="Chess Game", page_icon="♟️", layout="wide")
    if st.session_state.get("screen") == "game":
        st.success(f"Confirmed! difficulty = {st.session_state.get('difficulty')} "
                   f"(the game board would load here)")
    else:
        open_dialog()
