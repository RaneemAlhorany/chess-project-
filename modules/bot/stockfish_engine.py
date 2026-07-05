import logging
import random

from typing import Optional, Any

import chess
from stockfish import Stockfish as StockfishLib

from modules.shared.enums.difficulty import Difficulty
from modules.shared.constants.stockfish_constants import (
    STOCKFISH_PATH,
    DIFFICULTY_TO_DEPTH,
)

logger = logging.getLogger(__name__)


class StockfishEngine:
    """
    Handles all communication with the Stockfish chess engine.

    This class is responsible for initializing the Stockfish engine,
    configuring its difficulty level, evaluating board positions,
    and generating the best move for the current game state.

    It acts as a wrapper around the external Stockfish library,
    ensuring that the rest of the project remains independent
    from the underlying engine implementation.

    This class does not manage chess rules, board state,
    game flow, timers, sessions, or the user interface.
    Those responsibilities belong to other modules.
    """

#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self):
        """
        Initialize the Stockfish engine wrapper.

        Creates the internal engine state, sets the default
        difficulty level, and attempts to initialize the
        Stockfish engine.

        If the engine cannot be initialized, the instance
        remains usable, but engine-dependent operations
        will be unavailable.
        """

        #! Active Stockfish engine instance.
        self._engine: Optional[StockfishLib] = None

        #! Current bot difficulty level.
        self._difficulty: Difficulty = Difficulty.EASY

        #! Indicates whether the engine initialized successfully.
        self._available: bool = False

        #! Attempt to initialize the Stockfish engine.
        self._init_engine()

#% ==================================================
#! Engine Initialization
#% ==================================================

    def _init_engine(self) -> None:
        """
        Initialize the Stockfish engine.

        Creates the internal Stockfish engine instance using the
        configured executable path.

        The current difficulty level is then applied to the engine.

        If initialization fails, the engine is marked as unavailable,
        allowing the rest of the application to continue running
        safely without crashing.
        """

        if not STOCKFISH_PATH.exists() or STOCKFISH_PATH.stat().st_size == 0:
            self._engine = None
            self._available = False
            return

        try:
            self._engine = StockfishLib(
                path=str(STOCKFISH_PATH)
            )

            self._engine.set_depth(
                DIFFICULTY_TO_DEPTH[self._difficulty]
            )

            self._available = True

        except Exception as error:
            logger.warning(
                "Failed to initialize Stockfish: %s",
                error,
            )

            self._engine = None
            self._available = False



#% ==================================================
#! Engine Configuration
#% ==================================================

    def set_difficulty(self, difficulty: Difficulty) -> None:
        """
        Set the bot difficulty level.

        Updates the current difficulty setting and applies the
        corresponding search depth to the Stockfish engine if
        it has been successfully initialized.

        Args:
            difficulty: The desired difficulty level.
        """

        self._difficulty = difficulty

        if not self._available or self._engine is None:
            return

        try:
            self._engine.set_depth(
                DIFFICULTY_TO_DEPTH[self._difficulty]
            )

        except Exception as error:
            logger.warning(
                "Failed to update Stockfish difficulty: %s",
                error,
            )


#% ==================================================
#! Position Management
#% ==================================================

    def set_fen(self, fen: str) -> None:
        """
        Set the current board position for the Stockfish engine.

        Updates the engine with the provided board position
        represented as a Forsyth-Edwards Notation (FEN) string.

        Args:
            fen: The board position in FEN notation.
        """

        if not self._available or self._engine is None:
            return

        try:
            self._engine.set_fen_position(fen)

        except Exception as error:
            logger.warning(
                "Failed to update Stockfish position: %s",
                error,
            )

#% ==================================================
#! Move Generation
#% ==================================================

    def get_best_move(self, fen: str) -> Optional[str]:
        """
        Return the best move for the given board position.

        Updates the Stockfish engine with the supplied FEN position
        and calculates the strongest move based on the current
        difficulty level.

        Args:
            fen: The board position in FEN notation.

        Returns:
            The best move in UCI notation if available;
            otherwise None.
        """

        if not self._available or self._engine is None:
            return self._get_fallback_best_move(fen)

        try:
            self.set_fen(fen)
            return self._engine.get_best_move()

        except Exception as error:
            logger.warning(
                "Failed to generate best move: %s",
                error,
            )

            return None


    def _get_fallback_best_move(self, fen: str) -> Optional[str]:
        board = chess.Board(fen)
        legal_moves = list(board.legal_moves)

        if not legal_moves:
            return None

        return random.choice(legal_moves).uci()


    def get_evaluation( self, fen: str, ) -> Optional[dict[str, Any]]:
        """
        Evaluate the given board position.

        Updates the Stockfish engine with the supplied FEN position
        and returns the engine evaluation.

        Args:
            fen: The board position in FEN notation.

        Returns:
            A dictionary containing the evaluation returned by
            Stockfish, or None if the evaluation could not be
            performed.
        """

        if not self._available or self._engine is None:
            return None

        try:
            self.set_fen(fen)
            return self._engine.get_evaluation()

        except Exception as error:
            logger.warning(
                "Failed to evaluate position: %s",
                error,
            )

            return None



#% ==================================================
#! Engine Status
#% ==================================================

    def is_available(self) -> bool:
        """
        Check whether the Stockfish engine is available.

        Returns:
            True if the engine was successfully initialized;
            otherwise False.
        """
        return self._available


    def get_difficulty(self) -> Difficulty:
        """
        Return the current bot difficulty level.

        Returns:
            The currently configured difficulty.
        """
        return self._difficulty


    def get_depth(self) -> int:
        """
        Return the current Stockfish search depth.

        Returns:
            The search depth associated with the
            current difficulty level.
        """

        return DIFFICULTY_TO_DEPTH[self._difficulty]



#% ==================================================
#! Engine Management
#% ==================================================

    def reset(self) -> None:
        """
        Reset the Stockfish engine to the initial position.

        Clears the current board position inside the engine and
        restores the standard chess starting position.

        If the engine is unavailable, this method does nothing.
        """

        if not self._available or self._engine is None:
            return

        try:
            self._engine.set_position()

        except Exception as error:
            logger.warning(
                "Failed to reset Stockfish engine: %s",
                error,
            )       



