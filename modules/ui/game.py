import os
import base64

import chess
import streamlit as st

from modules.game.game_manager import GameManager
from modules.game.timer_manager import TimerManager
from modules.shared.enums.game_mode import GameMode
from modules.shared.enums.game_status import GameStatus
from modules.shared.enums.difficulty import Difficulty
from modules.shared.enums.player_color import PlayerColor
from translations.i18n import t
from modules.ui import promotion, result

GAME_IMAGE = "assets/images/Game.png"

# glyph colors
_WHITE_PIECE = "#f3e8cc"
_BLACK_PIECE = "#20140b"

# use the SOLID glyph for both colors (color/outline distinguishes them)
_SOLID_GLYPH = {
    chess.PAWN: "♟", chess.KNIGHT: "♞", chess.BISHOP: "♝",
    chess.ROOK: "♜", chess.QUEEN: "♛", chess.KING: "♚",
}

# starting material for computing captured pieces
_START_COUNTS = {chess.PAWN: 8, chess.KNIGHT: 2, chess.BISHOP: 2,
                 chess.ROOK: 2, chess.QUEEN: 1, chess.KING: 1}


# =====================================================================
# session helpers
# =====================================================================
def _mode_from_session() -> GameMode:
    raw = st.session_state.get("mode", GameMode.FRIEND.value)
    return GameMode.BOT if raw == GameMode.BOT.value else GameMode.FRIEND


def _difficulty_from_session() -> Difficulty:
    raw = st.session_state.get("difficulty", Difficulty.MEDIUM.value)
    for d in Difficulty:
        if d.value == raw:
            return d
    return Difficulty.MEDIUM


def _ensure_game_started(manager: GameManager) -> None:
    mode = _mode_from_session()
    difficulty = _difficulty_from_session() if mode == GameMode.BOT else None
    state = manager.get_game_state()
    if state is None or state.game_mode != mode or (
        mode == GameMode.BOT and state.difficulty != difficulty
    ):
        manager.start_game(game_mode=mode, difficulty=difficulty)
        st.session_state.timer_needs_reset = True


def _clear_move_state() -> None:
    st.session_state.pop("selected_from_square", None)
    st.session_state.pop("pending_promotion_from", None)
    st.session_state.pop("pending_promotion_to", None)


def _prepare_new_game(manager: GameManager) -> None:
    manager.restart_game()
    _clear_move_state()
    st.session_state.pop("result_reason", None)
    st.session_state.timer_needs_reset = True


_TIME_CONTROL_SECONDS = 600   # 10 minutes per side (change this for a different clock)


def _format_clock(seconds: float) -> str:
    s = max(0, int(seconds))
    return f"{s // 60}:{s % 60:02d}"


def _sync_timer() -> None:
    """Create the clock for a fresh game, or reset it when a new game starts."""
    if "timer" not in st.session_state or st.session_state.pop("timer_needs_reset", False):
        timer = TimerManager(initial_seconds=_TIME_CONTROL_SECONDS)
        timer.start(PlayerColor.WHITE)   # white's clock starts first
        st.session_state.timer = timer
        st.session_state.pop("result_reason", None)


def _timer_switch() -> None:
    """Pass the clock to the other player after a move."""
    timer = st.session_state.get("timer")
    if timer is not None:
        timer.switch()


@st.fragment(run_every="1s")
def _render_clocks() -> None:
    """Draw both clocks and tick them once a second (only this reruns, not the board)."""
    manager = st.session_state.get("game_manager")
    timer = st.session_state.get("timer")
    if manager is None or timer is None:
        return

    if manager.is_game_over() or st.session_state.get("result_reason"):
        timer.pause()   # freeze the clocks once the game is over
    else:
        loser = timer.is_time_up()
        if loser is not None:
            # the player who ran out loses; the other wins on time
            winner = PlayerColor.WHITE if loser == PlayerColor.BLACK else PlayerColor.BLACK
            manager.end_game(winner)
            timer.stop()
            st.session_state.result_reason = "on Time"
            st.rerun()   # full rerun so the result popup opens

    black = _format_clock(timer.get_remaining_time(PlayerColor.BLACK))
    white = _format_clock(timer.get_remaining_time(PlayerColor.WHITE))
    st.markdown(f"<div class='g-gold g-opptime'>⏱ {black}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-gold g-youtime'>⏱ {white}</div>", unsafe_allow_html=True)


