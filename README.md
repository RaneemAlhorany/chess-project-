# Chess Project

A feature-rich chess application built with **Streamlit** and **Python**, supporting both human-vs-human and human-vs-AI gameplay with a polished visual interface, chess clocks, move history, and bilingual (English/Arabic) support.

---

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`. The Stockfish binary is downloaded automatically on first bot game.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Modules Overview](#modules-overview)
  - [app.py — Application Entry Point](#apppy--application-entry-point)
  - [Shared Enums](#shared-enums)
  - [ChessEngine](#chessengine)
  - [StockfishEngine](#stockfishengine)
  - [Stockfish Installer](#stockfish-installer)
  - [GameState](#gamestate)
  - [GameManager](#gamemanager)
  - [CaptureManager](#capturemanager)
  - [HistoryManager](#historymanager)
  - [TimerManager](#timermanager)
  - [BoardState](#boardstate)
  - [MoveRecord](#moverecord)
  - [SessionManager](#sessionmanager)
  - [Shared Constants](#shared-constants)
  - [UI Screens](#ui-screens)
  - [Translations / i18n](#translations--i18n)
- [Architecture & Data Flow](#architecture--data-flow)
- [Configuration](#configuration)

---

## Features

- **Two game modes:** Play against a friend (hot-seat) or against the Stockfish AI engine.
- **Three difficulty levels:** Easy (depth 3), Medium (depth 10), Hard (depth 18).
- **Interactive chess board:** Click-to-select and click-to-move with visual highlights for legal moves and capturable pieces.
- **Chess clocks:** 10-minute-per-side timer with increment support, live countdown, and timeout detection.
- **Pawn promotion popup:** Choose Queen, Rook, Bishop, or Knight.
- **Move history panel:** Scrollable list of moves in Standard Algebraic Notation (SAN).
- **Game result popup:** Displays the winner and reason (checkmate or timeout) with Play Again / Main Page buttons.
- **Bilingual interface:** Full English and Arabic (العربية) translations with a toggle button.
- **Custom theming:** Dark walnut aesthetic with gold accents, serif typography, and full-screen background images.
- **Stockfish auto-installer:** Downloads and sets up the correct Stockfish binary for the user's platform (Windows, macOS, Linux) directly from GitHub releases.
- **Session persistence:** Game state is saved to Streamlit's session state for continuity during navigation.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12+** | Core language |
| **Streamlit** | Web UI framework |
| **python-chess** | Chess rules, move validation, board representation |
| **stockfish** | UCI wrapper for the Stockfish chess engine |
| **requests** | Downloading Stockfish binaries from GitHub |

---

## Project Structure

```
chess-project-/
├── app.py                                  # Application entry point
├── requirements.txt                        # Python dependencies
├── .gitignore                              # Git ignore rules
│
├── .streamlit/
│   └── config.toml                         # Streamlit theme config (dark walnut)
│
├── assets/
│   ├── images/
│   │   ├── Game.png                        # Background for the game screen
│   │   ├── home.png                        # Background for the home screen
│   │   ├── mode.png                        # Background for the mode select screen
│   │   ├── pawn.png                        # Background for the promotion popup
│   │   ├── select.png                      # Background for the difficulty popup
│   │   └── victory.png                     # Background for the result popup
│   ├── stockfish/                          # Stockfish binaries (downloaded at runtime)
│   └── icons/ & flags/                     # Additional static assets
│
├── translations/
│   ├── i18n.py                             # Translation lookup and normalization
│   └── strings.py                          # Legacy string constants
│
└── modules/
    ├── chess_engine/
    │   ├── __init__.py
    │   └── ChessEngine.py                  # Wrapper around python-chess
    │
    ├── bot/
    │   ├── __init__.py
    │   ├── stockfish_engine.py             # Stockfish wrapper (AI opponent)
    │   └── stockfish_installer.py          # Auto-download and setup of Stockfish
    │
    ├── game/
    │   ├── __init__.py
    │   ├── game_manager.py                 # Central game controller
    │   ├── game_state.py                   # Dataclass for game metadata
    │   ├── capture_manager.py              # Tracks captured pieces
    │   ├── history_manager.py              # Move history with navigation
    │   └── timer_manager.py                # Chess clock management
    │
    ├── models/
    │   ├── __init__.py
    │   ├── board_state.py                  # FEN + turn + move count dataclass
    │   └── move_record.py                  # Single move metadata dataclass
    │
    ├── session/
    │   ├── __init__.py                     # Session dataclass
    │   └── session_manager.py              # Streamlit session wrapper
    │
    ├── shared/
    │   ├── constants/
    │   │   ├── board_constants.py          # Board dimensions, FEN, promotion pieces
    │   │   ├── session_constants.py        # Session key definitions
    │   │   ├── stockfish_constants.py      # Paths, platform detection, depth mapping
    │   │   └── ui_constants.py             # Page title, icon, layout, messages
    │   ├── enums/
    │   │   ├── difficulty.py               # EASY, MEDIUM, HARD
    │   │   ├── game_end_reason.py          # CHECKMATE, STALEMATE, etc.
    │   │   ├── game_mode.py                # FRIEND, BOT
    │   │   ├── game_status.py              # NOT_STARTED, RUNNING, FINISHED
    │   │   └── player_color.py             # WHITE, BLACK
    │   └── helpers/
    │       └── display.py                  # Enum-to-label formatter
    │
    └── ui/
        ├── home.py                         # Home screen with "Begin Game" button
        ├── mode_select.py                  # Mode selection (Friend / AI)
        ├── difficulty.py                   # Difficulty selection popup
        ├── game.py                         # Main game screen (board, clocks, history)
        ├── promotion.py                    # Pawn promotion popup
        ├── result.py                       # Game result popup
        └── history.py                      # (reserved)
