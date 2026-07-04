# chess-project-



# Shared Enums

## Overview

The `enums` package contains all shared enumerations used throughout the project.

Its purpose is to centralize all fixed values in one place, making the code more readable, maintainable, and less prone to errors caused by hard-coded strings.

---

## Enums

### Difficulty

Represents the available bot difficulty levels.

Values:
- EASY
- MEDIUM
- HARD

---

### GameMode

Represents the available game modes.

Values:
- FRIEND
- BOT

--------------------------
--------------------------

### GameStatus

Represents the lifecycle state of the current game.

Values:
- NOT_STARTED
- RUNNING
- FINISHED

> Note:
> Chess conditions such as Check, Checkmate, Stalemate, and Draw are **not** part of this enum.
> These are handled by the Chess Engine module.

---

### PlayerColor

Represents the two player colors in chess.

Values:
- WHITE
- BLACK

---

## Design Principles

- Single Responsibility Principle (SRP)
- Shared across all project modules
- No business logic
- No dependencies on other modules
- Used to avoid hard-coded string values

---

## Dependencies

This package has **no dependencies**.

It is the lowest dependency layer in the project architecture.

----------------------------------
----------------------------


# Game Module

## Overview

The `game` module is responsible for managing the overall state of a chess match.

At this stage, the module contains the `GameState` class, which represents the current state of the game by storing all required game-related information.

Game logic such as move validation, check detection, and board manipulation is **not** handled here. These responsibilities belong to the Chess Engine module.

---

## Components

### GameState

Represents the current state of an active chess game.

It stores:

- Game mode (Friend / Bot)
- Game status
- Current player's turn
- Bot difficulty (if applicable)
- Winner (if the game has ended)

The `GameState` class acts as a **data container** and does not implement any game logic.

---

## Design Decisions

### Why DataClass?

`GameState` is implemented using Python's `@dataclass` because its primary responsibility is storing data rather than executing business logic.

Using a dataclass provides:

- Cleaner code
- Automatic constructor generation
- Better readability
- Easier maintenance

---

## Responsibilities

The GameState class is responsible for:

- Storing the current game information.
- Providing a single source of truth for the match state.
- Sharing game data between different modules.

---

## Not Responsible For

The GameState class does **not**:

- Validate chess moves.
- Manage the chess board.
- Detect Check or Checkmate.
- Control the game flow.
- Communicate with the Bot.

These responsibilities belong to other modules in the project.

---

## Dependencies

GameState depends only on:

- Shared Enums

It does not depend on:

- Chess Engine
- Bot
- Session
- UI

This makes it one of the lowest dependency classes in the project architecture.

---

## Design Principles

- Single Responsibility Principle (SRP)
- Low Coupling
- High Readability
- Data-Oriented Design
- Separation of Concerns

------------------------
-------------------------


# Game Module

## Overview

The `game` module is responsible for managing the overall state of a chess match.

Currently, this module contains the `GameState` class, which represents the current state of the game by storing all required game-related information.

Game logic such as move validation, move execution, check detection, and board manipulation is **not** handled here. These responsibilities belong to the Chess Engine module.

---

## Components

### GameState

Represents the current state of a chess match.

It stores:

- Game mode (Friend / Bot)
- Game status
- Current player's turn
- Bot difficulty (if applicable)
- Winner (if the game has ended)

`GameState` acts as a **data container** and does not implement any game logic.

---

## Design Decisions

### Why DataClass?

`GameState` is implemented using Python's `@dataclass` because its primary responsibility is storing data rather than executing business logic.

Using a dataclass provides:

- Cleaner code
- Automatic constructor generation
- Better readability
- Easier maintenance

---

## Responsibilities

The `GameState` class is responsible for:

- Storing the current game information.
- Providing a single source of truth for the match state.
- Sharing game data between different modules.

---

## Not Responsible For

The `GameState` class does **not**:

- Validate chess moves.
- Execute chess moves.
- Manage the chess board.
- Detect Check, Checkmate, or Stalemate.
- Control the game flow.
- Communicate with the Bot.
- Manage the user interface.

These responsibilities belong to other modules in the project.

---

## Dependencies

`GameState` depends only on:

- Shared Enums

It does **not** depend on:

- Chess Engine
- Bot
- Session
- UI

