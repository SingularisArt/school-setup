#!/usr/bin/env python3

"""
Function filename2number:
    - RofiLessonManager.utils.filename2number

    Converts the file-name (s) to the lecture number.

    Args:
        - s (str): Filename.

    Returns:
        - int: Lecture number.
"""


def filename2number(s):
    """
    Converts the file-name (s) to the lecture number.

    Args:
        - s (str): Filename.

    Returns:
        - int: Lecture number.
    """

    return str(s).replace('lec-', '').replace('.tex', '')
