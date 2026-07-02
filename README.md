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