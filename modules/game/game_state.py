from dataclasses import dataclass
from typing import Optional

from modules.shared.enums.difficulty import Difficulty
from modules.shared.enums.game_mode import GameMode
from modules.shared.enums.game_status import GameStatus
from modules.shared.enums.player_color import PlayerColor
from modules.shared.enums.game_end_reason import GameEndReason
from modules.models.board_state import BoardState



@dataclass
class GameState:
    """
    Represents the current state of a chess game.

    This class stores general match information.
    Chess-specific information such as the board state,
    current turn, move history, and game rules are managed
    by the ChessEngine.
    """

    game_mode: GameMode

    status: GameStatus

    difficulty: Optional[Difficulty] = None

    board_state: Optional[BoardState] = None

    winner: Optional[PlayerColor] = None

    end_reason: Optional[GameEndReason] = None