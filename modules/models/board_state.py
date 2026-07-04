from dataclasses import dataclass

from modules.shared.enums.player_color import PlayerColor


@dataclass(slots=True)
class BoardState:
    """
    Represents the current state of the chess board.

    This model contains only board-related information and is
    independent from game flow or user interface logic.
    """

    fen: str
    turn: PlayerColor
    move_count: int
    fullmove_number: int

    