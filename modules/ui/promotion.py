import os
import base64

import chess
import streamlit as st

from modules.game.game_manager import GameManager
from translations.i18n import t

PROMO_IMAGE = "assets/images/pawn.png"

# selection name -> python-chess piece type
_CHOICES = {
    "knight": chess.KNIGHT,
    "bishop": chess.BISHOP,
    "rook": chess.ROOK,
    "queen": chess.QUEEN,
}


def _image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _dialog_css():
    b64 = _image_base64(PROMO_IMAGE) if os.path.exists(PROMO_IMAGE) else ""
    selected = st.session_state.get("promotion_choice_name")
    highlight = ""
    if selected:
        highlight = (
            f".st-key-promo_{selected} button p {{"
            f" filter: drop-shadow(0 0 10px rgba(255,225,130,0.95)) !important; }}"
        )

    st.markdown(
        f"""
        <style>
        [data-testid="stDialog"] {{ background: transparent !important; }}
        div[role="dialog"] > div {{ background: transparent !important; }}

        div[role="dialog"] {{
            position: relative !important;
            width: 880px !important;
            max-width: 94vw !important;
            height: 587px !important;
            background-image: url("data:image/png;base64,{b64}");
            background-size: 100% 100%;
            background-repeat: no-repeat;
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0 !important;
        }}
        div[role="dialog"] button[aria-label="Close"] {{ display: none !important; }}

        div[role="dialog"] .stButton > button {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}
        div[role="dialog"] .stButton > button p {{
            font-size: 20px !important;
            font-weight: 700 !important;
            margin: 0 !important;
            white-space: nowrap !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: Georgia, "Times New Roman", serif;
            background: linear-gradient(180deg, #fbeaa0 0%, #e8c56d 45%, #a9791f 100%);
            -webkit-background-clip: text !important;
            background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            filter: drop-shadow(0 2px 2px rgba(0,0,0,0.8));
        }}

        .promo-title {{
            position: absolute;
            left: 37.7%;
            transform: translateY(17.5px);
            white-space: nowrap;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 28px;
            font-weight: 698;
            background: linear-gradient(180deg, #fbeaa0 0%, #e8c56d 45%, #a9791f 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 2px 2px rgba(0,0,0,0.8));
            z-index: 2;
        }}

        /* --- the four choices, each placed by CSS (own left / top) --- */
        .st-key-promo_knight, .st-key-promo_bishop,
        .st-key-promo_rook, .st-key-promo_queen {{
            position: absolute;
            top: 59.5%;                 /* the 4 labels: up/down */
            transform: translateX(-50%);
            width: 130px;
            z-index: 2;
        }}
        .st-key-promo_knight {{ left: 24.2%; }}
        .st-key-promo_bishop {{ left: 41.5%; }}
        .st-key-promo_rook   {{ left: 58%; }}
        .st-key-promo_queen  {{ left: 75%; }}

        .st-key-promo_confirm {{
            position: absolute;
            left: 50%;
            top: 73.3%;                 /* CONFIRM: up/down */
            transform: translateX(-50%);
            width: 198px;
            z-index: 2;
        }}
        {highlight}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.dialog(" ", width="large")
def _dialog(manager: GameManager):
    _dialog_css()
    lang = st.session_state.get("language", "en")

    # default choice is Queen (pre-highlighted)
    if "promotion_choice_name" not in st.session_state:
        st.session_state.promotion_choice_name = "queen"

    st.markdown("<div class='promo-title'>Promote Pawn</div>", unsafe_allow_html=True)

    if st.button(t("promotion_knight", lang), key="promo_knight", use_container_width=True):
        st.session_state.promotion_choice_name = "knight"
    if st.button(t("promotion_bishop", lang), key="promo_bishop", use_container_width=True):
        st.session_state.promotion_choice_name = "bishop"
    if st.button(t("promotion_rook", lang), key="promo_rook", use_container_width=True):
        st.session_state.promotion_choice_name = "rook"
    if st.button(t("promotion_queen", lang), key="promo_queen", use_container_width=True):
        st.session_state.promotion_choice_name = "queen"

    if st.button(t("difficulty_confirm", lang), key="promo_confirm", use_container_width=True):
        name = st.session_state.get("promotion_choice_name", "queen")
        frm = st.session_state.get("pending_promotion_from")
        to = st.session_state.get("pending_promotion_to")
        if frm is not None and to is not None:
            manager.make_move(frm, to, _CHOICES[name])
        for k in ("pending_promotion_from", "pending_promotion_to",
                  "promotion_choice_name", "selected_from_square"):
            st.session_state.pop(k, None)
        st.rerun()


def open_dialog(manager: GameManager):
    """Call from the game screen while a promotion is pending."""
    _dialog(manager)
