#!/usr/bin/env python3

import subprocess


def select(prompt: str, options: list, rofi_args=[], fuzzy=True) -> tuple:
    """
    Allow the user to select an item from a list, via Rofi.

    Args:
        prompt (str): The prompt to display to the user.
        options (list): The list of options for the user to select from.
        rofi_args (list): Optional arguments to pass to Rofi directly.
            Default: [].
        fuzzy (bool): Allow the user to fuzzy search. Default: True.

    Returns:
        tuple:
            status code (int)
            index (int)
            selected (str)
    """

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

    return code, index, selected


def input(prompt: str, rofi_args=[]) -> tuple:
    """
    Get user input, via Rofi.

    Args:
    -----
        prompt (str): The prompt to display to the user.
        rofi_args (list): Optional arguments to pass to Rofi directly.

    Returns:
    --------
        tuple:
            status code (int)
            user input (str)
    """

    args = [
        "rofi",
        "-lines",
        "0",
        "-separator-style",
        "'none'",
    ]

    args += ["-dmenu", "-p", prompt]
    args += rofi_args

    args = [str(arg) for arg in args]

    result = subprocess.run(args, stdout=subprocess.PIPE,
                            universal_newlines=True)

    returncode = result.returncode

    if returncode == 0:
        code = 0
    if returncode == 1:
        code = -1
    if returncode > 9:
        code = returncode - 9

    return code, result.stdout.strip("\n")


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

    return code


def msg(msg: str, bold=True, italic=False, underline=False, err=False) -> None:
    """
    Display a message, via Rofi. The text provided will be colored red, if the
        message is an error. Else, the color will be green. The default styles
        are: Bold

    Args:
    -----
        msg (str): The string to display.
        bold (bool): String to be bold or not. Default: True.
        italic (bool): String to be italic or not. Default: False.
        underline (bool): String to be underlined or not. Default: False.
        err (bool): If the message is an error message or not. If it is, then
            the color of the text will be red. Else, green.
    """

    beginning = (
        f"{'<b>' if bold else ''}"
        + f"{'<i>' if italic else ''}"
        + f"{'<u>' if underline else ''}"
    )
    end = (
        f"{'</u>' if underline else ''}"
        + f"{'</i>' if italic else ''}"
        + f"{'</b>' if bold else ''}"
    )
    text = f"{beginning}{msg}{end}"

    display_text(
        f"<span color='{'red' if err else 'green'}'>{text}</span>")
