# Standard Library
from typing import Optional
from typing import List

# Project Modules
from modules.chess_engine.ChessEngine import ChessEngine
from modules.game.game_state import GameState
from modules.session.session_manager import SessionManager

# Shared Enums
from modules.shared.enums.difficulty import Difficulty
from modules.shared.enums.game_mode import GameMode
from modules.shared.enums.game_status import GameStatus
from modules.shared.enums.player_color import PlayerColor
from modules.shared.enums.game_end_reason import GameEndReason

# Project Engines
from modules.stockfish.stockfish_engine import StockfishEngine

# Project Models
from modules.models.board_state import BoardState

# Shared Constants
from modules.shared.constants.session_constants import (
    GAME_STATE_SESSION_KEY,
)


# Third-Party Libraries
import chess



class GameManager:
    """
    Central controller of the chess application.

    Responsibilities:
    - Manage GameState lifecycle
    - Coordinate ChessEngine
    - Persist state via SessionManager
    """

#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self) -> None:
        """
        Initialize the GameManager.

        Creates all core components required to manage a chess match,
        including the chess engine, AI engine, and session manager.

        No game is started during initialization.
        A GameState instance is created only when
        start_game() is called.
        """

        #! Chess logic controller.
        self._engine = ChessEngine()

        #! AI engine used for bot-controlled games.
        self._bot = StockfishEngine()

        #! Session persistence manager.
        self._session = SessionManager()

        #! Active game state.
        self._game_state: Optional[GameState] = None


#% ==================================================
#! Game Lifecycle
#% ==================================================

    def start_game(self,game_mode: GameMode,
        difficulty: Optional[Difficulty] = None,) -> None:
        """
        Start a new chess game.

        Resets the chess engine, initializes the game state,
        configures the AI engine if playing against the bot,
        and synchronizes the new game with the session.

        Args:
            game_mode: The selected game mode.
            difficulty: The bot difficulty level for BOT games.
        """

        self._engine.reset()

        self._bot.reset()

        if game_mode == GameMode.BOT:
            difficulty = difficulty or Difficulty.EASY
            self._bot.set_difficulty(difficulty)

        self._game_state = GameState(
            game_mode=game_mode,
            status=GameStatus.RUNNING,
            difficulty=difficulty,
        )

        self._sync_session()


    def restart_game(self) -> None:
        """
        Restart the current game.

        Starts a new match using the same game mode and
        difficulty level as the current game.

        If no active game exists, this method does nothing.
        """

        if self._game_state is None:
            return

        self.start_game(
            game_mode=self._game_state.game_mode,
            difficulty=self._game_state.difficulty,
        )


    def end_game(self,
        winner: Optional[PlayerColor] = None,) -> None:
        """
        End the current chess game.

        Marks the active game as finished, records the
        winning player if applicable, and synchronizes
        the updated game state with the current session.

        Args:
            winner: The winning player, or None if the game
                ended in a draw or was terminated manually.
        """

        if self._game_state is None:
            return

        self._game_state.status = GameStatus.FINISHED
        self._game_state.winner = winner

        self._sync_session()


#% ==================================================
#! Gameplay
#% ==================================================

    def make_move(self,from_square: int,to_square: int,
        promotion: Optional[int] = None,) -> bool:
        """
        Execute a player's move.

        Applies the requested move using the chess engine,
        updates the game status, triggers the AI move when
        appropriate, and synchronizes the current game state.

        Args:
            from_square: Source square index.
            to_square: Destination square index.
            promotion: Optional promotion piece type.

        Returns:
            True if the move was successfully executed;
            otherwise False.
        """

        if self._engine.make_move(
            from_square,
            to_square,
            promotion,
        ) is None:
            return False

        self._update_game_status()

        if self._should_make_bot_move():
            if not self._make_bot_move():
                return False

        self._sync_session()

        return True



    def undo_last_move(self) -> bool:
        """
        Undo the most recently executed move.

        Reverts the latest move played on the chessboard.
        When playing against the AI, the player's previous
        move is also undone so the game returns to the
        player's turn.

        Updates the game status and synchronizes the current
        game state with the active session.

        Returns:
            True if the undo operation was successful;
            otherwise False.
        """

        if self._engine.undo_last_move() is None:
            return False

        if self._should_undo_player_move():
            if self._engine.undo_last_move() is None:
                return False

        self._update_game_status()

        self._sync_session()

        return True
    

