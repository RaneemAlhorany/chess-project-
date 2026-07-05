"""
Shared chess board constants.

These values centralize board dimensions and default chess
notation details used across the application.
"""

from __future__ import annotations

import chess


BOARD_FILES_COUNT = 8
BOARD_RANKS_COUNT = 8
BOARD_SQUARE_COUNT = 64

FILE_NAMES = tuple("abcdefgh")
RANK_NAMES = tuple("12345678")

STARTING_FEN = chess.STARTING_FEN

PROMOTION_PIECES = (
	chess.QUEEN,
	chess.ROOK,
	chess.BISHOP,
	chess.KNIGHT,
)
