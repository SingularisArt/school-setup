#!/usr/bin/env python3


def filename_to_number(s: str) -> int:
    """
    Convert the file name number.

    Args:
        s (str): The file name.

    Returns:
        int: The number.

    Example:
        filename_to_number("lec-04.tex") -> 04
        filename_to_number("lec-04.yaml") -> 04
        filename_to_number("lec-04.pdf") -> 04
        filename_to_number("lec-04.bib") -> 04
        filename_to_number("lec-04.png") -> 04

        filename_to_number("week-04.tex") -> 04
        filename_to_number("week-04.yaml") -> 04
        filename_to_number("week-04.pdf") -> 04
        filename_to_number("week-04.bib") -> 04
        filename_to_number("week-04.png") -> 04
    """

    n = int(
        str(s)
        .replace("lec-", "")
        .replace("week-", "")
        .replace(".yaml", "")
        .replace(".tex", "")
        .replace(".pdf", "")
        .replace(".bib", "")
        .replace(".png", "")
    )
    if n < 10:
        return int(f"0{n}")
    return int(n)
