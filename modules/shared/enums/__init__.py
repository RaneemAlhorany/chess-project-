
from .difficulty import Difficulty
from .game_mode import GameMode
from .game_status import GameStatus
from .player_color import PlayerColor
from modules.shared.enums.game_end_reason import GameEndReason



"""
Represents the current lifecycle state of a chess game.

This enum tracks the overall state of the match and should not
be confused with chess conditions such as check or checkmate,
which are handled by the Chess Engine.
"""

