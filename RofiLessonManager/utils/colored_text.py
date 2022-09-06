#!/usr/bin/env python3.10


def colored_text(text: str, color="#999999") -> str:
    """
    Return colored text for polybar.

    Args:
        text (str): Text to be colored.
        color (str): Hex color code.

    Returns:
        str: Colored text.

    Example:
        colored_text("hello", "101010") -> "%{F101010}hello%{F-}"
    """

    return "%{F" + color + "}" + text + "%{F-}"
