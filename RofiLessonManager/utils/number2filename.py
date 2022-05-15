"""
Function number2filename:
    - RofiLessonManager.utils.number2filename

    Converts the number (n) to the lecture file name.

    Args:
        - n (int): Lecture number.
    Returns:
        - str: Filename.
"""


def number2filename(n):
    """
    Converts the number (n) to the lecture file name.

    Args:
        - n (int): Lecture number.
    Returns:
        - str: Filename.
    """

    return 'lec-{}.tex'.format(n)