```

---

## Modules Overview

### app.py — Application Entry Point

**File:** `app.py`

#### Overview

The main entry point that configures the Streamlit page and routes between screens using `st.session_state.screen`.

#### Responsibilities

- Configuring the Streamlit page (title, icon, layout).
- Initializing session defaults (screen, language, mode, difficulty).
- Routing between screens: `home`, `mode`, `difficulty`, `game`.
- Managing the `GameManager` singleton.
- Preloading the Stockfish engine if available from a previous session.

#### Screen Flow

```
home → mode → difficulty (if bot) → game
```

#### Design Decisions

- Uses a `get_manager()` function to lazily initialize and reuse the `GameManager` across reruns.
- Session defaults are initialized once using guard clauses (`if "screen" not in st.session_state`).

---

### Shared Enums

**Location:** `modules/shared/enums/`

#### Overview

The `enums` package contains all shared enumerations used throughout the project. Its purpose is to centralize all fixed values in one place, making the code more readable, maintainable, and less prone to errors caused by hard-coded strings.

#### Enums

##### Difficulty

Represents the available bot difficulty levels.

- `EASY`
- `MEDIUM`
- `HARD`

##### GameMode

Represents the available game modes.

- `FRIEND` — play against another human
- `BOT` — play against the AI

##### GameStatus

Represents the lifecycle state of the current game.

- `NOT_STARTED`
- `RUNNING`
- `FINISHED`

##### PlayerColor

Represents the two player colors in chess.

- `WHITE`
- `BLACK`

##### GameEndReason

Represents the possible reasons why a chess game ended.

- `CHECKMATE`
- `STALEMATE`
- `INSUFFICIENT_MATERIAL`
- `FIFTY_MOVE_RULE`
- `THREEFOLD_REPETITION`
- `UNKNOWN`

#### Design Principles

- Single Responsibility Principle (SRP)
- Shared across all project modules
- No business logic
- No dependencies on other modules
- Used to avoid hard-coded string values

#### Dependencies

This package has **no dependencies**. It is the lowest dependency layer in the project architecture.

---

### ChessEngine

**File:** `modules/chess_engine/ChessEngine.py`

#### Overview

`ChessEngine` is the core chess logic module of the project. It acts as a wrapper around the **python-chess** library and is the only component in the project that communicates directly with it.

The engine is responsible for managing the chessboard, validating moves, executing moves, and providing board information. It contains no UI logic, game flow management, session handling, timers, or AI decision-making.

#### Responsibilities

- Initializing and resetting the chess board.
- Validating legal moves.
- Executing moves.
- Undoing moves.
- Tracking move history (SAN).
- Providing board information.
- Detecting special chess rules (castling, en passant, promotion).
- Detecting game-ending conditions (checkmate, stalemate, draw).
- Providing board snapshots via `BoardState`.

#### Not Responsible For

- User Interface / Streamlit components
- Game lifecycle
- Player management
- Session State
- AI logic
- Timers
- Move history presentation
- Captured pieces tracking

#### Public API

**Game Management:**
- `reset()`

**Move Validation:**
- `get_legal_moves()`
- `get_legal_targets()`
- `is_legal_move()`

**Move Execution:**
- `make_move()`
- `push_san()`
- `undo_last_move()`

**Board Queries:**
- `get_piece_at()`
- `get_piece_symbol_at()`
- `get_piece_type_at()`
- `get_piece_color_at()`
- `get_piece_map()`

**Game Status:**
- `is_check()`
- `is_checkmate()`
- `is_stalemate()`
- `is_insufficient_material()`
- `is_game_over()`
- `can_claim_draw()`
- `is_fifty_moves()`
- `is_repetition()`
- `result()`
- `outcome_reason()`
- `is_draw()`
- `is_pawn_promotion_move()`

**Board State:**
- `get_turn_color()`
- `get_fen()`
- `set_fen()`
- `get_board_state()`
- `get_board()`

**Move History:**
- `get_last_san()`
- `get_san_history()`
- `get_move_count()`

**Move Utilities:**
- `get_san()`

**Special Moves:**
- `is_castling_move()`
- `is_en_passant_move()`

**UCI Utilities:**
- `parse_uci()`
- `uci_to_from_square()`
- `uci_to_to_square()`
- `uci_get_promotion()`

**Board Utilities:**
- `get_last_move()`

#### Internal Design

Internally the engine stores:
- A `python-chess Board`
- SAN move history (`_san_history: List[str]`)

Move execution follows this sequence:

```
Validate Move → Generate SAN → Push Move → Update SAN History
```

#### Design Decisions

**Wrapper Pattern:** The project never imports `python-chess` outside this module. This isolates external dependencies and makes future replacements significantly easier.

**BoardState Model:** Instead of returning dictionaries, the engine returns a dedicated `BoardState` model for better type safety, IDE auto-completion, and cleaner architecture.

**GameEndReason Enum:** The engine converts `python-chess` termination values into project-specific enums, keeping the rest of the project independent from library enums.

**SAN History:** The engine stores SAN notation separately because `python-chess` stores only `Move` objects inside `move_stack`.

#### Architecture Position

```
UI → GameManager → ChessEngine → python-chess → Board
```

#### Dependencies

- **External:** `python-chess`
- **Internal:** `PlayerColor`, `GameEndReason`, `BoardState`

---

### StockfishEngine

**File:** `modules/bot/stockfish_engine.py`

#### Overview

The `StockfishEngine` module is responsible for all communication with the external **Stockfish** chess engine. It acts as a wrapper around the `stockfish` Python package, providing a clean and project-independent API for interacting with the chess engine.

The rest of the project never communicates with the Stockfish library directly.

#### Responsibilities

- Initializing the Stockfish engine.
- Managing the engine availability.
- Managing the bot difficulty level.
- Updating the current board position.
- Generating the best move.
- Evaluating chess positions.
- Resetting the engine state.

#### Not Responsible For

- Chess rules or move validation
- Game lifecycle
- Player turns
- Game history
- Timers
- UI logic
- Session management

#### Public API

- `set_difficulty(difficulty)` — updates bot difficulty and applies corresponding search depth.
- `set_fen(fen)` — updates the current board position inside Stockfish.
- `get_best_move(fen)` — returns the strongest move in UCI notation (or `None` if unavailable).
- `get_evaluation(fen)` — returns the engine evaluation dictionary.
- `is_available()` — returns whether the engine initialized successfully.
- `get_difficulty()` — returns the current difficulty level.
- `get_depth()` — returns the search depth associated with the current difficulty.
- `reset()` — restores the engine to the standard starting position.

#### Difficulty Mapping

| Difficulty | Depth |
|---|---|
| Easy | 3 |
| Medium | 10 |
| Hard | 18 |

#### Error Handling

Every engine interaction is wrapped in `try/except`. Unexpected failures never crash the application. Instead, the error is logged and methods safely return `None` or exit.

#### Fallback Mode

When Stockfish is unavailable, `get_best_move()` falls back to generating a random legal move using `python-chess`.

#### Design Decisions

- **Wrapper Pattern:** The project never exposes the Stockfish library outside this module, enabling loose coupling, easier testing, and cleaner architecture.
- **Single Responsibility Principle:** The class only manages communication with Stockfish, never game state, chess rules, UI, timers, or sessions.
- **Encapsulation:** The Stockfish instance is private; external modules interact only through public methods.
- **Guard Clauses:** Methods return early when the engine is unavailable, keeping code simple and avoiding unnecessary nesting.
- **DRY Principle:** Board updates are centralized in `set_fen()`; other methods reuse it instead of duplicating logic.

#### Architecture Position

```
UI → GameManager → StockfishEngine → Stockfish Library → Stockfish Executable
```

#### Dependencies

- **External:** `stockfish`, `logging`
- **Internal:** `Difficulty`, `stockfish_constants`

---

### Stockfish Installer

**File:** `modules/bot/stockfish_installer.py`

#### Overview

Automatically downloads and installs the correct Stockfish binary for the user's platform from the latest GitHub release.

#### Responsibilities

- Detecting the operating system (Windows, macOS, Linux) and architecture (x86, ARM).
- Selecting the optimal asset from the latest Stockfish GitHub release.
- Downloading and extracting archives (`.zip`, `.tar`, `.tar.gz`, `.tgz`, `.tar.xz`).
- Copying the binary to the project's `assets/stockfish/bin/<platform>/` directory.
- Setting executable permissions on Linux/macOS.
- Caching installation metadata to avoid repeated downloads.
- Finding and reusing project-local or legacy bundled binaries.

#### Flow

1. Check if binary already exists at `STOCKFISH_PATH`.
2. Look for a project-local binary in `assets/stockfish/`.
3. Look for a legacy bundled binary.
4. If none found, fetch the latest release from GitHub API.
5. Select the best matching asset for the current platform/architecture.
6. Download, extract, and copy the binary.
7. Save installation metadata to `installed_release.json`.

---

### GameState

**File:** `modules/game/game_state.py`

#### Overview

`GameState` represents the current state of a chess match. It acts as a **data container** and does not implement any game logic.

#### Fields

| Field | Type | Description |
|---|---|---|
| `game_mode` | `GameMode` | FRIEND or BOT |
| `status` | `GameStatus` | NOT_STARTED, RUNNING, or FINISHED |
| `difficulty` | `Optional[Difficulty]` | Bot difficulty (None for friend mode) |
| `board_state` | `Optional[BoardState]` | Snapshot of the board at the current state |
| `winner` | `Optional[PlayerColor]` | Winning player, if game has ended |
| `end_reason` | `Optional[GameEndReason]` | Reason the game ended |

#### Design Decisions

**Why DataClass?** `GameState` is implemented using Python's `@dataclass` because its primary responsibility is storing data rather than executing business logic. This provides cleaner code, automatic constructor generation, and better readability.

#### Responsibilities

- Storing the current game information.
- Providing a single source of truth for the match state.
- Sharing game data between different modules.

#### Not Responsible For

- Validating or executing chess moves.
- Managing the chess board.
- Detecting Check, Checkmate, or Stalemate.
- Controlling the game flow.
- Communicating with the Bot.
- Managing the user interface.

#### Dependencies

- `Shared Enums` only.
- Does **not** depend on ChessEngine, Bot, Session, or UI.
- One of the lowest dependency classes in the project.

#### Design Principles

- Single Responsibility Principle (SRP)
- Low Coupling
- High Readability
- Data-Oriented Design
- Separation of Concerns

---

### GameManager

**File:** `modules/game/game_manager.py`

#### Overview

The `GameManager` is the central controller of the chess application. It acts as the **orchestration layer** between ChessEngine, GameState, SessionManager, and the UI layer.

It does NOT implement chess rules itself, but delegates all rule logic to the ChessEngine.

#### Responsibilities

- Managing the lifecycle of a chess game (start, restart, end, load).
- Coordinating moves between UI and ChessEngine.
- Automatically triggering AI moves in BOT mode.
- Handling undo logic (undoing both bot and player moves in bot mode).
- Maintaining and updating GameState.
- Persisting state using SessionManager.
- Synchronizing game status (running, finished, winner, end reason).

#### Not Responsible For

- Implementing chess rules.
- Containing UI logic (Streamlit).
- Directly manipulating `st.session_state`.
- Defining game data structures.

#### Public API

**Game Lifecycle:**
- `start_game(game_mode, difficulty)` — resets engine, creates GameState, syncs session.
- `restart_game()` — restarts with the same mode and difficulty.
- `end_game(winner)` — marks game as finished, records winner.
- `load_game()` — restores the most recently saved game from session.

**Gameplay:**
- `make_move(from_square, to_square, promotion)` — executes a move (and bot response in BOT mode). Returns number of moves executed.
- `undo_last_move()` — undoes the last move(s). Returns success boolean.

**Engine Facade:**
- `get_board()`, `get_board_state()`, `get_turn()`, `get_move_history()`
- `get_result()`, `get_game_end_reason()`
- `is_game_over()`, `is_check()`, `is_checkmate()`, `is_stalemate()`, `is_draw()`

**Getters:**
- `get_game_state()` — returns the active GameState instance.

#### Move Flow (BOT Mode)

```
Player Move → GameManager.make_move()
    → ChessEngine.make_move() (player move)
    → _update_game_status()
    → StockfishEngine.get_best_move() (bot response)
    → ChessEngine.make_move() (bot move)
    → _sync_session()
