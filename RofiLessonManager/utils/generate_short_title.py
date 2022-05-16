#!/usr/bin/env python3

"""
Function generate_short_title:
    - RofiLessonManager.utils.generate_short_title

    Shorten a title of too long in length.

    Args:
        - title (str): The title to shorten.
        - MAX_LENGTH (int): The maximum length of the title. (Default: 36)

    Returns:
        - str: The shortened title.
"""


def generate_short_title(title, MAX_LENGTH=36):
    """
    Shorten a title of too long in length.

    Args:
        - title (str): The title to shorten.
        - MAX_LENGTH (int): The maximum length of the title. (Default: 36)

    Returns:
        - str: The shortened title.
    """

    ellipsis = ' ...'
    if len(title) < MAX_LENGTH:
        return title
    return title[:MAX_LENGTH - len(ellipsis)] + ellipsis
