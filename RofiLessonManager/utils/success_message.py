#!/usr/bin/env python3

"""
Function success_message:
    - RofiLessonManager.utils.success_message

    Displays an error message in red and bold.

    Args:
        - message (str): The message to display.
        - rofi (object): The rofi object from the rofi.Rofi.
"""

from rofi import Rofi


def success_message(message):
    """
    Displays an error message in red and bold.

    Args:
        - message (str): The message to display.
        - rofi (object): The rofi object from the rofi.Rofi.
    """

    rofi = Rofi()
    rofi.error('<span color="green"><b>{}</b></span>'.format(message),
               ['-markup'])
