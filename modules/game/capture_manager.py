from typing import Dict, List

from modules.shared.enums.player_color import PlayerColor


class CaptureManager:
    """
    Tracks which pieces have been captured by each player.

    The manager maintains separate lists of captured piece symbols
    for White and Black, allowing the UI to display captured
    material for both sides.
    """

#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self) -> None:
        """
        Initialise empty capture lists for both players.
        """

        #! Pieces captured by White (black pieces removed from the board).
        self._captured_by_white: List[str] = []

        #! Pieces captured by Black (white pieces removed from the board).
        self._captured_by_black: List[str] = []

#% ==================================================
#! Recording
#% ==================================================

    def record_capture(self, captured_piece_symbol: str,
                       captured_by: PlayerColor) -> None:
        """
        Record a captured piece under the capturing player's colour.

        Args:
            captured_piece_symbol: FEN-style symbol of the captured piece
                                   (e.g. 'P', 'N', 'B', 'R', 'Q', 'K').
            captured_by: The colour of the player who made the capture.
        """

        if captured_by == PlayerColor.WHITE:
            self._captured_by_white.append(captured_piece_symbol)
        else:
            self._captured_by_black.append(captured_piece_symbol)

#% ==================================================
#! Query
#% ==================================================

    def get_captured_by(self, color: PlayerColor) -> List[str]:
        """
        Return a shallow copy of the pieces captured by the given colour.

        Args:
            color: The player colour to query.

        Returns:
            A list of piece symbols captured by that player.
        """

        if color == PlayerColor.WHITE:
            return list(self._captured_by_white)

        return list(self._captured_by_black)

    def get_all_captured(self) -> Dict[PlayerColor, List[str]]:
        """
        Return all captured pieces organised by capturing player colour.

        Returns:
            A dict mapping each PlayerColor to its list of captured pieces.
        """

        return {
            PlayerColor.WHITE: self.get_captured_by(PlayerColor.WHITE),
            PlayerColor.BLACK: self.get_captured_by(PlayerColor.BLACK),
        }

    def get_material_count(self, color: PlayerColor) -> int:
        """
        Return the total number of pieces captured by the given colour.

        Args:
            color: The player colour to query.

        Returns:
            The count of captured pieces for that player.
        """

        if color == PlayerColor.WHITE:
            return len(self._captured_by_white)

        return len(self._captured_by_black)

    def get_total_captures(self) -> int:
        """
        Return the total number of captures across both players.

        Returns:
            The sum of all captured pieces.
        """

        return self.get_material_count(PlayerColor.WHITE) + self.get_material_count(PlayerColor.BLACK)

#% ==================================================
#! Management
#% ==================================================

    def clear(self) -> None:
        """
        Reset all capture lists to their empty initial state.
        """

        self._captured_by_white.clear()
        self._captured_by_black.clear()
