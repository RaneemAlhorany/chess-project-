
#% ==================================================
#! Models
#% ==================================================

from modules.models.move_record import MoveRecord



class HistoryManager:
    """
    Manages the move history of a chess game.

    This manager records played moves, provides access to the
    recorded history, and supports navigation through previously
    recorded moves.

    It is responsible only for managing move history and does
    not perform move validation or game logic.
    """

#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self) -> None:
        """
        Initialize the history manager.

        Creates an empty move history and resets the navigation
        position to its initial state.
        """

        #! Ordered list of recorded moves.
        self._moves: list[MoveRecord] = []

        #! Current position within the move history (-1 means no moves).
        self._current_index: int = -1


#% ==================================================
#! Recording & Undo
#% ==================================================

    def record_move(self, record: MoveRecord) -> None:
        """
        Record a move in the history.

        If the current navigation position is not at the end of the
        history, all subsequent moves are discarded before recording
        the new move.

        Args:
            record: The move record to add to the history.
        """

        if self._current_index < len(self._moves) - 1:
            self._moves = self._moves[: self._current_index + 1]

        self._moves.append(record)
        self._current_index = len(self._moves) - 1


    def undo_last(self) -> MoveRecord | None:
        """
        Remove and return the last recorded move.

        Returns:
            The removed move record, or None if the history is empty.
        """

        if not self._moves:
            return None

        removed_move = self._moves.pop()
        self._current_index = len(self._moves) - 1

        return removed_move


#% ==================================================
#! Query
#% ==================================================

    def get_history(self) -> list[MoveRecord]:
        """
        Return a copy of the recorded move history.

        Returns:
            A list of move records in chronological order.
        """

        return list(self._moves)






# 9
    def get_last_move(self) -> Optional[MoveRecord]:
        """
        Return the most recent move without removing it.

        Returns:
            The last MoveRecord if one exists; otherwise None.
        """

        return self._moves[-1] if self._moves else None

# 8
    def get_move_at(self, index: int) -> Optional[MoveRecord]:
        """
        Return the move at a specific index in the history.

        Args:
            index: Zero-based position in the history.

        Returns:
            The MoveRecord at that index, or None if out of range.
        """

        if 0 <= index < len(self._moves):
            return self._moves[index]

        return None
# 7
    def get_move_count(self) -> int:
        """
        Return the total number of moves stored in the history.

        Returns:
            The length of the move history.
        """

        return len(self._moves)

# 6
    def get_current_index(self) -> int:
        """
        Return the index of the currently-viewed move.

        Returns:
            The current navigation index, or -1 if no moves exist.
        """

        return self._current_index

#% ==================================================
#! Navigation
#% ==================================================

# 5
    def can_go_forward(self) -> bool:
        """
        Check whether a later move exists to navigate to.

        Returns:
            True if there is a move ahead of the current index.
        """

        return self._current_index < len(self._moves) - 1

# 4
    def can_go_backward(self) -> bool:
        """
        Check whether an earlier move exists to navigate to.

        Returns:
            True if there is a move before the current index.
        """

        return self._current_index > 0

# 3
    def go_forward(self) -> Optional[MoveRecord]:
        """
        Advance the current index by one and return that move.

        Returns:
            The next MoveRecord, or None if already at the end.
        """

        if not self.can_go_forward():
            return None

        self._current_index += 1
        return self._moves[self._current_index]

# 2
    def go_backward(self) -> Optional[MoveRecord]:
        """
        Rewind the current index by one and return that move.

        Returns:
            The previous MoveRecord, or None if already at the start.
        """

        if not self.can_go_backward():
            return None

        self._current_index -= 1
        return self._moves[self._current_index]

#% ==================================================
#! Management
#% ==================================================

# 1
    def clear(self) -> None:
        """
        Reset the history to an empty state.
        """

        self._moves.clear()
        self._current_index = -1