#% ==================================================
#! Bot Management
#% ==================================================

    def _should_make_bot_move(self) -> bool:
        """
        Determine whether the AI should make a move.

        The AI is allowed to move only when:
        - A game is currently active.
        - The game mode is BOT.
        - The game is still running.

        Returns:
            True if the AI should make a move;
            otherwise False.
        """

        if self._game_state is None:
            return False

        return (
            self._game_state.game_mode == GameMode.BOT
            and self._game_state.status == GameStatus.RUNNING
        )


    def _make_bot_move(self) -> bool:
        """
        Generate and execute the AI player's move.

        Retrieves the current board position from the chess engine,
        requests the best move from the AI engine, and delegates
        its execution to the internal move application helper.

        Returns:
            True if the AI move was successfully executed;
            otherwise False.
        """

        fen = self._engine.get_fen()

        uci_move = self._bot.get_best_move(fen)

        if uci_move is None:
            return False

        return self._apply_bot_move(uci_move)


    def _apply_bot_move(self,uci_move: str,) -> bool:
        """
        Execute an AI move on the chessboard.

        Converts the supplied UCI move into the corresponding
        board coordinates and executes it using the chess engine.

        Updates the game status after a successful move.

        Args:
            uci_move: The AI move in UCI notation.

        Returns:
            True if the move was successfully executed;
            otherwise False.
        """

        from_square = self._engine.uci_to_from_square(uci_move)

        to_square = self._engine.uci_to_to_square(uci_move)

        promotion = self._engine.uci_get_promotion(uci_move)

        move = self._engine.make_move(
            from_square,
            to_square,
            promotion,
        )

        if move is None:
            return False

        self._update_game_status()

        return True
        

    def _should_undo_player_move(self) -> bool:
        """
        Determine whether the player's move should also be undone.

        This helper is used after undoing the bot's move during
        a bot game. If the game still contains a previous player
        move, it should also be reverted so the board returns
        to the player's previous turn.

        Returns:
            True if the player's move should also be undone;
            otherwise False.
        """

        if self._game_state is None:
            return False

        if self._game_state.game_mode != GameMode.BOT:
            return False

        return self._engine.get_move_count() > 0


#% ==================================================
#! Gameplay Helpers
#% ==================================================

    def _undo_engine_move(self) -> bool:
        """
        Undo the most recent move executed by the chess engine.

        Returns:
            True if a move was successfully undone;
            otherwise False.
        """

        return self._engine.undo_last_move() is not None


#% ==================================================
#! Game Status
#% ==================================================

    def _update_game_status(self) -> None:
        """
        Synchronize the current game status with the chess engine.

        Updates the active GameState based on the current state
        of the ChessEngine, including the game status, winner,
        and end reason.

        If the game is still in progress, any previously stored
        end-of-game information is cleared.
        """

        if self._game_state is None:
            return

        if not self._engine.is_game_over():
            self._game_state.status = GameStatus.RUNNING
            self._game_state.winner = None
            self._game_state.end_reason = None
            return

        self._game_state.status = GameStatus.FINISHED
        self._game_state.end_reason = self._engine.outcome_reason()

        result = self._engine.result()

        if result == "1-0":
            self._game_state.winner = PlayerColor.WHITE

        elif result == "0-1":
            self._game_state.winner = PlayerColor.BLACK

        else:
            self._game_state.winner = None

#% ==================================================
#! Session Handling
#% ==================================================

    def _sync_session(self) -> None:
        """
        Synchronize the current game state with the active session.

        Persists the latest GameState instance using the
        SessionManager, ensuring that the current match
        can be restored later if needed.
        """

        self._session.set(
            GAME_STATE_SESSION_KEY,
            self._game_state,
        )

