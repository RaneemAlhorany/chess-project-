import time
from modules.shared.enums.player_color import PlayerColor



class TimerManager:
    """
    Manages chess clocks for both players.

    This manager controls the remaining time for each player,
    supports configurable time controls, and handles clock
    operations such as starting, pausing, resuming, stopping,
    and switching turns.

    It is responsible only for time management and does not
    determine player turns, validate moves, or decide game
    outcomes.
    """



#% ==================================================
#! Constructor
#% ==================================================

    def __init__(
        self,
        initial_seconds: float = 600.0,
        increment_seconds: float = 0.0,
    ) -> None:
        """
        Initialize the timer manager.

        Args:
            initial_seconds: The starting time, in seconds,
                assigned to each player.
            increment_seconds: The bonus time, in seconds,
                added after each completed move.
        """

        #! Configured time control.
        self._initial_time: float = initial_seconds
        self._increment: float = increment_seconds

        #! Remaining time for each player.
        self._white_time: float = initial_seconds
        self._black_time: float = initial_seconds

        #! Runtime clock state.
        self._active_color: PlayerColor | None = None
        self._turn_started_at: float | None = None
        self._running: bool = False

#% ==================================================
#! Time Control
#% ==================================================

    def set_time_control(
        self,
        initial_seconds: float,
        increment_seconds: float = 0.0,
    ) -> None:
        """
        Configure a new time control and reset both clocks.

        Args:
            initial_seconds: The starting time, in seconds,
                assigned to each player.
            increment_seconds: The bonus time, in seconds,
                added after each completed move.
        """

        self._initial_time = initial_seconds
        self._increment = increment_seconds

        self.reset()


    def get_initial_time(self) -> float:
        """
        Return the configured initial time for each player.

        Returns:
            The initial time, in seconds.
        """

        return self._initial_time


    def get_increment(self) -> float:
        """
        Return the configured increment for each move.

        Returns:
            The increment, in seconds.
        """

        return self._increment

#% ==================================================
#! Clock Controls
#% ==================================================


    def start(self, color: PlayerColor) -> None:
        """
        Start the clock for the specified player.

        Args:
            color: The player whose clock should begin running.
        """

        if self._running:
            return

        self._active_color = color
        self._start_clock()



    def switch(self) -> None:
        """
        Switch the active clock to the opposing player.

        The active player's remaining time is updated before
        the opponent's clock begins running.
        """

        if not self._running or self._active_color is None:
            return

        self._deduct_elapsed()

        if self._active_color == PlayerColor.WHITE:
            self._white_time += self._increment
            self._active_color = PlayerColor.BLACK
        else:
            self._black_time += self._increment
            self._active_color = PlayerColor.WHITE

        self._start_clock()


    def pause(self) -> None:
        """
        Pause the active clock.

        The active player's remaining time is updated before
        the clock is suspended.
        """

        if not self._running or self._active_color is None:
            return

        self._deduct_elapsed()
        self._running = False
        self._turn_started_at = None


    def resume(self) -> None:
        """
        Resume the active player's clock.

        The timer continues from the player's remaining time
        without changing the active player.
        """

        if self._running or self._active_color is None:
            return

        self._start_clock()


    def stop(self) -> None:
        """
        Stop the timer.

        If the clock is currently running, the active player's
        remaining time is updated before the timer is reset.
        """

        if self._active_color is None:
            return

        if self._running:
            self._deduct_elapsed()

        self._running = False
        self._active_color = None
        self._turn_started_at = None



#% ==================================================
#! Private Helpers
#% ==================================================


    def _start_clock(self) -> None:
        """
        Start timing for the current active player.

        This helper records the current timestamp and marks
        the timer as running.
        """

        self._turn_started_at = time.monotonic()
        self._running = True


    def _deduct_elapsed(self) -> float:
        """
        Update the active player's remaining time.

        Returns:
            The elapsed time, in seconds, that was deducted
            from the active player's clock.
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


    def _get_remaining_time_value(self, player: PlayerColor) -> float:
        """
        Return the stored remaining time for the specified player.

        Args:
            player: The player whose stored remaining time should
                be returned.

        Returns:
            The internally stored remaining time, in seconds.
        """

        if player == PlayerColor.WHITE:
            return self._white_time

        return self._black_time



#% ==================================================
#! Query
#% ==================================================

    def get_remaining_time(self, color: PlayerColor) -> float:
        """
        Return the remaining time for the specified player.

        If the player's clock is currently running, the returned
        value reflects the elapsed time up to the moment of the call.

        Args:
            color: The player whose remaining time should be returned.

        Returns:
            The remaining time, in seconds.
        """

        remaining = self._get_remaining_time_value(color)

        if (
            self._running
            and self._active_color == color
            and self._turn_started_at is not None
        ):
            elapsed = time.monotonic() - self._turn_started_at
            remaining = max(0.0, remaining - elapsed)

        return remaining


    def get_active_color(self) -> PlayerColor | None:
        """
        Return the player whose clock is currently active.

        Returns:
            The active player, or None if no clock is active.
        """

        return self._active_color


    def is_running(self) -> bool:
        """
        Return whether the timer is currently running.

        Returns:
            True if a player's clock is active; otherwise False.
        """

        return self._running


    def is_time_up(self) -> PlayerColor | None:
        """
        Return the player whose time has expired.

        Returns:
            The player whose remaining time has reached zero,
            or None if both players still have time remaining.
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
        Reset the timer to its configured initial state.

        The configured time control remains unchanged, while
        both player clocks and the runtime state are restored.
        """

        self._white_time = self._initial_time
        self._black_time = self._initial_time

        self._active_color = None
        self._turn_started_at = None
        self._running = False