This makes it one of the lowest dependency classes in the project architecture and allows it to be safely reused by higher-level modules without introducing unnecessary coupling.

---

## Design Principles

- Single Responsibility Principle (SRP)
- Low Coupling
- High Readability
- Data-Oriented Design
- Separation of Concerns

---

## Future Extensions

As the project grows, additional classes such as `GameManager` will be added to this module.

`GameState` will remain responsible only for storing the current match data, while all game management logic will be implemented in dedicated classes.


---------------------------
-----------------------------


# ChessEngine

## Overview

`ChessEngine` is the core chess logic module of the project.

It acts as a wrapper around the **python-chess** library and is the only component in the project that communicates directly with it.

The engine is responsible for managing the chessboard, validating moves, executing moves, and providing board information.

It does **not** contain any UI logic, game flow management, session handling, timers, or AI decision-making.

---

# Responsibilities

The ChessEngine is responsible for:

- Initializing and resetting the chess board.
- Validating legal moves.
- Executing moves.
- Undoing moves.
- Tracking move history (SAN).
- Providing board information.
- Detecting special chess rules.
- Detecting game-ending conditions.
- Providing board snapshots.

---

# Not Responsible For

The ChessEngine intentionally does **not** handle:

- User Interface
- Streamlit components
- Game lifecycle
- Player management
- Session State
- AI logic
- Timers
- Move history presentation
- Captured pieces

Those responsibilities belong to other modules.

---

# Architecture

```
                UI
                 │
                 ▼
          GameManager
                 │
                 ▼
           ChessEngine
                 │
                 ▼
          python-chess
```

Only `ChessEngine` communicates with the external chess library.

This keeps the rest of the project independent from third-party APIs.

---

# Public API

## Game Management

- `reset()`

---

## Move Validation

- `get_legal_moves()`
- `get_legal_targets()`
- `is_legal_move()`

---

## Move Execution

- `make_move()`

---

## Board Queries

- `get_piece_at()`
- `get_piece_symbol_at()`
- `get_piece_type_at()`
- `get_piece_color_at()`
- `get_piece_map()`

---

## Game Status

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
- `is_pawn_promotion_move()`

---

## Board State

- `get_turn_color()`
- `get_fen()`
- `set_fen()`
- `get_board_state()`

---

## Move History

- `get_last_san()`
- `get_san_history()`

---

## Move Utilities

- `get_san()`
- `push_san()`
- `undo_last_move()`

---

## Special Moves

- `is_castling_move()`
- `is_en_passant_move()`

---

## UCI Utilities

- `parse_uci()`
- `uci_to_from_square()`
- `uci_to_to_square()`
- `uci_get_promotion()`

---

## Board Utilities

- `get_last_move()`

---

# Internal Design

Internally the engine stores:

- A `python-chess Board`
- SAN move history
- Board state information

Move execution always follows this sequence:

```
Validate Move
      │
      ▼
Generate SAN
      │
      ▼
Push Move
      │
      ▼
Update SAN History
```

---

# Design Decisions

## Wrapper Pattern

The project never imports `python-chess` outside this module.

This isolates external dependencies and makes future replacements significantly easier.

---

## BoardState Model

Instead of returning dictionaries, the engine returns a dedicated `BoardState` model.

Advantages:

- Better type safety
- Easier maintenance
- Cleaner APIs
- IDE auto-completion
- Clear project architecture

---

## GameEndReason Enum

The engine converts `python-chess` termination values into project-specific enums.

Advantages:

- Removes dependency on library enums.
- Keeps the rest of the project independent.
- Makes future engine replacement easier.

---

## SAN History

The engine stores SAN notation separately because `python-chess` stores only `Move` objects inside `move_stack`.

---

# Data Flow

```
UI

↓

GameManager

↓

ChessEngine

↓

python-chess

↓

Board
```

---

# Dependencies

External:

- python-chess

Internal:

- PlayerColor
- GameEndReason
- BoardState

---

# Usage Example

```python
engine = ChessEngine()

engine.make_move(
    chess.E2,
    chess.E4,
)

print(engine.get_turn_color())

print(engine.get_board_state())

print(engine.is_check())
```

---

# Future Extensions

The current design allows adding:

- PGN Export
- PGN Import
- Board Evaluation
- Move Analysis
- Opening Detection
- Move Suggestions
- Chess960 Support

without changing the public API.

---

