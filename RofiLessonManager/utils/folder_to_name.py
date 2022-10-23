#!/usr/bin/env python3


def folder_to_name(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()
