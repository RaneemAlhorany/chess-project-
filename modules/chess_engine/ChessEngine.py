import chess
from typing import Optional, List


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

    def __init__(self):  #   (Constructor)   Creates a new chessboard & Creates a record of moves
        self.board = chess.Board()
        self._move_log: List[str] = [] #! can delete
        ## TODO:
        # Re-evaluate whether _move_log is necessary.
        # python-chess already provides board.move_stack.
        # Decide later whether to keep this cache or rely on the library.

    #% ==================================================
    #! Game Management
    #% ==================================================

    def reset(self) -> None:   
        """Reset the chess game to its initial state."""
        self.board.reset()
        self._move_log.clear() # # TODO: Re-evaluate _move_log after ChessEngine review.


    #% ==================================================
    #! Move Validation
    #% ==================================================


    def get_legal_moves(self) -> List[chess.Move]:
        """
        Return all legal moves for the current board position.
        Returns:
            List[chess.Move]: A list of all legal moves.
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
        self._move_log.append(san) #! TODO: Review _move_log usage after ChessEngine refactoring.

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


# 31
    def get_piece_color_at(self, square: int) -> Optional[bool]:
        piece = self.board.piece_at(square)
        return piece.color if piece else None




    
    get_piece_map()




# ! last section in the file
#$ ==================================================
#! Private Helper Methods
#$ ==================================================

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






    # ==================================================
    # Game Status
    # ==================================================

    is_check()

    is_checkmate()

    ...


    # ==================================================
    # FEN
    # ==================================================

    get_fen()

    set_fen()


    # ==================================================
    # Move History
    # ==================================================

    get_last_san()

    get_move_log()



    # !Utility Methods








        

# 30
    def is_check(self) -> bool:
        return self.board.is_check()
# 29
    def is_checkmate(self) -> bool:
        return self.board.is_checkmate()
# 28
    def is_stalemate(self) -> bool:
        return self.board.is_stalemate()
# 27
    def is_insufficient_material(self) -> bool:
        return self.board.is_insufficient_material()
# 26
    def is_game_over(self) -> bool:
        return self.board.is_game_over()
# 25
    def can_claim_draw(self) -> bool:
        return self.board.can_claim_draw()
# 24
    def is_fifty_moves(self) -> bool:
        return self.board.is_fifty_moves()
# 23
    def is_repetition(self) -> bool:
        return self.board.is_repetition()
# 22
    def result(self) -> str:
        return self.board.result()
# 21
    def outcome(self) -> Optional[chess.Outcome]:
        return self.board.outcome()
# 20
    def outcome_reason(self) -> Optional[str]:
        outcome = self.board.outcome()
        if outcome is None:
            return None
        if outcome.termination == chess.Termination.CHECKMATE:
            return "checkmate"
        if outcome.termination == chess.Termination.STALEMATE:
            return "stalemate"
        if outcome.termination == chess.Termination.INSUFFICIENT_MATERIAL:
            return "insufficient_material"
        if outcome.termination == chess.Termination.FIFTY_MOVES:
            return "fifty_move_rule"
        if outcome.termination == chess.Termination.THREEFOLD_REPETITION:
            return "threefold_repetition"
        if outcome.termination == chess.Termination.SEVENTYFIVE_MOVES:
            return "fifty_move_rule"
        if outcome.termination == chess.Termination.FIVEFOLD_REPETITION:
            return "threefold_repetition"
        if outcome.termination == chess.Termination.VARIANT_WIN:
            return "variant_win"
        if outcome.termination == chess.Termination.VARIANT_LOSS:
            return "variant_loss"
        return "unknown"
# 19
    def get_turn(self) -> bool: 
        return self.board.turn
# 18
    def get_turn_color(self) -> str:
        return "white" if self.board.turn else "black"
# 17
    def get_fen(self) -> str: #get board state in FEN notation
        return self.board.fen()
# 16
    def set_fen(self, fen: str) -> None: #set board state in FEN notation
        self.board = chess.Board(fen)
# 15
    def get_san(self, move: chess.Move) -> str:
        return self.board.san(move)
# 14
    def get_last_san(self) -> Optional[str]: #The last move of the game
        return self._move_log[-1] if self._move_log else None
# 13
    def get_move_log(self) -> List[str]: # Tha all moves of the game are returned in SAN notation.
        return list(self._move_log)


# 12
    def is_castling_move(self, move: chess.Move) -> bool: # Castling rookie move and king move are returned as true.
        return self.board.is_castling(move)
# 11
    def is_en_passant_move(self, move: chess.Move) -> bool:
        return self.board.is_en_passant(move)
# 10
    def get_last_move(self) -> Optional[chess.Move]:
        return self.board.peek() if self.board.move_stack else None
# 9
    def has_king(self, color: bool) -> bool:
        return any(
            piece and piece.piece_type == chess.KING and piece.color == color
            for piece in self.board.piece_map().values()
        )
# 8
    def get_board_state(self) -> dict:
        state = {
            "fen": self.get_fen(),
            "turn": self.get_turn_color(),
            "is_check": self.is_check(),
            "is_checkmate": self.is_checkmate(),
            "is_stalemate": self.is_stalemate(),
            "is_game_over": self.is_game_over(),
            "is_insufficient_material": self.is_insufficient_material(),
            "is_fifty_moves": self.is_fifty_moves(),
            "is_repetition": self.is_repetition(),
            "move_count": len(self._move_log),
            "fullmove_number": self.board.fullmove_number,
        }
        return state
# 7
    def undo_last_move(self) -> Optional[chess.Move]:
        if self.board.move_stack:
            move = self.board.pop()
            if self._move_log:
                self._move_log.pop()
            return move
        return None
# 6
    def push_san(self, san: str) -> chess.Move: #A movement written in SAN format is executed.
        move = self.board.parse_san(san)
        self.board.push(move)
        self._move_log.append(san)
        return move
# 5
    def get_piece_map(self) -> dict:
        return dict(self.board.piece_map())
# 4
    def parse_uci(self, uci: str) -> chess.Move:
        return chess.Move.from_uci(uci)
# 3
    def uci_to_from_square(self, uci: str) -> int:
        return chess.Move.from_uci(uci).from_square
# 2
    def uci_to_to_square(self, uci: str) -> int:
        return chess.Move.from_uci(uci).to_square
# 1
    def uci_get_promotion(self, uci: str) -> Optional[int]:
        return chess.Move.from_uci(uci).promotion


///////////////////////////////////////////////



#! TODO: Review whether this method is needed.
    def is_pawn_promotion_move(self, from_square: int, to_square: int) -> bool: 
        piece = self.board.piece_at(from_square)

        if piece is None or piece.piece_type != chess.PAWN:
            return False

        return is_promotion_rank(to_square, piece.color == chess.WHITE)




