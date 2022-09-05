#!/usr/bin/env python3

"""
Function location:
    Get the location of the class.

    Args:
        text (str): The text to search for.

    Returns:
        str: If text is empty, an emptry string will be returned. Else, the
            location of the class.

    Example:
        location("TCB 208") -> %{F999999}in%{F-} TCB 208.
        location("") -> ""
"""

import RofiLessonManager.utils as utils


def location(text: str) -> str:
    """
    Get the location of the class.

    Args:
        text (str): The text to search for.

    Returns:
        str: If text is empty, an emptry string will be returned. Else, the
            location of the class.

    Example:
        location("TCB 208") -> %{F999999}in%{F-} TCB 208.
        location("") -> ""
    """

    if not text:
        return ""

    return f"{utils.colored_text('in')} {text}"