# Notes

The ChessEngine is designed according to the following principles:

- Single Responsibility Principle (SRP)
- Separation of Concerns
- Wrapper Pattern
- Small Public API
- High Cohesion
- Low Coupling

The engine should remain focused exclusively on chess logic.

All higher-level application logic should be implemented in `GameManager`.



-----------------------
----------------------

# Stockfish Engine Module

## Overview

The `StockfishEngine` module is responsible for all communication with the external **Stockfish** chess engine.

It acts as a wrapper around the `stockfish` Python package, providing a clean and project-independent API for interacting with the chess engine.

The rest of the project never communicates with the Stockfish library directly.

---

# Responsibilities

The `StockfishEngine` is responsible for:

- Initializing the Stockfish engine.
- Managing the engine availability.
- Managing the bot difficulty level.
- Updating the current board position.
- Generating the best move.
- Evaluating chess positions.
- Resetting the engine state.

---

# Out of Scope

This module **does NOT** handle:

- Chess rules.
- Move validation.
- Game lifecycle.
- Player turns.
- Game history.
- Timers.
- UI logic.
- Session management.

Those responsibilities belong to other modules.

---

# Architecture

```
                GameManager
                     │
                     ▼
             StockfishEngine
                     │
                     ▼
              Stockfish Library
                     │
                     ▼
             Stockfish Executable
```

Only `StockfishEngine` communicates with the external Stockfish engine.

---

# Project Position

```
UI
 │
 ▼
GameManager
 ├───────────────┐
 │               │
 ▼               ▼
ChessEngine   StockfishEngine
```

The GameManager requests moves from the bot.

The bot never communicates directly with the UI.

---

# Dependencies

- stockfish
- logging
- typing

Project modules:

- Difficulty
- stockfish_constants

---

# Public API

## Engine Configuration

### set_difficulty()

Updates the bot difficulty and applies the corresponding search depth to the engine.

---

## Position Management

### set_fen()

Updates the current board position inside Stockfish using a FEN string.

---

## Move Generation

### get_best_move()

Returns the strongest move for the given board position.

Returned value:

- UCI move string
- or None if unavailable.

Example:

```
e2e4
```

---

### get_evaluation()

Returns the engine evaluation.

Typical result:

```python
{
    "type": "cp",
    "value": 34
}
```

or

```python
{
    "type": "mate",
    "value": -2
}
```

---

## Engine Status

### is_available()

Returns whether the engine initialized successfully.

---

### get_difficulty()

Returns the current difficulty level.

---

### get_depth()

Returns the search depth associated with the current difficulty.

---

## Engine Management

### reset()

Restores the engine to the standard chess starting position.

---

# Internal API

## _init_engine()

Initializes the Stockfish engine.

This method is private and should never be called outside the class.

---

# Difficulty Mapping

Difficulty levels are mapped to Stockfish search depth using:

```
DIFFICULTY_TO_DEPTH
```

Example:

| Difficulty | Depth |
|------------|------:|
| Easy | 5 |
| Medium | 10 |
| Hard | 18 |

The mapping is defined in:

```
modules/shared/constants/stockfish_constants.py
```

---

# Error Handling

Every engine interaction is wrapped in:

```
try / except
```

Unexpected failures never crash the application.

Instead:

- the error is logged,
- the engine remains usable,
- methods safely return `None` or exit.

---

# Design Decisions

## Wrapper Pattern

The project never exposes the Stockfish library outside this module.

Advantages:

- loose coupling
- easier testing
- easier replacement
- cleaner architecture

---

## Single Responsibility Principle

The class only manages communication with Stockfish.

It never manages:

- game state
- chess rules
- UI
- timers
- sessions

---

## Encapsulation

The Stockfish instance is private.

External modules interact only through public methods.

---

## Guard Clauses

Methods return early when the engine is unavailable.

Example:

```python
if not self._available or self._engine is None:
    return
```

This keeps the code simple and avoids unnecessary nesting.

---

## DRY Principle

Board updates are centralized in:

```
set_fen()
```

Other methods reuse it instead of duplicating logic.

---

# Typical Flow

```
GameManager

      │

      ▼

get_fen()

      │

      ▼

StockfishEngine.set_fen()

      │

      ▼

StockfishEngine.get_best_move()

      │

      ▼

UCI Move

      │

      ▼

ChessEngine.make_move()
```

