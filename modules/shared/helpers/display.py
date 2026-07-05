from enum import Enum


def format_label(value: Enum | str | None) -> str:
    """
    Convert enums and identifier-like strings into user-facing labels.

    Examples:
        GameMode.BOT -> "Bot"
        "fifty_move_rule" -> "Fifty Move Rule"
    """

    if value is None:
        return ""

    if isinstance(value, Enum):
        value = value.value

    return str(value).replace("_", " ").title()