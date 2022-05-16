"""
Function join:
    - RofiLessonManager.utils.join

    Joins a list of strings with a given separator.

    Args:
        - *args: list of strings

    Returns:
        - joined string
"""


def join(*args):
    """
    Joins a list of strings with a given separator.

    Args:
        - *args: list of strings

    Returns:
        - joined string
    """

    return ' '.join(str(e) for e in args if e)
