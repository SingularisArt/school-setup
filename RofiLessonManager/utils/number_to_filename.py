#!/usr/bin/env python3


def number_to_filename(n: int) -> str:
    if n < 10:
        n = f"0{n}"
    else:
        n = n

    return f"lec-{n}.tex"
