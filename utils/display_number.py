#!/usr/bin/env python3


def display_number(n: int) -> int:
    if int(n) < 10 and len(n) == 2:
        return int(n[1])
    else:
        return int(n)
