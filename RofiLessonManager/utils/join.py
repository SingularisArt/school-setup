#!/usr/bin/env python3


def join(*args, separator=" ") -> str:
    return separator.join(str(e) for e in args if e)
