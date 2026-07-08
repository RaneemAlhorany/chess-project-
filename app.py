import streamlit as st

from modules.game.game_manager import GameManager
from modules.shared.constants.ui_constants import PAGE_ICON, PAGE_LAYOUT, PAGE_TITLE
from modules.shared.enums.difficulty import Difficulty
from modules.shared.enums.game_mode import GameMode
from modules.ui import difficulty as difficulty_ui
from modules.ui import game as game_ui
from modules.ui import home, mode_select


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)


def get_manager() -> GameManager:
    if "game_manager" not in st.session_state:
        st.session_state.game_manager = GameManager()
        # Reuse a preloaded Stockfish engine if available to avoid reinitialization.
        if "preloaded_bot" in st.session_state:
            try:
                st.session_state.game_manager._bot = st.session_state.preloaded_bot
            except Exception:
                pass
    return st.session_state.game_manager


def _init_session_defaults() -> None:
    if "screen" not in st.session_state:
        st.session_state.screen = "home"

    if "language" not in st.session_state:
        st.session_state.language = "en"

    if "mode" not in st.session_state:
        st.session_state.mode = GameMode.FRIEND.value

    if "difficulty" not in st.session_state:
        st.session_state.difficulty = Difficulty.MEDIUM.value


def main() -> None:
    _init_session_defaults()
    screen = st.session_state.get("screen", "home")

    if screen == "home":
        home.render()
        return

    if screen == "mode":
        mode_select.render()
        return

    if screen == "difficulty":
        mode_select.render()          # draw the mode scene behind the popup
        difficulty_ui.open_dialog()
        return

    if screen == "game":
        manager = get_manager()
        game_ui.render(manager)
        return

    st.session_state.screen = "home"
    st.rerun()


main()
