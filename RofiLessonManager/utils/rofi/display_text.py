#!/usr/bin/env python3

import subprocess


def display_text(prompt: str, rofi_args=[]) -> tuple:
    """
    Display text to the user, via Rofi.

    Args:
    -----
        prompt (str): The prompt to display to the user.
        rofi_args (list): Optional arguments to pass to Rofi directly.

    Returns:
    --------
        status code (int)
    """

    args = ["rofi", "-markup"]

    args += ["-e", prompt]
    args += rofi_args
    args = [str(arg) for arg in args]

    result = subprocess.run(
        args, input=prompt, stdout=subprocess.PIPE, universal_newlines=True
    )

    returncode = result.returncode

    if returncode == 0:
        code = 0
    if returncode == 1:
        code = -1
    if returncode > 9:
        code = returncode - 9
    else:
        code = -1

    return code
