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

---

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