"""
Function formatdd:
    - RofiLessonManager.utils.formatdd

    Return the time between the beginning and end.

    Args:
        - begin (datetime): The beginning of the time.
        - end (datetime): The end of the time.

    Returns:
        - str: The time between the beginning and end.
"""

import math


def formatdd(begin, end):
    """
    Return the time between the beginning and end.

    Args:
        - begin (datetime): The beginning of the time.
        - end (datetime): The end of the time.

    Returns:
        - str: The time between the beginning and end.
    """

    minutes = math.ceil((end - begin).seconds / 60)

    if minutes == 1:
        return '1 minute'

    if minutes < 60:
        return '{} minutes'.format(minutes)

    hours = math.floor(minutes/60)
    rest_minutes = minutes % 60

    if hours == 1 and rest_minutes == 0:
        return '1 hour'
    elif hours == 1:
        return '1 hour and {} minutes'.format(rest_minutes)
    elif hours > 5 or rest_minutes == 0:
        return '{} hours'.format(hours)

    return '{} hours {:02d} minutes'.format(hours, rest_minutes)
