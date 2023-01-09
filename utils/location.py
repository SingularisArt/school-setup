#!/usr/bin/env python3

import utils


def location(text: str) -> str:
    if not text:
        return ""

    return f"{utils.colored_text('in')} {text}"