```

#### Undo Flow (BOT Mode)

```
Undo → ChessEngine.undo_last_move() (undo bot)
     → ChessEngine.undo_last_move() (undo player)
     → _update_game_status()
     → _sync_session()
```

#### Architecture Position

```
UI (Streamlit) → GameManager → ChessEngine
                             → StockfishEngine
                             → GameState
                             → SessionManager
```

#### Dependencies

- ChessEngine, StockfishEngine, GameState, SessionManager
- All shared enums
- BoardState model

---

### CaptureManager

**File:** `modules/game/capture_manager.py`

#### Overview

Manages captured chess pieces for both players. Records captured piece symbols and provides query operations.

#### Public API

- `record_capture(captured_by, captured_piece_symbol)` — record a captured piece.
- `get_captured_by(player)` — returns a defensive copy of captured pieces for a player.
- `get_all_captured()` — returns captured pieces for both players.
- `get_capture_count(player)` — returns the number of pieces captured by a player.
- `get_total_captures()` — returns combined capture count.
- `clear()` — resets all recorded captures.

---

### HistoryManager

**File:** `modules/game/history_manager.py`

#### Overview

Manages the move history of a chess game with navigation support for moving forward and backward through recorded moves.

#### Public API

- `record_move(record)` — records a move, discarding future moves if not at the end.
- `undo_last()` — removes and returns the last recorded move.
- `get_history()` — returns a copy of all recorded moves.
- `get_last_move()` — returns the most recent move.
- `get_move_at(index)` — returns the move at a specific index.
- `get_move_count()` — returns the total number of recorded moves.
- `get_current_index()` — returns the current navigation position.
- `can_go_forward()` / `can_go_backward()` — navigation availability checks.
- `go_forward()` / `go_backward()` — navigate through history.
- `clear()` — resets the history.

---

### TimerManager

**File:** `modules/game/timer_manager.py`

#### Overview

Manages chess clocks for both players with configurable time controls.

#### Public API

**Time Control:**
- `set_time_control(initial_seconds, increment_seconds)`
- `get_initial_time()`, `get_increment()`

**Clock Controls:**
- `start(color)` — starts the clock for the specified player.
- `switch()` — switches the active clock to the opposing player (adds increment).
- `pause()` — pauses the active clock.
- `resume()` — resumes the active clock.
- `stop()` — stops the timer entirely.

**Queries:**
- `get_remaining_time(color)` — returns remaining time in seconds (accounts for active running time).
- `get_active_color()` — returns the player whose clock is active.
- `is_running()` — returns whether the timer is active.
- `is_time_up()` — returns the player whose time has expired, or None.

**Management:**
- `reset()` — resets both clocks to the configured initial time.

#### Implementation Details

- Uses `time.monotonic()` for accurate elapsed time measurement.
- Elapsed time is deducted from the active player's clock on switch, pause, and stop.
- Increment is added after each completed move during `switch()`.
- `get_remaining_time()` accounts for currently running time in real-time.

---

### BoardState

**File:** `modules/models/board_state.py`

#### Overview

A `@dataclass(slots=True)` representing the current state of the chess board.

#### Fields

| Field | Type | Description |
|---|---|---|
| `fen` | `str` | Board position in FEN notation |
| `turn` | `PlayerColor` | WHITE or BLACK |
| `move_count` | `int` | Number of moves played |
| `fullmove_number` | `int` | Fullmove counter (starts at 1, increments after Black's move) |

---

### MoveRecord

**File:** `modules/models/move_record.py`

#### Overview

A `@dataclass(slots=True)` representing a single move with full contextual metadata.

#### Fields

| Field | Type | Description |
|---|---|---|
| `move_number` | `int` | Sequential move number |
| `san` | `str` | Move in Standard Algebraic Notation |
| `from_square` | `int` | Source square index |
| `to_square` | `int` | Destination square index |
| `piece_symbol` | `str` | FEN symbol of the moved piece |
| `captured_piece_symbol` | `Optional[str]` | FEN symbol of captured piece (if any) |
| `is_check` | `bool` | Whether the move gives check |
| `is_checkmate` | `bool` | Whether the move delivers checkmate |
| `is_castling` | `bool` | Whether the move is a castle |
| `is_en_passant` | `bool` | Whether the move is en passant |
| `is_promotion` | `bool` | Whether the move is a promotion |
| `promotion_piece_symbol` | `Optional[str]` | Promoted piece symbol (if promotion) |

---

### SessionManager

**File:** `modules/session/session_manager.py`

#### Overview

The `SessionManager` module provides a clean and centralized wrapper around Streamlit's `st.session_state`. It decouples application logic from Streamlit, ensuring that the rest of the system does not directly depend on UI framework internals.

#### Responsibilities

- Storing values in session state.
- Retrieving stored values safely.
- Checking whether keys exist.
- Removing specific session entries.
- Clearing the entire session state.

#### Not Responsible For

- Game logic
- ChessEngine interaction
- UI rendering
- Business rules

#### Public API

- `set(key, value)` — store a value in the current session.
- `get(key, default=None)` — retrieve a value from the current session.
- `contains(key)` — check whether a session key exists.
- `remove(key)` — remove a value from the current session.
- `clear()` — clear the entire session state.

#### Why This Module Exists

Without SessionManager, Streamlit dependency would be scattered across the codebase, making session state hard to manage and creating tight coupling between UI and logic. With SessionManager, state management is centralized with clean separation of concerns.

#### Architecture Position

```
GameManager → SessionManager → st.session_state
```

#### Design Principles

- Single Responsibility Principle (SRP)
- Separation of Concerns (SoC)
- UI framework isolation (Streamlit abstraction)
- Clean Architecture principles

---

### Shared Constants

**Location:** `modules/shared/constants/`

#### Board Constants (`board_constants.py`)

| Constant | Value | Description |
|---|---|---|
| `BOARD_FILES_COUNT` | `8` | Number of files |
| `BOARD_RANKS_COUNT` | `8` | Number of ranks |
| `BOARD_SQUARE_COUNT` | `64` | Total squares |
| `FILE_NAMES` | `("a","b","c","d","e","f","g","h")` | File labels |
| `RANK_NAMES` | `("1","2","3","4","5","6","7","8")` | Rank labels |
| `STARTING_FEN` | `chess.STARTING_FEN` | Starting position FEN |
| `PROMOTION_PIECES` | `(QUEEN, ROOK, BISHOP, KNIGHT)` | Promotion choices |

#### Session Constants (`session_constants.py`)

| Constant | Value | Description |
|---|---|---|
| `GAME_STATE_SESSION_KEY` | `"game_state"` | Key for storing GameState in session |

#### Stockfish Constants (`stockfish_constants.py`)

| Constant | Description |
|---|---|
| `PROJECT_ROOT` | Project root directory (resolved from file location) |
| `STOCKFISH_ROOT` | `assets/stockfish/` |
| `STOCKFISH_BIN_DIR` | `assets/stockfish/bin/` |
| `PLATFORM_KEY` | `"windows"`, `"macos"`, or `"linux"` |
| `STOCKFISH_PATH` | Full path to the Stockfish executable |
| `DIFFICULTY_TO_DEPTH` | Mapping: `{EASY: 3, MEDIUM: 10, HARD: 18}` |

#### UI Constants (`ui_constants.py`)

| Constant | Value | Description |
|---|---|---|
| `PAGE_TITLE` | `"Chess Project"` | Browser tab title |
| `PAGE_ICON` | `"♟️"` | Browser tab icon |
| `PAGE_LAYOUT` | `"wide"` | Streamlit layout mode |

#### Display Helper (`modules/shared/helpers/display.py`)

- `format_label(value)` — converts enums and snake_case strings to user-facing titles (e.g., `"fifty_move_rule"` → `"Fifty Move Rule"`, `GameMode.BOT` → `"Bot"`).

---

### UI Screens

**Location:** `modules/ui/`

#### Home Screen (`home.py`)

Landing page with a full-screen background image. Features a "Begin Game" button positioned over an ornamental plaque and an EN/AR language toggle button in the top-right corner. Uses CSS injection for styling.

#### Mode Select (`mode_select.py`)

Mode selection screen with two buttons: "Human Challenger" (Friend mode) and "Strategic AI" (Bot mode). Selecting AI preloads the Stockfish engine in the background. Includes a "Back" button to return home.

#### Difficulty Selection (`difficulty.py`)

A Streamlit dialog popup for selecting AI difficulty (Easy / Medium / Hard) with visual highlighting of the selected option. Includes a Confirm button to proceed to the game.

#### Game Screen (`game.py`)

The main game screen containing:
- An 8×8 interactive chess board using Streamlit buttons.
- Visual move hints: dots for empty target squares, rings for capturable pieces.
- Chess clocks with live 1-second updates via `@st.fragment(run_every="1s")`.
- Turn indicator ("White to move" / "Black to move").
- Player name panels with captured piece display (computed from the board).
- Move history panel (scrollable, SAN notation, alternating white/black moves).
- Restart and End Game buttons.
- Check warning toast.
- Triggers promotion and result popups as needed.

**Clock:** Default is 10 minutes per side (`_TIME_CONTROL_SECONDS = 600`). Timeout detection automatically ends the game with the opponent winning on time.

**Move Handling:** Click a piece to select it, then click a valid destination to move. Invalid clicks deselect or select a different piece.

#### Promotion Popup (`promotion.py`)

A dialog popup for pawn promotion with four choices (Knight, Bishop, Rook, Queen) and a Confirm button. The default selection is Queen. The chosen piece is visually highlighted.

#### Result Popup (`result.py`)

A dialog popup displayed at game end showing the winner ("White Wins" / "Black Wins" / "Bot Wins") and the reason ("by Checkmate" / "on Time"). Offers "Play Again" and "Main Page" buttons. Uses a full-screen victory background image.

---

### Translations / i18n

**File:** `translations/i18n.py`

#### Overview

A lightweight translation module supporting English and Arabic.

#### API

- `t(key, language)` — looks up a key in the current language map, falling back to English.
- `normalize_language(language)` — normalizes language codes (`"ar"` → Arabic, everything else → English).

#### Translation Maps

Contains two dictionaries (`"en"` and `"ar"`) with keys covering all UI labels, buttons, messages, and game text. Arabic dictionary uses Arabic script for all labels.

---

## Architecture & Data Flow

### Overall Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Streamlit UI                        │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│  │Home  │ │Mode  │ │Diff  │ │Game  │ │Promo │ │Result│  │
│  │Screen│ │Select│ │Popup │ │Screen│ │Popup │ │Popup │  │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────┐
│                    GameManager                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │                GameState                         │  │
│  └──────────────────────────────────────────────────┘  │
└─────────┬──────────────────────┬───────────────────────┘
          │                      │
          ▼                      ▼
    ┌────────────┐    ┌─────────────────┐
    │ ChessEngine│    │ StockfishEngine │
    │            │    │                 │
    │python-chess│    │ stockfish lib   │
    └────────────┘    └─────────────────┘
          │
          ▼
   ┌──────────────┐
   │SessionManager│
   │              │
   │st.session_   │
   │state         │
   └──────────────┘
```

