#!/usr/bin/env python3

import subprocess


def select(prompt, options, rofi_args=[], fuzzy=True):
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


def display_text(prompt, rofi_args=[]):
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


def input(prompt, rofi_args=[]):
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


def error_message(msg):
    display_text("<span color='red'><b>{}</b></span>".format(msg))


def success_message(msg):
    display_text("<span color='green'><b>{}</b></span>".format(msg))
