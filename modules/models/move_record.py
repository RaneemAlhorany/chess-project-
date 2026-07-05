from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class MoveRecord:
    """
    Represents a single move with full contextual metadata.

    This model captures not only the algebraic notation of a move
    but also the pieces involved, special move flags, and the
    resulting board status after the move was played.
    """

    move_number: int
    san: str
    from_square: int
    to_square: int
    piece_symbol: str
    captured_piece_symbol: Optional[str] = None
    is_check: bool = False
    is_checkmate: bool = False
    is_castling: bool = False
    is_en_passant: bool = False
    is_promotion: bool = False
    promotion_piece_symbol: Optional[str] = None