# =====================================================================
# move handling (click to select, click to move, + promotion)
# =====================================================================
def _try_select(square: int, board: chess.Board) -> None:
    piece = board.piece_at(square)
    if piece is None or piece.color != board.turn:
        return
    if any(m.from_square == square for m in board.legal_moves):
        st.session_state.selected_from_square = square


def _handle_click(manager: GameManager, clicked: int, language: str) -> None:
    board = manager.get_board()
    legal = list(board.legal_moves)
    selected = st.session_state.get("selected_from_square")

    if selected is None:
        _try_select(clicked, board)
        return

    if clicked == selected:
        st.session_state.selected_from_square = None
        return

    matches = [m for m in legal if m.from_square == selected and m.to_square == clicked]
    if not matches:
        st.session_state.selected_from_square = None
        _try_select(clicked, board)
        return

    if any(m.promotion is not None for m in matches):
        st.session_state.pending_promotion_from = selected
        st.session_state.pending_promotion_to = clicked
        st.session_state.selected_from_square = None
        return

    moves = manager.make_move(selected, clicked, None)
    # Switch the clock once per executed move (player, then possibly bot).
    for _ in range(moves):
        _timer_switch()
    st.session_state.selected_from_square = None


# =====================================================================
# captured-pieces (computed from the board — pure UI, no backend change)
# =====================================================================
def _captured(board: chess.Board):
    on_board = {chess.WHITE: {}, chess.BLACK: {}}
    for piece in board.piece_map().values():
        on_board[piece.color][piece.piece_type] = \
            on_board[piece.color].get(piece.piece_type, 0) + 1

    def missing(color):
        glyphs = ""
        for ptype, start in _START_COUNTS.items():
            gone = start - on_board[color].get(ptype, 0)
            if gone > 0 and ptype != chess.KING:
                glyphs += chess.Piece(ptype, color).unicode_symbol() * gone
        return glyphs

    # pieces WHITE captured = black pieces missing, and vice versa
    return missing(chess.BLACK), missing(chess.WHITE)


def _square_key(board: chess.Board, square: int) -> str:
    piece = board.piece_at(square)
    if piece is None:
        return f"sqe_{square}"
    color = "w" if piece.color == chess.WHITE else "b"
    typ = piece.symbol().upper()          # P N B R Q K
    return f"sq{color}{typ}_{square}"     # e.g. sqwN_12


