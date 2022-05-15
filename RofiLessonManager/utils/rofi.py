#!/usr/bin/env python3

"""
Function rofi:
    - RofiLessonManager.utils.rofi

    Run rofi with the given prompt and options.

    Args:
        - prompt (str): The prompt to display.
        - options (list): A list of options to display.
        - rofi_args (list): A list of arguments to pass to rofi. (default: [])
        - fuzzy (bool): Whether to use fuzzy matching. (default: True)

    Returns:
        - key (int): The status code of the rofi process.
        - index (int): The index of the selected option.
        - selected (str): The selected option.
"""

import subprocess


def rofi(prompt, options, rofi_args=[], fuzzy=True):
    """
    Run rofi with the given prompt and options.

    Args:
        - prompt (str): The prompt to display.
        - options (list): A list of options to display.
        - rofi_args (list): A list of arguments to pass to rofi. (default: [])
        - fuzzy (bool): Whether to use fuzzy matching. (default: True)

    Returns:
        - key (int): The status code of the rofi process.
        - index (int): The index of the selected option.
        - selected (str): The selected option.
    """

    optionstr = '\n'.join(option.replace('\n', ' ') for option in options)

    args = ['rofi', '-sort', '-no-levenshtein-sort']

    if fuzzy:
        args += ['-matching', 'fuzzy']

    args += ['-dmenu', '-p', prompt, '-format', 's', '-i']
    args += rofi_args
    args = [str(arg) for arg in args]

    result = subprocess.run(args, input=optionstr,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    returncode = result.returncode
    stdout = result.stdout.strip()

    selected = stdout.strip()

    try:
        index = [opt.strip() for opt in options].index(selected)
    except ValueError:
        index = -1

    if returncode == 0:
        key = 0
    if returncode == 1:
        key = -1
    if returncode > 9:
        key = returncode - 9

    return key, index, selected
