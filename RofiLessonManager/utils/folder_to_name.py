#!/usr/bin/env python3


def folder_to_name(name: str) -> str:
    """
    Convert the folder name to the course name.

    Args:
    -----
        name (str): The folder name.

    Returns:
    --------
        str: The course name.

    Example:
    --------
        folder_to_name("hello-world") -> Hello World
        folder_to_name("hello_world") -> Hello World
    """

    return name.replace("-", " ").replace("_", " ").title()