### Data Flow (Player Move)

```
1. Player clicks a piece → square selected in session_state
2. Player clicks destination → _handle_click() called
3. GameManager.make_move() called
4. ChessEngine.make_move() validates and executes the move
5. _update_game_status() checks for game-ending conditions
6. If BOT mode: StockfishEngine.get_best_move() → ChessEngine.make_move()
7. _sync_session() persists the updated GameState
8. Timer switches to the next player
9. UI rerenders with updated board, clocks, and history
```

### Dependency Hierarchy

```
UI Layer (depends on GameManager, i18n)
    │
GameManager (depends on ChessEngine, StockfishEngine, GameState, SessionManager)
    │
ChessEngine (depends on BoardState, enums)
StockfishEngine (depends on Difficulty, stockfish_constants)
GameState (depends on enums, BoardState)
SessionManager (depends on Streamlit)
    │
Shared Layer (constants, enums, helpers) — no dependencies on other modules
```

---

## Configuration

### Streamlit Theme (`.streamlit/config.toml`)

| Setting | Value | Description |
|---|---|---|
| `base` | `"dark"` | Dark theme |
| `primaryColor` | `#c9a24b` | Antique gold for buttons and highlights |
| `backgroundColor` | `#241a10` | Dark walnut page background |
| `secondaryBackgroundColor` | `#3a2a19` | Panel/card background |
| `textColor` | `#ecdfc8` | Parchment text color |
| `font` | `"serif"` | Serif font family |

