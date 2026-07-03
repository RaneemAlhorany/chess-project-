from enum import Enum


class GameEndReason(Enum):
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    INSUFFICIENT_MATERIAL = "insufficient_material"
    FIFTY_MOVE_RULE = "fifty_move_rule"
    THREEFOLD_REPETITION = "threefold_repetition"
    VARIANT_WIN = "variant_win"
    VARIANT_LOSS = "variant_loss"
    UNKNOWN = "unknown"