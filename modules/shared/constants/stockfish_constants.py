import platform
from pathlib import Path

from modules.shared.enums.difficulty import Difficulty


#% ==================================================
#! Project Paths
#% ==================================================

# Root directory of the project, resolved relative to this file.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

STOCKFISH_ROOT = PROJECT_ROOT / "assets" / "stockfish"
STOCKFISH_BIN_DIR = STOCKFISH_ROOT / "bin"



def _platform_key() -> str:
    system = platform.system().lower()

    if system == "windows":
        return "windows"

    if system == "darwin":
        return "macos"

    if system == "linux":
        return "linux"

    raise RuntimeError(f"Unsupported operating system: {system}")


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