### Difficulty Levels

| Level | Stockfish Search Depth |
|---|---|
| Easy | 3 |
| Medium | 10 |
| Hard | 18 |

### Time Control

Default: **10 minutes per side** with no increment. Change by modifying `_TIME_CONTROL_SECONDS` in `modules/ui/game.py`.

### Stockfish Binary

Automatic download location: `assets/stockfish/bin/<platform>/stockfish[.exe]`

Supported platforms: Windows, macOS (Intel & Apple Silicon), Linux (x86_64 & ARM)

---

## Design Principles

The project follows these architectural principles throughout:

- **Single Responsibility Principle (SRP):** Each class has one clearly defined responsibility.
- **Separation of Concerns:** Chess logic, game management, session handling, and UI are cleanly separated.
- **Wrapper Pattern:** External libraries (`python-chess`, `stockfish`) are wrapped behind project-specific interfaces.
- **Low Coupling:** Modules depend only on what they need; enums and models sit at the lowest dependency level.
- **High Cohesion:** Related functionality is grouped within the same module.
- **Data-Oriented Design:** Data containers (`GameState`, `BoardState`, `MoveRecord`) use `@dataclass` for clarity and simplicity.
- **Framework Isolation:** Streamlit-specific code is limited to `SessionManager` and the UI module.

---

## License

This project is provided for educational and personal use.

