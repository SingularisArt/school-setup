"""
Function get_color_from_id:
    - RofiLessonManager.utils.get_color_from_id

    Get color from id and text to colorize.

    Args:
        - id (int): color id (default: None)
        - text (str): text to colorize

    Returns:
        - str: colorized text
"""

import RofiLessonManager.utils as utils


def get_color_from_id(id, text):
    """
    Get color from id and text to colorize.

    Args:
        - id (int): color id (default: None)
        - text (str): text to colorize

    Returns:
        - str: colorized text
    """

    color = ''

    if not id:
        color = '#4f86f7'
    if id == '1':
        color = '#dcd0ff'
    if id == '2':
        color = '#bcb88a'
    if id == '3':
        color = '#6f2da8'
    if id == '4':
        color = '#fc8eac'
    if id == '5':
        color = '#ffe135'
    if id == '6':
        color = '#f28500'
    if id == '8':
        color = '#251607'
    if id == '9':
        color = '#326872'
    if id == '10':
        color = '#626e60'
    if id == '11':
        color = '#ff6347'

    return utils.colored_text(text, color)
