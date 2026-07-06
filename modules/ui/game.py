import chess

from modules.game.game_manager import GameManager
from modules.shared.enums.game_mode import GameMode
from modules.shared.enums.game_status import GameStatus
from modules.shared.enums.difficulty import Difficulty
from modules.shared.helpers.display import format_label
from modules.shared.constants.ui_constants import (
    BOARD_FEN_LANGUAGE,
    DEFAULT_COLUMN_RATIOS,
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
)
from modules.ui import home, mode_select, difficulty as difficulty_ui
from translations.i18n import t



def _get_mode_from_session() -> GameMode:
    raw_mode = st.session_state.get("mode", GameMode.FRIEND.value)

    if raw_mode == GameMode.BOT.value:
        return GameMode.BOT

    return GameMode.FRIEND


def _get_difficulty_from_session() -> Difficulty:
    raw_difficulty = st.session_state.get("difficulty", Difficulty.MEDIUM.value)

    for difficulty in Difficulty:
        if difficulty.value == raw_difficulty:
            return difficulty

    return Difficulty.MEDIUM


def _ensure_game_started(manager: GameManager) -> None:
    mode = _get_mode_from_session()
    difficulty = _get_difficulty_from_session() if mode == GameMode.BOT else None

    game_state = manager.get_game_state()

    if game_state is None:
        manager.start_game(game_mode=mode, difficulty=difficulty)
        return

    if game_state.game_mode != mode:
        manager.start_game(game_mode=mode, difficulty=difficulty)
        return

    if mode == GameMode.BOT and game_state.difficulty != difficulty:
        manager.start_game(game_mode=mode, difficulty=difficulty)


def _piece_label_map(language: str) -> dict[str, int]:
    return {
        t("promotion_queen", language): chess.QUEEN,
        t("promotion_rook", language): chess.ROOK,
        t("promotion_bishop", language): chess.BISHOP,
        t("promotion_knight", language): chess.KNIGHT,
    }


def _clear_move_ui_state() -> None:
    st.session_state.pop("selected_from_square", None)
    st.session_state.pop("pending_promotion_from", None)
    st.session_state.pop("pending_promotion_to", None)


def _try_select_piece(square: int, board: chess.Board) -> None:
    legal_moves = list(board.legal_moves)
    has_legal_from_square = any(move.from_square == square for move in legal_moves)
    piece = board.piece_at(square)

    if piece is None:
        return

    if piece.color != board.turn:
        return

    if not has_legal_from_square:
        return

    st.session_state.selected_from_square = square


def _handle_board_click(manager: GameManager, clicked_square: int, language: str) -> None:
    board = manager.get_board()
    legal_moves = list(board.legal_moves)
    selected_from = st.session_state.get("selected_from_square")

    if selected_from is None:
        _try_select_piece(clicked_square, board)
        return

    if clicked_square == selected_from:
        st.session_state.selected_from_square = None
        return

    matching_moves = [
        move
        for move in legal_moves
        if move.from_square == selected_from and move.to_square == clicked_square
    ]

    if not matching_moves:
        _try_select_piece(clicked_square, board)
        if st.session_state.get("selected_from_square") == selected_from:
            st.session_state.selected_from_square = None
        return

    promotion_moves = [move for move in matching_moves if move.promotion is not None]
    if promotion_moves:
        st.session_state.pending_promotion_from = selected_from
        st.session_state.pending_promotion_to = clicked_square
        st.session_state.selected_from_square = None
        return

    moved = manager.make_move(
        selected_from,
        clicked_square,
        None,
    )

    st.session_state.selected_from_square = None

    if not moved:
        st.error(t("error_illegal_move", language))
        return

    st.rerun()


