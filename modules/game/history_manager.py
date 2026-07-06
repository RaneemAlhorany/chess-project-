
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



    def get_last_move(self) -> MoveRecord | None:
        """
        Return the most recently recorded move.

        Returns:
            The last recorded move, or None if the history is empty.
        """

        return self._moves[-1] if self._moves else None




    def get_move_at(self, index: int) -> MoveRecord | None:
        """
        Return the recorded move at the specified history index.

        Args:
            index: The zero-based position of the move.

        Returns:
            The requested move record, or None if the index is invalid.
        """

        if 0 <= index < len(self._moves):
            return self._moves[index]

        return None



    def get_move_count(self) -> int:
        """
        Return the number of recorded moves.

        Returns:
            The total number of recorded moves.
        """

        return len(self._moves)



    def get_current_index(self) -> int:
        """
        Return the current navigation position.

        Returns:
            The current move index, or -1 if the history is empty.
        """

        return self._current_index


#% ==================================================
#! Navigation
#% ==================================================

    def can_go_forward(self) -> bool:
        """
        Determine whether navigation can move forward.

        Returns:
            True if a later recorded move is available; otherwise False.
        """

        return self._current_index < len(self._moves) - 1




    def can_go_backward(self) -> bool:
        """
        Determine whether navigation can move backward.

        Returns:
            True if an earlier recorded move is available;
            otherwise False.
        """

        return self._current_index > 0



    def go_forward(self) -> MoveRecord | None:
        """
        Navigate to the next recorded move.

        Returns:
            The next move record, or None if already at the end
            of the history.
        """

        if not self.can_go_forward():
            return None

        self._current_index += 1
        return self._moves[self._current_index]




    def go_backward(self) -> MoveRecord | None:
        """
        Navigate to the previous recorded move.

        Returns:
            The previous move record, or None if already at the
            beginning of the history.
        """

        if not self.can_go_backward():
            return None

        self._current_index -= 1
        return self._moves[self._current_index]
    
#% ==================================================
#! Management
#% ==================================================


    def clear(self) -> None:
        """
        Clear the move history and reset the navigation state.
        """

        self._moves.clear()
        self._current_index = -1
