import streamlit as st

from modules.game.game_manager import GameManager
from modules.shared.enums.difficulty import Difficulty
from modules.shared.enums.game_mode import GameMode
from modules.shared.helpers.display import format_label
from modules.shared.constants.ui_constants import (
    BOARD_FEN_LANGUAGE,
    DEFAULT_EMPTY_GAME_MESSAGE,
    DEFAULT_EMPTY_HISTORY_MESSAGE,
    DEFAULT_COLUMN_RATIOS,
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
)
from translations.strings import (
    APP_CAPTION,
    APP_TITLE,
    BUTTON_LOAD_SAVED_GAME,
    BUTTON_RESTART_GAME,
    BUTTON_START_GAME,
    BUTTON_UNDO_LAST_MOVE,
    CAPTION_NO_MOVES,
    INFO_NO_ACTIVE_GAME,
    LABEL_DIFFICULTY,
    LABEL_END_REASON,
    LABEL_GAME_MODE,
    LABEL_MODE,
    LABEL_MOVE_COUNT,
    LABEL_STATUS,
    LABEL_TURN,
    LABEL_WINNER,
    SIDEBAR_NEW_GAME,
    SUBHEADER_BOARD,
    SUBHEADER_GAME_STATE,
    SUBHEADER_MOVE_HISTORY,
)


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)


def get_manager() -> GameManager:
    if "game_manager" not in st.session_state:
        st.session_state.game_manager = GameManager()
    return st.session_state.game_manager


manager = get_manager()

st.title(APP_TITLE)
st.caption(APP_CAPTION)

with st.sidebar:
    st.header(SIDEBAR_NEW_GAME)
    game_mode = st.selectbox(LABEL_MODE, [GameMode.FRIEND, GameMode.BOT], format_func=format_label)
    difficulty = st.selectbox(LABEL_DIFFICULTY, [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD], format_func=format_label)

    if st.button(BUTTON_START_GAME):
        manager.start_game(game_mode=game_mode, difficulty=difficulty if game_mode == GameMode.BOT else None)
        st.rerun()

    if st.button(BUTTON_LOAD_SAVED_GAME):
        manager.load_game()
        st.rerun()

    if st.button(BUTTON_RESTART_GAME):
        manager.restart_game()
        st.rerun()

    if st.button(BUTTON_UNDO_LAST_MOVE):
        manager.undo_last_move()
        st.rerun()


game_state = manager.get_game_state()

if game_state is None:
    st.info(INFO_NO_ACTIVE_GAME)
else:
    board_state = manager.get_board_state()

    left, right = st.columns(DEFAULT_COLUMN_RATIOS)
    with left:
        st.subheader(SUBHEADER_GAME_STATE)
        st.write(f"{LABEL_GAME_MODE}: {format_label(game_state.game_mode)}")
        st.write(f"{LABEL_STATUS}: {format_label(game_state.status)}")
        st.write(f"{LABEL_TURN}: {format_label(board_state.turn)}")
        st.write(f"{LABEL_MOVE_COUNT}: {board_state.move_count}")
        if game_state.difficulty is not None:
            st.write(f"{LABEL_DIFFICULTY}: {format_label(game_state.difficulty)}")
        if game_state.winner is not None:
            st.write(f"{LABEL_WINNER}: {format_label(game_state.winner)}")
        if game_state.end_reason is not None:
            st.write(f"{LABEL_END_REASON}: {format_label(game_state.end_reason)}")

    with right:
        st.subheader(SUBHEADER_BOARD)
        st.code(board_state.fen, language=BOARD_FEN_LANGUAGE)

    st.subheader(SUBHEADER_MOVE_HISTORY)
    history = manager.get_move_history()
    if history:
        st.write(history)
    else:
        st.caption(CAPTION_NO_MOVES)
