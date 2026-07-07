"""
RESULT / VICTORY POPUP  —  Chess project
Owner: Ruba.  (UI only.)

Shown when the game is over and a side has won. Background = victory.png.
The middle shows the winner (White / Black / Bot) and, if the backend gives it,
the reason (e.g. "by Checkmate"). Two buttons: Play Again (left) and Main Page (right).

Opened from game.py when the game is over:
    from modules.ui import result
    result.open_dialog(manager)
"""

import os
import base64

import streamlit as st

from modules.game.game_manager import GameManager
from modules.shared.enums.game_mode import GameMode
from modules.shared.enums.player_color import PlayerColor
from modules.shared.enums.game_end_reason import GameEndReason

RESULT_IMAGE = "assets/images/victory.png"


def _image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _winner_and_reason(manager: GameManager):
    """Read the winner and end reason from the backend game state."""
    state = manager.get_game_state()
    winner = state.winner if state else None
    end_reason = state.end_reason if state else None
    mode_raw = st.session_state.get("mode", GameMode.FRIEND.value)

    # winner label: White / Black / Bot
    if winner == PlayerColor.WHITE:
        winner_text = "White"
    elif winner == PlayerColor.BLACK:
        # in bot mode the black side is the bot
        winner_text = "Bot" if mode_raw == GameMode.BOT.value else "Black"
    else:
        winner_text = ""   # no winner (no draws expected)

    # reason (only what the backend actually reports)
    reason_text = ""
    if end_reason == GameEndReason.CHECKMATE:
        reason_text = "by Checkmate"
    # "on Time" would go here once the TimerManager is wired into the backend.

    return winner_text, reason_text


def _dialog_css():
    b64 = _image_base64(RESULT_IMAGE) if os.path.exists(RESULT_IMAGE) else ""
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

        /* winner text in the middle (top:% doesn't work here, use translateY) */
        .result-winner {{
            position: absolute; left: 50%; top: 0;
            transform: translateX(-50%) translateY(273px);   /* winner: down/up */
            white-space: nowrap; text-align: center;
            font-family: Georgia, "Times New Roman", serif; font-weight: 700;
            font-size: 34px; color: #f4e4a2;
            text-shadow: 0 2px 3px rgba(0,0,0,0.75); z-index: 2;
        }}
        .result-reason {{
            position: absolute; left: 50%; top: 0;
            transform: translateX(-50%) translateY(310px);    /* reason: down/up */
            white-space: nowrap; text-align: center;
            font-family: Georgia, "Times New Roman", serif; font-weight: 600;
            font-size: 20px; color: #cdb46e;
            text-shadow: 0 2px 3px rgba(0,0,0,0.7); z-index: 2;
        }}

        /* the two buttons */
        .st-key-btn_again, .st-key-btn_home {{
            position: absolute; top: 76%; transform: translateX(-50%); width: 166px; z-index: 2;
        }}
        .st-key-btn_again {{ left: 38%; }}    /* Play Again: left/right */
        .st-key-btn_home  {{ left: 62.1%; }}  /* Main Page:  left/right */
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.dialog(" ", width="large")
def _dialog(manager: GameManager):
    _dialog_css()
    winner_text, reason_text = _winner_and_reason(manager)

    if winner_text:
        st.markdown(f"<div class='result-winner'>{winner_text} Wins</div>",
                    unsafe_allow_html=True)
    if reason_text:
        st.markdown(f"<div class='result-reason'>{reason_text}</div>",
                    unsafe_allow_html=True)

    if st.button("PLAY AGAIN", key="btn_again", use_container_width=True):
        manager.restart_game()
        for k in ("selected_from_square", "pending_promotion_from",
                  "pending_promotion_to", "promotion_choice_name"):
            st.session_state.pop(k, None)
        st.session_state.screen = "game"
        st.rerun()

    if st.button("MAIN PAGE", key="btn_home", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()


def open_dialog(manager: GameManager):
    """Call from the game screen when the game is over."""
    _dialog(manager)
