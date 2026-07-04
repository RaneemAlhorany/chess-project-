from enum import Enum


class GameEndReason(Enum):
    """
    Represents the possible reasons why a chess game ended.

    These values are independent from python-chess and include
    only the game-ending conditions supported by this project.
    """

    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    INSUFFICIENT_MATERIAL = "insufficient_material"
    FIFTY_MOVE_RULE = "fifty_move_rule"
    THREEFOLD_REPETITION = "threefold_repetition"
    UNKNOWN = "unknown"

    