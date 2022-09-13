#!/usr/bin/env python3


def join(*args, separator=" ") -> str:
    """
    Joins a list of strings with a given separator.

    Args:
    -----
        *args: list of strings.
        separator (str): The separator you wish to use. Default: " ".

    Returns:
    --------
        str: Joined string.

    Example:
    --------
        join(["h", "e", "l", "l", "o"]) = hello.
        join(["h", "e", "l", "l", "o"], "/") = h/e/l/l/o.
    """

    return separator.join(str(e) for e in args if e)
