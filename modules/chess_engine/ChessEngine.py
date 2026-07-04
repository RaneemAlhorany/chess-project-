import chess

from typing import Optional, List

from modules.shared.enums.player_color import PlayerColor

from modules.shared.enums.game_end_reason import GameEndReason

from modules.models.board_state import BoardState


#% ==================================================
#! Module Constants
#% ==================================================

_TERMINATION_TO_GAME_END_REASON = {
    chess.Termination.CHECKMATE: GameEndReason.CHECKMATE,
    chess.Termination.STALEMATE: GameEndReason.STALEMATE,
    chess.Termination.INSUFFICIENT_MATERIAL: GameEndReason.INSUFFICIENT_MATERIAL,
    chess.Termination.FIFTY_MOVES: GameEndReason.FIFTY_MOVE_RULE,
    chess.Termination.SEVENTYFIVE_MOVES: GameEndReason.FIFTY_MOVE_RULE,
    chess.Termination.THREEFOLD_REPETITION: GameEndReason.THREEFOLD_REPETITION,
    chess.Termination.FIVEFOLD_REPETITION: GameEndReason.THREEFOLD_REPETITION,
}


class ChessEngine:
    """
    Handles all chess board operations using the python-chess library.

    This class is responsible for managing the chess board,
    validating moves, executing moves, and querying the current
    board state. It does not manage the overall game flow or UI.
    """

#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self):
        self.board = chess.Board()
        #! Stores the move history in SAN notation.
        #! python-chess preserves only chess.Move objects
        #! inside board.move_stack, not their SAN strings.
        self._san_history: List[str] = []

#% ==================================================
#! Game Management
#% ==================================================

    def reset(self) -> None:   
        """Reset the chess game to its initial state."""
        self.board.reset()
        self._san_history.clear()


#% ==================================================
#! Move Validation
#% ==================================================


    def get_legal_moves(self) -> List[chess.Move]:
        """
        Return all legal moves for the current board position.

        Returns:
            A list of all legal chess moves.
        """
        return list(self.board.legal_moves)


    def get_legal_targets(self, from_square: int) -> List[int]:
        """
        Return all legal destination squares for a piece
        located on the given square.
        """
        return [
            move.to_square
            for move in self.board.legal_moves
            if move.from_square == from_square
        ]


    def is_legal_move(self, from_square: int, to_square: int) -> bool:   
        """
        Check whether moving from one square to another is legal.
        Returns:
            True if the move is legal, otherwise False.
        """
        return self._find_move(from_square, to_square) is not None

#% ==================================================
#! Move Execution
#% ==================================================


    def make_move(self, from_square: int, to_square: int,    
                  promotion: Optional[int] = None) -> Optional[chess.Move]:
        """
        Execute a legal move on the chessboard.

        Returns:
            The executed chess.Move if successful, otherwise None.
        """ 
        legal_move = self._find_move(from_square, to_square, promotion)

        if legal_move is None:
            return None

        san = self.board.san(legal_move)
        self.board.push(legal_move)
        self._san_history.append(san) 

        return legal_move

#% ==================================================
#! Board Queries
#% ==================================================

    def get_piece_at(self, square: int) -> Optional[chess.Piece]:
        """
        Return the chess piece located on the given square.

        Args:
            square: The board square to inspect.

        Returns:
            The chess piece if one exists; otherwise None.
        """
        return self.board.piece_at(square)


    def get_piece_symbol_at(self, square: int) -> str:
        """
        Return the symbol of the piece located on the given square.

        Args:
            square: The board square to inspect.

        Returns:
            The piece symbol if one exists; otherwise an empty string.
        """
        piece = self.get_piece_at(square)
        return piece.symbol() if piece else "" 


    def get_piece_type_at(self, square: int) -> Optional[int]:
        """
        Return the type of the piece located on the given square.

        Args:
            square: The board square to inspect.

        Returns:
            The piece type if one exists; otherwise None.
        """
        piece = self.get_piece_at(square)
        return piece.piece_type if piece else None


    def get_piece_color_at(self, square: int) -> Optional[PlayerColor]:
        """
        Return the color of the piece located on the given square.

        Args:
            square: The board square to inspect.

        Returns:
            The piece color if one exists; otherwise None.
        """
        piece = self.get_piece_at(square)

        if piece is None:
            return None

        return (
            PlayerColor.WHITE
            if piece.color == chess.WHITE
            else PlayerColor.BLACK
        )


    def get_piece_map(self) -> dict[int, chess.Piece]:
        """
        Return a mapping of all occupied squares to their chess pieces.

        Returns:
            A dictionary where each key is a square index and
            each value is the corresponding chess piece.
        """
        return dict(self.board.piece_map())


