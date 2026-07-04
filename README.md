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


