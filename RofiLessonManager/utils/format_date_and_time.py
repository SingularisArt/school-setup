#!/usr/bin/env python3


import math


def format_date_and_time(begin, end):
    """
    Return the time between the beginning and end in a human readable format.

    Args:
        begin (datetime): The beginning of the time.
        end (datetime): The end of the time.

    Returns:
        str: The time between the beginning and end.
    """

    minutes = math.ceil((end - begin).seconds / 60)

    if minutes == 1:
        return "1 minute"

    if minutes < 60:
        return f"{minutes} minutes"

    hours = math.floor(minutes / 60)
    rest_minutes = minutes % 60

    if hours == 1 and rest_minutes == 0:
        return "1 hour"
    elif hours == 1:
        return f"1 hour and {rest_minutes} minutes"
    elif hours > 5 or rest_minutes == 0:
        return f"{hours} hours"

    return f"{hours} hours {rest_minutes:02d} minutes"
