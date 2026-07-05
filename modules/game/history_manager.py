from typing import List, Optional

from modules.models.move_record import MoveRecord


class HistoryManager:
    """
    Manages the full move history with rich per-move metadata.

    Each move is stored as a MoveRecord containing SAN notation,
    source/destination squares, piece information, special-move
    flags, and resulting board status.

    The manager also supports basic navigation (forward/backward)
    for reviewing previously played moves.
    """

#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self) -> None:
        """
        Initialise an empty move history.

        The current index always points to the last recorded move;
        navigation methods adjust this index without modifying the
        underlying history.
        """

        #! Ordered list of all recorded moves.
        self._moves: List[MoveRecord] = []

        #! Index of the currently-viewed move (-1 means no move yet).
        self._current_index: int = -1

#% ==================================================
#! Recording & Undo
#% ==================================================

    def record_move(self, record: MoveRecord) -> None:
        """
        Append a move record to the history and advance the index.

        If the user had navigated backwards, any moves after the
        current index are discarded before recording (branching
        history is not supported).

        Args:
            record: The fully-populated MoveRecord to store.
        """

        if self._current_index < len(self._moves) - 1:
            self._moves = self._moves[: self._current_index + 1]

        self._moves.append(record)
        self._current_index = len(self._moves) - 1

    def undo_last(self) -> Optional[MoveRecord]:
        """
        Remove and return the most recently recorded move.

        Returns:
            The removed MoveRecord if one existed; otherwise None.
        """

        if not self._moves:
            return None

        popped = self._moves.pop()
        self._current_index = len(self._moves) - 1

        return popped

#% ==================================================
#! Query
#% ==================================================

    def get_history(self) -> List[MoveRecord]:
        """
        Return a shallow copy of the entire move history.

        Returns:
            A list of all MoveRecord objects in chronological order.
        """

        return list(self._moves)

    def get_last_move(self) -> Optional[MoveRecord]:
        """
        Return the most recent move without removing it.

        Returns:
            The last MoveRecord if one exists; otherwise None.
        """

        return self._moves[-1] if self._moves else None

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

    def get_move_count(self) -> int:
        """
        Return the total number of moves stored in the history.

        Returns:
            The length of the move history.
        """

        return len(self._moves)

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

    def can_go_forward(self) -> bool:
        """
        Check whether a later move exists to navigate to.

        Returns:
            True if there is a move ahead of the current index.
        """

        return self._current_index < len(self._moves) - 1

    def can_go_backward(self) -> bool:
        """
        Check whether an earlier move exists to navigate to.

        Returns:
            True if there is a move before the current index.
        """

        return self._current_index > 0

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

    def clear(self) -> None:
        """
        Reset the history to an empty state.
        """

        self._moves.clear()
        self._current_index = -1
