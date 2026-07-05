from pathlib import Path

from modules.shared.enums.difficulty import Difficulty


#% ==================================================
#! Project Paths
#% ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

STOCKFISH_PATH = (
    PROJECT_ROOT
    / "assets"
    / "stockfish"
    / "stockfish.exe"
)


#% ==================================================
#! Stockfish Configuration
#% ==================================================

DIFFICULTY_TO_DEPTH = {
    Difficulty.EASY: 3,
    Difficulty.MEDIUM: 10,
    Difficulty.HARD: 18,
}