# =====================================================================
# STYLING
# =====================================================================
def _inject_style(board: chess.Board) -> None:
    b64 = ""
    if os.path.exists(GAME_IMAGE):
        with open(GAME_IMAGE, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

    # highlight selected square + legal targets
    selected = st.session_state.get("selected_from_square")
    highlight = ""
    if selected is not None:
        # no box on the selected square — only the dots/rings on the targets
        for m in board.legal_moves:
            if m.from_square != selected:
                continue
            tkey = _square_key(board, m.to_square)
            if board.piece_at(m.to_square) is None:
                # empty square -> centered dot; light dot on dark squares and
                # dark dot on light squares so it always shows
                is_light = (chess.square_file(m.to_square)
                            + chess.square_rank(m.to_square)) % 2 == 1
                dot = "rgba(35,25,15,0.40)" if is_light else "rgba(240,226,192,0.60)"
                highlight += (
                    f".st-key-{tkey} > .stButton > button "
                    f"{{ background-image: radial-gradient(circle at 50% 50%,"
                    f" {dot} 0 20%, transparent 21%) !important;"
                    f" background-position: center !important;"
                    f" background-size: 100% 100% !important;"
                    f" background-repeat: no-repeat !important; }}"
                )
            else:
                # capturable piece -> a thin circular ring AROUND it (chess.com style)
                highlight += (
                    f".st-key-{tkey} > .stButton > button {{ position: relative !important; }}"
                    f".st-key-{tkey} > .stButton > button::after {{"
                    f" content:''; position:absolute; inset:7%;"
                    f" border:4px solid rgba(245,240,225,0.55); border-radius:50%;"
                    f" box-sizing:border-box; pointer-events:none; }}"
                )

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
        .block-container {{ padding: 0 !important; }}

        /* ---------- the 8x8 board grid, laid over the baked board ---------- */
        .st-key-board_grid {{
            position: fixed;
            left: 28.5%;    /* board left  */
            top: 18.5%;     /* board top   */
            width: 41.5%;   /* board width */
            z-index: 5;
        }}
        .st-key-board_grid [data-testid="stHorizontalBlock"] {{ gap: 0 !important; }}
        .st-key-board_grid [data-testid="stVerticalBlock"] {{ gap: 0 !important; }}
        .st-key-board_grid .stButton > button {{
            height: 7.1vh;
            padding: 0 !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}
        /* kill the gold focus/active border box on the clicked square */
        .st-key-board_grid .stButton > button:focus,
        .st-key-board_grid .stButton > button:focus-visible,
        .st-key-board_grid .stButton > button:active,
        .st-key-board_grid .stButton > button:hover {{
            border: none !important;
            outline: none !important;
        }}
        .st-key-board_grid .stButton > button p {{
            font-size: 7.5vh !important;
            line-height: 1 !important;
            margin: 0 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.45);
        }}
        [class*="st-key-sqw"] .stButton > button p {{
            color: {_WHITE_PIECE} !important; -webkit-text-fill-color: {_WHITE_PIECE} !important;
            -webkit-text-stroke: 1.4px #3a2a17;   /* dark outline on cream pieces */
            text-shadow: 0 2px 3px rgba(0,0,0,0.55);
            transform: translateY(-4px) !important;
        }}
        [class*="st-key-sqb"] .stButton > button p {{
            color: {_BLACK_PIECE} !important; -webkit-text-fill-color: {_BLACK_PIECE} !important;
            -webkit-text-stroke: 1.4px #7a5a30;      /* warm edge on dark pieces */
            text-shadow: 0 2px 3px rgba(0,0,0,0.4);
        }}
        {highlight}

        /* ---------- gold text overlays ---------- */
        .g-gold {{
            position: fixed;
            font-family: Georgia, "Times New Roman", serif;
            font-weight: 700;
            color: #ecd58a;
            text-shadow: 0 2px 3px rgba(0,0,0,0.7);
            z-index: 6;
            text-align: center;
        }}
        .g-turn    {{ left: 50%;  top: 2.45%;  transform: translateX(-50%); font-size: 2.0vw; }}
        .g-turnsub {{ left: 50%;  top: 7.45%;  transform: translateX(-50%); font-size: 1.1vw; color:#c9b06a; }}
        .g-modeinfo{{ left: 86.5%; top: 7%;   transform: translateX(-50%); font-size: 1.1vw; }}
        .g-oppname {{ left: 13%;  top: 27.5%;   transform: translateX(-50%); font-size: 1.2vw; letter-spacing: 2px; }}
        .g-opptime {{ left: 13%;  top: 30.5%; transform: translateX(-50%); font-size: 1.2vw; letter-spacing: 2px; }}
        .g-oppcap  {{ left: 13%;  top: 44%;   transform: translateX(-50%); font-size: 1.3vw; width: 15%; white-space: nowrap; overflow: hidden; color:#d8c8a0; }}
        .g-youname {{ left: 13%;  top: 73.5%;   transform: translateX(-50%); font-size: 1.2vw; letter-spacing: 2px; }}
        .g-youtime {{ left: 13%;  top: 76.5%; transform: translateX(-50%); font-size: 1.2vw; letter-spacing: 2px; }}
        .g-youcap  {{ left: 13%;  top: 88.5%;   transform: translateX(-50%); font-size: 1.3vw; width: 15%; white-space: nowrap; overflow: hidden; color:#d8c8a0; }}
        .g-moves-title {{ position: fixed; left: 76.5%; top: 11.5%; width: 16.5%; text-align: center;
                       font-weight: 600; color: #ecd58a; font-size: 1.2vw; letter-spacing: 2px;
                       text-shadow: 0 2px 3px rgba(0,0,0,0.7); padding-bottom: 8px;
                       border-bottom: 2px solid #c9a24b; z-index: 6; }}
        .g-moves   {{ left: 77.5%;  top: 19.5%;   width: 17%; height: 55%; overflow-y: auto;
                       font-size: 1.0vw; color:#d8c8a0; text-shadow:none; text-align:left; line-height:1.7; }}

        /* ---------- Restart / End Game buttons ---------- */
        .st-key-btn_restart, .st-key-btn_end {{
            position: fixed; left: 86%; transform: translateX(-50%); width: 12vw; z-index: 6;
        }}
        .st-key-btn_restart {{ top: 81.5%; }}
        .st-key-btn_end     {{ top: 90.5%; }}
        .st-key-btn_restart .stButton > button, .st-key-btn_end .stButton > button {{
            background: transparent !important; border: none !important; box-shadow: none !important;
        }}
        .st-key-btn_restart .stButton > button p, .st-key-btn_end .stButton > button p {{
            font-size: 1.2vw !important; letter-spacing: 2px !important; color:#ecd58a !important;
            -webkit-text-fill-color:#ecd58a !important; text-transform: uppercase !important;
            text-shadow: 0 2px 3px rgba(0,0,0,0.7) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# board grid
# =====================================================================
def _render_board(manager: GameManager) -> None:
    board = manager.get_board()
    clicked = None
    with st.container(key="board_grid"):
        for rank in range(7, -1, -1):
            cols = st.columns(8, gap="small")
            for file_index in range(8):
                square = chess.square(file_index, rank)
                piece = board.piece_at(square)
                glyph = _SOLID_GLYPH[piece.piece_type] if piece else " "
                key = _square_key(board, square)
                if cols[file_index].button(glyph, key=key, use_container_width=True):
                    clicked = square

    if clicked is not None:
        _handle_click(manager, clicked, st.session_state.get("language", "en"))
        st.rerun()


# (the pawn-promotion popup now is in modules/ui/promotion.py)


# =====================================================================
# PUBLIC ENTRY POINT — app.py calls render(manager)
# =====================================================================
def render(manager: GameManager) -> None:
    language = st.session_state.get("language", "en")
    _ensure_game_started(manager)
    _sync_timer()

    board = manager.get_board()
    _inject_style(board)

    mode = _mode_from_session()
    turn_white = board.turn == chess.WHITE
    opp_cap, you_cap = _captured(board)

    # names (bot vs friend)
    if mode == GameMode.BOT:
        opp_name, you_name = t("play_with_bot", language), t("game_you", language)
    else:
        opp_name, you_name = t("color_black", language), t("color_white", language)

    # ---- turn indicator ----
    turn_word = t("label_turn", language)
    turn_sub = t("white_to_move", language) if turn_white else t("black_to_move", language)
    st.markdown(f"<div class='g-gold g-turn'>{turn_word}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-gold g-turnsub'>{turn_sub}</div>", unsafe_allow_html=True)

    # ---- mode / difficulty (top-right) ----

    # ---- player panels (names + captured; clocks are drawn by _render_clocks) ----
    st.markdown(f"<div class='g-gold g-oppname'>{opp_name}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-gold g-oppcap'>{opp_cap}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-gold g-youname'>{you_name}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-gold g-youcap'>{you_cap}</div>", unsafe_allow_html=True)

    # ---- the two clocks (tick live once a second) ----
    _render_clocks()

    # ---- move history (right panel) ----
    history = manager.get_move_history()
    rows = ""
    for i in range(0, len(history), 2):
        num = i // 2 + 1
        white_mv = history[i]
        black_mv = history[i + 1] if i + 1 < len(history) else ""
        rows += f"{num}. {white_mv} &nbsp; {black_mv}<br>"
    st.markdown(
        f"<div class='g-moves-title'>{t('subheader_move_history', language)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='g-gold g-moves'>{rows}</div>", unsafe_allow_html=True)

    # ---- the board ----
    _render_board(manager)

    # ---- check flash ----
    if manager.is_check() and not board.is_game_over():
        st.toast(t("warning_check", language))

    # ---- Restart / End Game ----
    if st.button(t("game_restart", language), key="btn_restart"):
        _prepare_new_game(manager)
        st.rerun()
    if st.button(t("game_end", language), key="btn_end"):
        _prepare_new_game(manager)
        st.session_state.screen = "home"
        st.rerun()

    # ---- promotion popup — opens while a pawn promotion is pending ----
    if st.session_state.get("pending_promotion_from") is not None:
        promotion.open_dialog(manager)

    # ---- result popup — opens on checkmate OR when a clock runs out ----
    elif manager.is_game_over() or st.session_state.get("result_reason"):
        result.open_dialog(manager)
