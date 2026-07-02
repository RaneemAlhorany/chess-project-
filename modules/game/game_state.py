from dataclasses import dataclass
from typing import Optional

from modules.shared.enums.difficulty import Difficulty
from modules.shared.enums.game_mode import GameMode
from modules.shared.enums.game_status import GameStatus
from modules.shared.enums.player_color import PlayerColor


@dataclass
class GameState:
    """
    Represents the current state of a chess game.

    This class stores all game-related data during a match.
    It does not contain game logic.
    """

    game_mode: GameMode
    status: GameStatus
    current_turn_color: PlayerColor
    difficulty: Optional[Difficulty] = None
    winner: Optional[PlayerColor] = None