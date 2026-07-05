import time

from typing import Optional

from modules.shared.enums.player_color import PlayerColor


class TimerManager:
    """
    Manages chess clocks for both players.

    Supports standard time controls with an optional increment
    applied after each move.  Each player's clock counts down
    independently; the active clock belongs to the player whose
    turn it is.
    """

#% ==================================================
#! Constructor
#% ==================================================

    def __init__(self,
                 initial_seconds: float = 600.0,
                 increment_seconds: float = 0.0) -> None:
        """
        Initialise both clocks with the given time control.

        Args:
            initial_seconds: Starting time in seconds for each player
                             (default 10 minutes).
            increment_seconds: Bonus seconds added after each move
                               (default 0).
        """

        #! Time control parameters.
        self._initial_time: float = initial_seconds
        self._increment: float = increment_seconds

        #! Remaining time in seconds for each player.
        self._white_time: float = initial_seconds
        self._black_time: float = initial_seconds

        #! Which clock is currently ticking, if any.
        self._active_color: Optional[PlayerColor] = None

        #! Monotonic timestamp of when the active clock was started.
        self._turn_started_at: Optional[float] = None

        #! Whether the clock is running.
        self._running: bool = False

#% ==================================================
#! Time Control
#% ==================================================

    def set_time_control(self,
                         initial_seconds: float,
                         increment_seconds: float = 0.0) -> None:
        """
        Update the time control parameters and reset both clocks.

        Args:
            initial_seconds: New starting time in seconds per player.
            increment_seconds: New increment in seconds per move.
        """

        self.stop()

        self._initial_time = initial_seconds
        self._increment = increment_seconds

        self._white_time = initial_seconds
        self._black_time = initial_seconds

    def get_initial_time(self) -> float:
        """
        Return the configured initial time per player.

        Returns:
            The starting time in seconds.
        """

        return self._initial_time

    def get_increment(self) -> float:
        """
        Return the configured increment per move.

        Returns:
            The increment in seconds.
        """

        return self._increment

#% ==================================================
#! Clock Controls
#% ==================================================

    def start(self, color: PlayerColor) -> None:
        """
        Start (or resume) the clock for the given player.

        If the clocks were previously stopped, the active colour
        is set and its timer begins counting down from its
        remaining time.

        Args:
            color: The player whose clock should start ticking.
        """

        self._active_color = color
        self._turn_started_at = time.monotonic()
        self._running = True

    def switch(self) -> None:
        """
        Switch the active clock after a move.

        The current player's elapsed time is deducted, the
        increment is applied to that player, and the opponent's
        clock starts.
        """

        if not self._running or self._active_color is None:
            return

        elapsed = self._deduct_elapsed()

        # Apply increment to the player who just moved.
        if self._active_color == PlayerColor.WHITE:
            self._white_time += self._increment
        else:
            self._black_time += self._increment

        # Switch to the opponent.
        self._active_color = (
            PlayerColor.BLACK
            if self._active_color == PlayerColor.WHITE
            else PlayerColor.WHITE
        )

        self._turn_started_at = time.monotonic()

    def pause(self) -> None:
        """
        Pause the active clock without switching turns.

        The elapsed time since the last start or switch is
        deducted from the active player's remaining time.
        """

        if not self._running or self._active_color is None:
            return

        self._deduct_elapsed()
        self._running = False
        self._turn_started_at = None

    def resume(self) -> None:
        """
        Resume a paused clock for the same active player.
        """

        if self._running or self._active_color is None:
            return

        self._turn_started_at = time.monotonic()
        self._running = True

    def stop(self) -> None:
        """
        Stop the clock entirely and deduct any remaining elapsed time.
        """

        if self._active_color is None:
            return

        if self._running:
            self._deduct_elapsed()

        self._running = False
        self._active_color = None
        self._turn_started_at = None

#% ==================================================
#! Helpers
#% ==================================================

    def _deduct_elapsed(self) -> float:
        """
        Deduct the elapsed time from the currently active clock.

        Returns:
            The number of seconds that were deducted.

        Raises:
            RuntimeError: if no clock is active.
        """

        if self._active_color is None or self._turn_started_at is None:
            return 0.0

        now = time.monotonic()
        elapsed = now - self._turn_started_at
        self._turn_started_at = now

        if self._active_color == PlayerColor.WHITE:
            self._white_time = max(0.0, self._white_time - elapsed)
        else:
            self._black_time = max(0.0, self._black_time - elapsed)

        return elapsed

#% ==================================================
#! Query
#% ==================================================

    def get_remaining_time(self, color: PlayerColor) -> float:
        """
        Return the remaining time for the given player.

        If the player's clock is actively running, the returned
        value accounts for time elapsed up to the instant of the
        call.

        Args:
            color: The player colour to query.

        Returns:
            Remaining time in seconds (never negative).
        """

        remaining = (
            self._white_time
            if color == PlayerColor.WHITE
            else self._black_time
        )

        if self._running and self._active_color == color:
            elapsed = time.monotonic() - (self._turn_started_at or 0.0)
            remaining = max(0.0, remaining - elapsed)

        return remaining

    def get_active_color(self) -> Optional[PlayerColor]:
        """
        Return the colour whose clock is currently active.

        Returns:
            The active PlayerColor, or None if no clock is running.
        """

        return self._active_color

    def is_running(self) -> bool:
        """
        Check whether any clock is currently ticking.

        Returns:
            True if a clock is active; otherwise False.
        """

        return self._running

    def is_time_up(self) -> Optional[PlayerColor]:
        """
        Check whether either player has run out of time.

        Returns:
            The PlayerColor whose time has expired, or None if
            both players still have time remaining.
        """

        white = self.get_remaining_time(PlayerColor.WHITE)
        black = self.get_remaining_time(PlayerColor.BLACK)

        if white <= 0.0:
            return PlayerColor.WHITE

        if black <= 0.0:
            return PlayerColor.BLACK

        return None

#% ==================================================
#! Management
#% ==================================================

    def reset(self) -> None:
        """
        Reset both clocks to the configured initial time and stop.

        This does NOT change the time control parameters; use
        ``set_time_control`` to change those.
        """

        self._white_time = self._initial_time
        self._black_time = self._initial_time
        self._active_color = None
        self._turn_started_at = None
        self._running = False
