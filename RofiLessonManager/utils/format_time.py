#!/usr/bin/env python3


def format_time(time, format="%I:%M %p"):
    """
    Returns a formatted time string from a time object.

    Args:
        time (datetime.time): The time object to format.
        format (str): The format to use. Default: %I:%M %p.

    Returns:
        str: The formatted time string.
    """

    return time.strftime(format)
