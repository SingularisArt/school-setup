#!/usr/bin/env python3


def generate_short_title(title: str, MAX_LENGTH=34) -> str:
    ellipsis = " ..."
    if len(title) < MAX_LENGTH:
        return title

    return title[: MAX_LENGTH - len(ellipsis)] + ellipsis