#% ==================================================
#! Game Status
#% ==================================================

    def is_check(self) -> bool:
        """
        Check whether the current player's king is in check.

        Returns:
            True if the current player is in check; otherwise False.
        """
        return self.board.is_check()


    def is_checkmate(self) -> bool:
        """
        Check whether the current game is in checkmate.

        Returns:
            True if the game has ended by checkmate; otherwise False.
        """
        return self.board.is_checkmate()


    def is_stalemate(self) -> bool:
        """
        Check whether the current game is in stalemate.

        Returns:
            True if the game has ended by stalemate; otherwise False.
        """
        return self.board.is_stalemate()


    def is_insufficient_material(self) -> bool:
        """
        Check whether the game has insufficient material for checkmate.

        Returns:
            True if neither player has enough material to deliver
            checkmate; otherwise False.
        """
        return self.board.is_insufficient_material()


    def is_game_over(self) -> bool:
        """
        Check whether the current game has ended.

        Returns:
            True if the game is over; otherwise False.
        """
        return self.board.is_game_over()


    def can_claim_draw(self) -> bool:
        """
        Check whether the current player can claim a draw.

        Returns:
            True if the current player is allowed to claim
            a draw according to the rules of chess;
            otherwise False.
        """
        return self.board.can_claim_draw()


    def is_fifty_moves(self) -> bool:
        """
        Check whether the fifty-move rule condition has been reached.

        Returns:
            True if the fifty-move rule applies;
            otherwise False.
        """
        return self.board.is_fifty_moves()
 

    def is_repetition(self) -> bool:
        """
        Check whether the current board position has been repeated.

        Returns:
            True if the current position satisfies the repetition
            rule; otherwise False.
        """
        return self.board.is_repetition()


    def result(self) -> str:
        """
        Return the official result of the current game.

        Returns:
            The game result in standard chess notation:
            "1-0" for a White win,
            "0-1" for a Black win,
            "1/2-1/2" for a draw,
            or "*" if the game is still in progress.
        """
        return self.board.result()


    def is_pawn_promotion_move(self, from_square: int,to_square: int,) -> bool:
        """
        Check whether a move would result in a pawn promotion.

        Args:
            from_square: The source square.
            to_square: The destination square.

        Returns:
            True if the move reaches the promotion rank;
            otherwise False.
        """
        piece = self.board.piece_at(from_square)
        if piece is None or piece.piece_type != chess.PAWN:
            return False
        promotion_rank = 7 if piece.color == chess.WHITE else 0
        return chess.square_rank(to_square) == promotion_rank



    def outcome_reason(self) -> Optional[GameEndReason]:

        outcome = self.board.outcome()
        if outcome is None:
            return None
        return _TERMINATION_TO_GAME_END_REASON.get(
            outcome.termination,
            GameEndReason.UNKNOWN,
        )

#% ==================================================
#! Board State
#% ==================================================


    def get_turn_color(self) -> PlayerColor:
        """
        Return the color of the player whose turn it is.

        Returns:
            The current player's color.
        """
        return (
            PlayerColor.WHITE
            if self.board.turn == chess.WHITE
            else PlayerColor.BLACK
        )


    def get_fen(self) -> str:
        """
        Return the current board position in FEN notation.

        Returns:
            The current board state as a Forsyth-Edwards Notation (FEN) string.
        """
        return self.board.fen()


    def set_fen(self, fen: str) -> None:
        """
        Set the current board position from a FEN string.

        Args:
            fen: A valid Forsyth-Edwards Notation (FEN) string.
        """
        self.board.set_fen(fen)
        self._san_history.clear()

        
    def get_board_state(self) -> BoardState:
        """
        Return the current board state.

        Returns:
            A BoardState object representing the current board position.
        """
        return BoardState(
            fen=self.get_fen(),
            turn=self.get_turn_color(),
            move_count=len(self.board.move_stack),
            fullmove_number=self.board.fullmove_number,
        )




