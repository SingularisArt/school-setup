#!/usr/bin/env python3


def display_number(n: int) -> int:
    """
    If the number is less than 10, return the first digit.

    Args:
        n (int): A number

    Returns:
        int: The first digit if n is less than 10. Otherwise, just n

    Example:
        display_number(10): 10
        display_number(08):  8
        display_number(02):  2
        display_number(2):   2

    Raises:
        IndexError: If n < 10 and len(n) == 1, then n will be returned.
    """

    if int(n) < 10:
        try:
            return int(n[1])
        except IndexError:
            return int(n)
    else:
        return int(n)