---

# Notes

- This module assumes all incoming FEN strings are valid.
- FEN validation is the responsibility of `ChessEngine`.
- The engine does not store game history.
- The engine does not own the board state.
- The engine only evaluates positions and generates moves.

---

# Future Extensions

Possible future improvements include:

- MultiPV support.
- Move ordering.
- Engine hash configuration.
- Thread configuration.
- Skill level support.
- Engine benchmarking.
- Move analysis mode.

The current architecture allows these features to be added without modifying the rest of the project.

---

# Summary

The `StockfishEngine` module provides a clean abstraction over the Stockfish engine.

It isolates all engine-specific functionality behind a stable API, allowing the rest of the project to remain independent from the underlying chess engine implementation.

This design improves maintainability, readability, extensibility, and long-term project scalability.


-----------------------------
----------------------------


#  Session Manager Module

##  Overview

The `SessionManager` module provides a clean and centralized wrapper around Streamlit's `st.session_state`.

It decouples application logic from Streamlit, ensuring that the rest of the system does not directly depend on UI framework internals.

This improves:
- Maintainability
- Testability
- Code clarity
- Architecture separation
- Scalability

---

## 🎯 Responsibility

The SessionManager is responsible for **session state management only**, including:

- Storing values in session state
- Retrieving stored values safely
- Checking whether keys exist
- Removing specific session entries
- Clearing the entire session state

---

## ❌ What this module does NOT do

- Does NOT contain any game logic
- Does NOT interact with ChessEngine
- Does NOT handle UI rendering
- Does NOT manage business rules

---

##  Architecture Role

The SessionManager acts as the lowest persistence layer in the system.


UI (Streamlit)
↓
GameManager
↓
SessionManager
↓
st.session_state


---

##  Data Flow


GameManager updates state
↓
SessionManager stores state
↓
Streamlit reruns script
↓
UI reflects updated game status


---

##  Why this module exists

Without SessionManager:
- Streamlit dependency would be scattered across the codebase ❌
- Session state becomes hard to manage ❌
- Tight coupling between UI and logic ❌

With SessionManager:
- Centralized state management ✔
- Clean separation of concerns ✔
- Easier debugging and testing ✔
- More scalable architecture ✔

---

##  Design Principles

- Single Responsibility Principle (SRP)
- Separation of Concerns (SoC)
- UI framework isolation (Streamlit abstraction)
- Clean Architecture principles

---

## ✅ Summary

SessionManager is a lightweight abstraction over Streamlit session state that ensures a  clean, scalable, and maintainable architecture for the Chess Project.
 
-----------------------------
-----------------------------

# ♟️ Game Manager Module

##  Overview

The `GameManager` is the central controller of the chess application.

It acts as the **orchestration layer** between:

- ChessEngine (game rules & logic)
- GameState (data model)
- SessionManager (state persistence)
- UI layer (Streamlit)

It does NOT implement chess rules itself, but delegates all rule logic to the ChessEngine.

---

##  Responsibility

The GameManager is responsible for:

- Managing the lifecycle of a chess game
- Coordinating moves between UI and ChessEngine
- Maintaining and updating GameState
- Persisting state using SessionManager
- Synchronizing game status (running, finished, winner, etc.)

---

## ❌ What this module does NOT do

- Does NOT implement chess rules
- Does NOT contain UI logic (Streamlit)
- Does NOT directly manipulate session_state
- Does NOT define game data structures
- Does NOT replace ChessEngine responsibilities

---

##  Architecture Role

The GameManager acts as the **central controller** of the system:


UI (Streamlit)
↓
GameManager
↓
ChessEngine
↓
GameState
↓
SessionManager


---

## 🔄 Game Flow

The following diagram describes how a move flows through the system:


Player Action
↓
GameManager
↓
ChessEngine
↓
GameState Update
↓
SessionManager Save
↓
UI Refresh


This flow guarantees:
- Centralized control of game logic
- Consistent state updates
- Persistent session storage
- Clean separation between UI and backend logic

---

#  Summary

This architecture ensures a clean separation of concerns:

- SessionManager → handles persistence
- GameManager → controls game flow
- ChessEngine → handles chess rules
- GameState → stores game data
- UI (Streamlit) → presentation layer

The result is a scalable, maintainable, and modular chess application architecture.