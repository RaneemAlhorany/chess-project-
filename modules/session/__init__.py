from dataclasses import dataclass
from typing import Optional

from modules.game.game_state import GameState


@dataclass(slots=True)
class Session:
    """
    Stores persistent session data for Streamlit.
    """

    game_state: Optional[GameState] = None