#! TODO:
#~ Revisit this method after completing SessionManager.
#~ Verify that loading a session fully restores the chess board,
#~ GameState, and all runtime information.
    def load_game(self) -> Optional[GameState]:
        """
        Load the most recently saved game session.

        Retrieves the stored GameState from the SessionManager,
        updates the active game state, and returns the loaded
        game if one exists.

        Returns:
            The restored GameState instance if a saved game
            exists; otherwise None.
        """

        self._game_state = self._session.get(
            GAME_STATE_SESSION_KEY,
        )

        return self._game_state


#% ==================================================
#! Engine Facade
#% ==================================================

    def get_board(self) -> chess.Board:
        """
        Return the active chess board.

        Provides access to the underlying chess.Board
        instance managed by the ChessEngine.

        Returns:
            The active chess board.
        """

        return self._engine.get_board()


    def get_board_state(self) -> BoardState:
        """
        Return the current board state.

        Provides a snapshot of the current chess position,
        including the board representation and additional
        game metadata.

        Returns:
            The current BoardState instance.
        """

        return self._engine.get_board_state()


    def get_turn(self) -> PlayerColor:
        """
        Return the color of the player whose turn it is.

        Delegates the request to the ChessEngine and returns
        the player currently allowed to make a move.

        Returns:
            The current player's color.
        """

        return self._engine.get_turn_color()


    def get_move_history(self) -> List[str]:
        """
        Return the complete move history.

        Delegates the request to the ChessEngine and returns
        the game's move history in Standard Algebraic Notation (SAN).

        Returns:
            A list containing all executed moves in SAN notation.
        """

        return self._engine.get_san_history()


    def get_result(self) -> str:
        """
        Return the official result of the current game.

        Delegates the request to the ChessEngine and returns
        the game's result using the standard chess notation.

        Returns:
            The game result in standard notation:
            "1-0" for a White win,
            "0-1" for a Black win,
            "1/2-1/2" for a draw,
            or "*" if the game is still in progress.
        """

        return self._engine.result()


    def get_game_end_reason(self) -> Optional[GameEndReason]:
        """
        Return the reason why the game ended.

        Delegates the request to the ChessEngine and returns
        the reason that caused the game to finish.

        Returns:
            The GameEndReason if the game has ended;
            otherwise None.
        """

        return self._engine.outcome_reason()


    def is_game_over(self) -> bool:
        """
        Check whether the current game has ended.

        Delegates the request to the ChessEngine.

        Returns:
            True if the game is over; otherwise False.
        """

        return self._engine.is_game_over()


    def is_check(self) -> bool:
        """
        Check whether the current player is in check.

        Delegates the request to the ChessEngine.

        Returns:
            True if the current player's king is in check;
            otherwise False.
        """

        return self._engine.is_check()


    def is_checkmate(self) -> bool:
        """
        Check whether the current game has ended by checkmate.

        Delegates the request to the ChessEngine.

        Returns:
            True if the game ended by checkmate;
            otherwise False.
        """

        return self._engine.is_checkmate()


    def is_stalemate(self) -> bool:
        """
        Check whether the current game has ended by stalemate.

        Delegates the request to the ChessEngine.

        Returns:
            True if the game ended by stalemate;
            otherwise False.
        """

        return self._engine.is_stalemate()


    def is_draw(self) -> bool:
        """
        Check whether the current game ended in a draw.

        Delegates the request to the ChessEngine.

        Returns:
            True if the game ended in a draw;
            otherwise False.
        """

        return self._engine.is_draw()

#% ==================================================
#! Getters
#% ==================================================

    def get_game_state(self) -> Optional[GameState]:
        """
        Return the active game state.

        Provides access to the current GameState instance
        managed by the GameManager.

        Returns:
            The active GameState if a game exists;
            otherwise None.
        """

        return self._game_state

#! TODO:
## Review whether exposing the internal ChessEngine is necessary.
## If all required operations are available through GameManager,
## this getter should be removed to preserve encapsulation.
    def get_engine(self) -> ChessEngine:
        """
        Return the internal chess engine.

        Returns:
            The ChessEngine instance currently managed by
            the GameManager.
        """

        return self._engine
        