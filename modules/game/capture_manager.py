from modules.shared.enums.player_color import PlayerColor


class CaptureManager:
    """
    Manages captured chess pieces for both players.

    This manager records captured piece symbols for each player
    and provides query operations for the recorded captures.

    It is responsible only for storing and retrieving capture
    information and does not perform move validation, move
    execution, or capture detection.
    """


#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self) -> None:
        """
        Initialize the capture manager.

        Creates empty capture collections for both players,
        ready to record captured pieces throughout the game.
        """

        #! Pieces captured by White (black pieces removed from the board).
        self._captured_by_white: list[str] = []

        #! Pieces captured by Black (white pieces removed from the board).
        self._captured_by_black: list[str] = []


#% ==================================================
#! Private Helpers
#% ==================================================

    def _get_capture_list(self, player: PlayerColor) -> list[str]:
        """
        Return the internal capture list for the specified player.

        Args:
            player: The player whose capture list should be returned.

        Returns:
            The internal list used to store captured pieces.

        Notes:
            This helper is intended for internal use only.
            Public methods should return defensive copies instead of
            exposing the internal collections directly.
        """

        if player == PlayerColor.WHITE:
            return self._captured_by_white

        return self._captured_by_black





#% ==================================================
#! Recording
#% ==================================================

    def record_capture(
        self,
        captured_by: PlayerColor,
        captured_piece_symbol: str,
    ) -> None:
        """
        Record a captured piece for the specified player.

        This method assumes that the supplied piece symbol has
        already been validated by the ChessEngine.

        Args:
            captured_by: The player who captured the piece.
            captured_piece_symbol: The FEN symbol of the captured piece.
        """

        self._get_capture_list(captured_by).append(captured_piece_symbol)


#% ==================================================
#! Query
#% ==================================================

    def get_captured_by(self, player: PlayerColor) -> list[str]:
        """
        Return a copy of the captured pieces for the specified player.

        Args:
            player: The player whose captured pieces should be returned.

        Returns:
            A defensive copy of the player's captured piece symbols.
        """

        return list(self._get_capture_list(player))



    def get_all_captured(self) -> dict[PlayerColor, list[str]]:
        """
        Return the captured pieces for both players.

        Returns:
            A mapping of each player to their captured piece symbols.
        """

        return {
            PlayerColor.WHITE: self.get_captured_by(PlayerColor.WHITE),
            PlayerColor.BLACK: self.get_captured_by(PlayerColor.BLACK),
        }


    def get_capture_count(self, player: PlayerColor) -> int:
        """
        Return the number of pieces captured by the specified player.

        Args:
            player: The player whose capture count should be returned.

        Returns:
            The total number of captured pieces recorded for the player.
        """

        return len(self._get_capture_list(player))



    def get_total_captures(self) -> int:
        """
        Return the total number of captured pieces.

        Returns:
            The combined capture count for both players.
        """

        return (
            self.get_capture_count(PlayerColor.WHITE)
            + self.get_capture_count(PlayerColor.BLACK)
        )


#% ==================================================
#! Management
#% ==================================================

    def clear(self) -> None:
        """
        Clear all recorded captures.

        This restores the manager to its initial empty state.
        """

        self._captured_by_white.clear()
        self._captured_by_black.clear()