#% ==================================================
#! Move History
#% ==================================================

    def get_last_san(self) -> Optional[str]:
        """
        Return the last move in SAN notation.

        Returns:
            The last move in Standard Algebraic Notation (SAN)
            if one exists; otherwise None.
        """
        return self._san_history[-1] if self._san_history else None


    def get_san_history(self) -> List[str]:
        """
        Return the complete move history in SAN notation.

        Returns:
            A copy of the move history, where each move is
            represented in Standard Algebraic Notation (SAN).
        """
        return list(self._san_history)

#% ==================================================
#! Move Utilities
#% ==================================================


    def get_san(self, move: chess.Move) -> str:
        """
        Return the SAN representation of a chess move.

        Args:
            move: The move to convert.

        Returns:
            The move in Standard Algebraic Notation (SAN).
        """
        return self.board.san(move)


    def push_san(self, san: str) -> chess.Move:
        """
        Execute a move written in Standard Algebraic Notation (SAN).

        Args:
            san: The move in SAN format.

        Returns:
            The executed chess move.
        """
        move = self.board.parse_san(san)
        self.board.push(move)
        self._san_history.append(san) 

        return move


    def undo_last_move(self) -> Optional[chess.Move]:
        """
        Undo the last executed move.

        Returns:
            The undone chess move if one exists;
            otherwise None.
        """

        if not self.board.move_stack:
            return None

        move = self.board.pop()

        if self._san_history:
            self._san_history.pop()

        return move
 


#% ==================================================
#! Special Moves
#% ==================================================


    def is_castling_move(self, move: chess.Move) -> bool:
        """
        Check whether the given move is a castling move.

        Args:
            move: The move to inspect.

        Returns:
            True if the move is a castling move; otherwise False.
        """
        return self.board.is_castling(move)

 
    def is_en_passant_move(self, move: chess.Move) -> bool:
        """
        Check whether the given move is an en passant capture.

        Args:
            move: The move to inspect.

        Returns:
            True if the move is an en passant capture; otherwise False.
        """
        return self.board.is_en_passant(move)



#% ==================================================
#! UCI Utilities
#% ==================================================

    def parse_uci(self, uci: str) -> chess.Move:
        """
        Parse a UCI move string into a chess.Move object.

        Args:
            uci: A move in Universal Chess Interface (UCI) format.

        Returns:
            The corresponding chess.Move object.
        """
        return chess.Move.from_uci(uci)


    def uci_to_from_square(self, uci: str) -> int:
        """
        Return the source square from a UCI move string.

        Args:
            uci: A move in Universal Chess Interface (UCI) format.

        Returns:
            The source square index.
        """
        return self.parse_uci(uci).from_square


    def uci_to_to_square(self, uci: str) -> int:
        """
        Return the destination square from a UCI move string.

        Args:
            uci: A move in Universal Chess Interface (UCI) format.

        Returns:
            The destination square index.
        """
        return self.parse_uci(uci).to_square


    def uci_get_promotion(self, uci: str) -> Optional[int]:
        """
        Return the promotion piece encoded in a UCI move string.

        Args:
            uci: A move in Universal Chess Interface (UCI) format.

        Returns:
            The promotion piece type if present; otherwise None.
        """
        return self.parse_uci(uci).promotion


#% ==================================================
#! Board Utilities
#% ==================================================

    def get_last_move(self) -> Optional[chess.Move]:
        """
        Return the last executed move.

        Returns:
            The last chess move if one exists; otherwise None.
        """
        return self.board.peek() if self.board.move_stack else None




#% ==================================================
#! Private Helper Methods
#% ==================================================

    def _find_move(self, from_square: int, to_square: int, 
                   promotion: Optional[int] = None) -> Optional[chess.Move]:
        """
        Find a legal move matching the given source, destination,
        and optional promotion piece.
        """
        for move in self.board.legal_moves:
            if move.from_square != from_square:
                continue

            if move.to_square != to_square:
                continue

            if promotion is None:
                return move

            if move.promotion == promotion:
                return move

        return None



     


