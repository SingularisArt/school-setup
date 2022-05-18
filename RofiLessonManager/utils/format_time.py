"""
Function format_time:
    - RofiLessonManager.utils.format_time

    Returns a formatted time string from a time object.

    Args:
        - time (datetime.time): The time object to format.
        - format (str): The format to use. (default: '%H:%M')

    Returns:
        - str: The formatted time string.
"""


def format_time(time, format='%I:%M %p'):
    """
    Returns a formatted time string from a time object.

    Args:
        - time (datetime.time): The time object to format.
        - format (str): The format to use. (default: '%I:%M %p')

    Returns:
        - str: The formatted time string.
    """

    return time.strftime(format)