def _render_promotion_selector(manager: GameManager, language: str) -> None:
    from_square = st.session_state.get("pending_promotion_from")
    to_square = st.session_state.get("pending_promotion_to")

    if from_square is None or to_square is None:
        return

    piece_map = _piece_label_map(language)
    st.subheader(t("subheader_promotion", language))
    promotion_label = st.selectbox(
        t("move_promotion", language),
        options=list(piece_map.keys()),
        key="promotion_piece",
    )

    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button(t("button_confirm_promotion", language), key="confirm_promotion"):
            moved = manager.make_move(
                from_square,
                to_square,
                piece_map[promotion_label],
            )

            _clear_move_ui_state()

            if not moved:
                st.error(t("error_illegal_move", language))
                return

            st.rerun()

    with col_cancel:
        if st.button(t("button_cancel", language), key="cancel_promotion"):
            _clear_move_ui_state()
            st.rerun()


def _render_clickable_board(manager: GameManager, language: str) -> None:
    board = manager.get_board()
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        st.info(t("info_no_legal_moves", language))
        return

    st.caption(t("board_click_hint", language))

    selected_from = st.session_state.get("selected_from_square")
    legal_targets = {
        move.to_square
        for move in legal_moves
        if move.from_square == selected_from
    }

    if selected_from is not None:
        st.caption(f"{t('board_selected_from', language)}: {chess.square_name(selected_from)}")

    clicked_square = None
    for rank in range(7, -1, -1):
        columns = st.columns(8)
        for file_index in range(8):
            square = chess.square(file_index, rank)
            piece = board.piece_at(square)
            label = piece.unicode_symbol() if piece else "·"

            if square == selected_from:
                label = f"[{label}]"
            elif square in legal_targets:
                label = f"*{label}"

            if columns[file_index].button(label, key=f"board_square_{square}"):
                clicked_square = square

    if clicked_square is not None:
        _handle_board_click(manager, clicked_square, language)
        st.rerun()

    _render_promotion_selector(manager, language)


def _render_game_screen(manager: GameManager) -> None:
    language = st.session_state.get("language", "en")
    _ensure_game_started(manager)

    game_state = manager.get_game_state()

    with st.sidebar:
        st.header(t("sidebar_new_game", language))

        if st.button(t("button_start_game", language)):
            mode = _get_mode_from_session()
            difficulty = _get_difficulty_from_session() if mode == GameMode.BOT else None
            manager.start_game(game_mode=mode, difficulty=difficulty)
            _clear_move_ui_state()
            st.rerun()

        if st.button(t("button_load_saved_game", language)):
            manager.load_game()
            _clear_move_ui_state()
            st.rerun()

        if st.button(t("button_restart_game", language)):
            manager.restart_game()
            _clear_move_ui_state()
            st.rerun()

        if st.button(t("button_undo_last_move", language)):
            manager.undo_last_move()
            _clear_move_ui_state()
            st.rerun()

        if st.button(t("button_back_home", language)):
            _clear_move_ui_state()
            st.session_state.screen = "home"
            st.rerun()

    if game_state is None:
        st.info(t("info_no_active_game", language))
        return

    board_state = manager.get_board_state()

    left, right = st.columns(DEFAULT_COLUMN_RATIOS)
    with left:
        st.subheader(t("subheader_game_state", language))
        st.write(f"{t('label_game_mode', language)}: {format_label(game_state.game_mode)}")
        st.write(f"{t('label_status', language)}: {format_label(game_state.status)}")
        st.write(f"{t('label_turn', language)}: {format_label(board_state.turn)}")
        st.write(f"{t('label_move_count', language)}: {board_state.move_count}")

        if game_state.difficulty is not None:
            st.write(f"{t('label_difficulty', language)}: {format_label(game_state.difficulty)}")

        if game_state.winner is not None:
            st.write(f"{t('label_winner', language)}: {format_label(game_state.winner)}")

        if game_state.end_reason is not None:
            st.write(f"{t('label_end_reason', language)}: {format_label(game_state.end_reason)}")

        if game_state.status == GameStatus.RUNNING and manager.is_check():
            st.warning(t("warning_check", language))

    with right:
        st.subheader(t("subheader_board", language))
        _render_clickable_board(manager, language)
        st.caption(t("board_fen", language))
        st.code(board_state.fen, language=BOARD_FEN_LANGUAGE)

    st.subheader(t("subheader_move_history", language))
    history = manager.get_move_history()
    if history:
        st.write(history)
    else:
        st.caption(t("caption_no_moves", language))
