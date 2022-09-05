#!/usr/bin/env python3

"""
Function generate_short_title:
    Shorten a title of too long in length.

    Args:
        title (str): The title to shorten.
        MAX_LENGTH (int): The maximum length of the title. Default: 34.

    Returns:
        str: The shortened title.

    Example:
        generate_short_title(
            "This string is too long. I need to cut it down."
        ): This string is too long. I nee ...
"""


def generate_short_title(title, MAX_LENGTH=34):
    """
    Shorten a title of too long in length.

    Args:
        title (str): The title to shorten.
        MAX_LENGTH (int): The maximum length of the title. Default: 34.

    Returns:
        str: The shortened title.

    Example:
        generate_short_title(
            "This string is too long. I need to cut it down."
        ): This string is too long. I nee ...
    """

    ellipsis = " ..."
    if len(title) < MAX_LENGTH:
        return title

    return title[: MAX_LENGTH - len(ellipsis)] + ellipsis
