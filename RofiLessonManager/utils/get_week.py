#!/usr/bin/env python3


from datetime import datetime


def get_week(d=datetime.today()) -> int:
    """
    Get the week number of the year.

    Args:
    -----
        d (datetime): The date to get the week number of. Default:
            datetime.today()).

    Returns:
    --------
        int: The week number of the year.

    Example:
    --------
        get_week() -> 13
    """

    return (int(d.strftime("%W")) + 52 - 5) % 52
