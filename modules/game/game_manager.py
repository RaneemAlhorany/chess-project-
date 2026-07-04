
# "يدير دورة حياة المباراة."


#/*

# هذا أهم Class في المشروع كله.

# هو قائد اللعبة.

# لا يعرف تفاصيل قوانين الشطرنج، لكنه يعرف كيف تُدار المباراة.

# مسؤولياته
# إنشاء مباراة جديدة.
# بدء المباراة.
# إعادة المباراة.
# إنهاء المباراة.
# معرفة اللاعب الحالي.
# التواصل مع ChessEngine.
# التواصل مع Session.
# التواصل مع Bot (إذا كان نمط اللعب ضد الحاسوب).

# أي أنه Coordinator وليس منفذًا لكل شيء.

# 

from typing import Optional

from modules.chess_engine.ChessEngine import ChessEngine
from modules.game.game_state import GameState
from modules.session.session_manager import SessionManager

from modules.shared.enums.difficulty import Difficulty
from modules.shared.enums.game_mode import GameMode
from modules.shared.enums.game_status import GameStatus
from modules.shared.enums.player_color import PlayerColor


class GameManager:
    """
    Central controller of the chess application.

    Responsibilities:
    - Manage GameState lifecycle
    - Coordinate ChessEngine
    - Persist state via SessionManager
    """

    def __init__(self) -> None:
        self._engine = ChessEngine()
        self._session = SessionManager()

        self._game_state: Optional[GameState] = None

    # ==================================================
    # Game Lifecycle
    # ==================================================

    def start_game(
        self,
        game_mode: GameMode,
        difficulty: Optional[Difficulty] = None,
    ) -> None:

        self._engine.reset()

        self._game_state = GameState(
            game_mode=game_mode,
            game_status=GameStatus.RUNNING,
            difficulty=difficulty,
        )

        self._sync_session()

    def restart_game(self) -> None:
        if not self._game_state:
            return

        self.start_game(
            game_mode=self._game_state.game_mode,
            difficulty=self._game_state.difficulty,
        )

    def end_game(
        self,
        winner: Optional[PlayerColor] = None,
    ) -> None:

        if not self._game_state:
            return

        self._game_state.game_status = GameStatus.FINISHED
        self._game_state.winner_color = winner

        self._sync_session()

    # ==================================================
    # Gameplay
    # ==================================================

    def make_move(
        self,
        from_square: int,
        to_square: int,
        promotion: Optional[int] = None,
    ) -> bool:

        move = self._engine.make_move(
            from_square,
            to_square,
            promotion,
        )

        if move is None:
            return False

        self._update_game_status()
        self._sync_session()

        return True

    def undo_last_move(self) -> bool:

        move = self._engine.undo_last_move()

        if move is None:
            return False

        self._update_game_status()
        self._sync_session()

        return True
    
        # ==================================================
    # Game Status Sync
    # ==================================================

    def _update_game_status(self) -> None:

        if not self._game_state:
            return

        if not self._engine.is_game_over():
            self._game_state.game_status = GameStatus.RUNNING
            self._game_state.winner_color = None
            return

        self._game_state.game_status = GameStatus.FINISHED

        result = self._engine.result()

        if result == "1-0":
            self._game_state.winner_color = PlayerColor.WHITE

        elif result == "0-1":
            self._game_state.winner_color = PlayerColor.BLACK

        else:
            self._game_state.winner_color = None

    # ==================================================
    # Session Handling
    # ==================================================

    def _sync_session(self) -> None:
        self._session.set("game_state", self._game_state)

    def load_game(self) -> Optional[GameState]:
        self._game_state = self._session.get("game_state")
        return self._game_state

    # ==================================================
    # Engine Facade
    # ==================================================

    def get_board(self):
        return self._engine.get_board()

    def get_board_state(self):
        return self._engine.get_board_state()

    def get_turn(self):
        return self._engine.get_turn_color()

    def get_move_history(self):
        return self._engine.get_san_history()

    def get_result(self):
        return self._engine.result()

    def get_game_end_reason(self):
        return self._engine.outcome_reason()

    def is_game_over(self) -> bool:
        return self._engine.is_game_over()

    def is_check(self) -> bool:
        return self._engine.is_check()

    def is_checkmate(self) -> bool:
        return self._engine.is_checkmate()

    def is_stalemate(self) -> bool:
        return self._engine.is_stalemate()

    def is_draw(self) -> bool:
        return self._engine.is_draw()

    # ==================================================
    # Getters
    # ==================================================

    def get_game_state(self) -> Optional[GameState]:
        return self._game_state

    def get_engine(self) -> ChessEngine:
        return self._engine