"""
Function location:
    - RofiLessonManager.utils.location

    Return the location of the class.

    Args:
        - text (str): The text to search for.

    Returns:
        - str: The location of the class.
"""

import RofiLessonManager.utils as utils


def location(text):
    """
    Return the location of the class.

    Args:
        - text (str): The text to search for.

    Returns:
        - str: The location of the class.
    """

    if not text:
        return ''

    return '{} {}'.format(utils.colored_text("in"), text)
