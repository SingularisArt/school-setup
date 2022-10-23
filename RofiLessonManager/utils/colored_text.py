#!/usr/bin/env python3.10


def colored_text(text: str, color="#999999") -> str:
    return "%{F" + color + "}" + text + "%{F-}"
