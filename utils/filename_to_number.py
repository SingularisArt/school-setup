#!/usr/bin/env python3

import utils


def filename_to_number(s: str) -> str:
    n = utils.replace_str(
        s,
        ["lec-", ""],
        ["week-", ""],
        [".yaml", ""],
        [".tex", ""],
        [".pdf", ""],
        [".bib", ""],
        [".png", ""],
    )

    if int(n) < 10 and len(str(n)) == 1:
        return str(f"0{n}")
    return str(n)
