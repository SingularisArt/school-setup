#!/usr/bin/env python3

import subprocess


def select(prompt: str, options: list, rofi_args=[], fuzzy=True) -> tuple:
    optionstr = "\n".join(option.replace("\n", " ") for option in options)

    args = ["rofi", "-markup"]

    if fuzzy:
        args += ["-matching", "fuzzy"]

    args += ["-dmenu", "-p", prompt, "-format", "s", "-i"]
    args += rofi_args
    args = [str(arg) for arg in args]

    result = subprocess.run(
        args, input=optionstr, stdout=subprocess.PIPE, universal_newlines=True
    )

    returncode = result.returncode
    stdout = result.stdout.strip()

    selected = stdout.strip()

    try:
        index = [opt.strip() for opt in options].index(selected)
    except ValueError:
        index = -1

    if returncode == 0:
        code = 0
    if returncode == 1:
        code = -1
    if returncode > 9:
        code = returncode - 9
    else:
        code = -1

    return code, index, selected
