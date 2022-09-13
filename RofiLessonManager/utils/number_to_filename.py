#!/usr/bin/env python3


def number_to_filename(n: int) -> str:
    """
    Converts the number (n) to the lecture file name. If the number is less
    than 10, then 0 will be added in front of n.

    Args:
    -----
        n (int): Lecture number.

    Returns:
    --------
        str: Filename.

    Example:
    --------
        number_to_filename(3) -> lec-03.tex
        number_to_filename(14) -> lec-14.tex
    """

    if n < 10:
        n = f"0{n}"
    else:
        n = n

    return f"lec-{n}.tex"
