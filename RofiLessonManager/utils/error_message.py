#!/usr/bin/env python3

"""
Function error_message:
    - RofiLessonManager.utils.error_message

    Displays an error message in red and bold.

    Args:
        - message (str): The message to display.
"""

from rofi import Rofi


def error_message(message):
    """
    Displays an error message in red and bold.

    Args:
        - message (str): The message to display.
    """

    rofi = Rofi()
    rofi.error('<span color="red"><b>{}</b></span>'.format(message),
               ['-markup'])
