#!/usr/bin/env python3

"""
Function get_week:
    - RofiLessonManager.utils.get_week

    Get the week number of the year.

    Args:
        - d (datetime): The date to get the week number of
            (default is: datetime.today()).

    Returns:
        - int: The week number of the year.
"""

from datetime import datetime


def get_week(d=datetime.today()):
    """
    Get the week number of the year.

    Args:
        - d (datetime): The date to get the week number of
            (default is: datetime.today()).

    Returns:
        - int: The week number of the year.
    """
    return (int(d.strftime('%W')) + 52 - 5) % 52
