from pathlib import Path
import platform

from modules.shared.enums.difficulty import Difficulty


#% ==================================================
#! Project Paths
#% ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

STOCKFISH_ROOT = PROJECT_ROOT / "assets" / "stockfish"
STOCKFISH_BIN_DIR = STOCKFISH_ROOT / "bin"


def _platform_key() -> str:
    system = platform.system().lower()

    if system.startswith("win"):
        return "windows"

    if system == "darwin":
        return "macos"

    return "linux"


PLATFORM_KEY = _platform_key()


def _stockfish_filename() -> str:
    if PLATFORM_KEY == "windows":
        return "stockfish.exe"

    return "stockfish"


STOCKFISH_FILENAME = _stockfish_filename()

STOCKFISH_PLATFORM_DIR = STOCKFISH_BIN_DIR / PLATFORM_KEY

STOCKFISH_PATH = (
    STOCKFISH_PLATFORM_DIR
    / STOCKFISH_FILENAME
)


#% ==================================================
#! Stockfish Configuration
#% ==================================================

DIFFICULTY_TO_DEPTH = {
    Difficulty.EASY: 3,
    Difficulty.MEDIUM: 10,
    Difficulty.HARD: 18,
}

