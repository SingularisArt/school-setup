"""
Function colored_text:
    - RofiLessonManager.utils.colored_text

    Return colored text for polybar.

    Args:
        - text (str): Text to be colored.
        - color (str): Hex color code.

    Returns:
        - str: Colored text.
"""


def colored_text(text, color='#999999'):
    """
    Return colored text for polybar.

    Args:
        - text (str): Text to be colored.
        - color (str): Hex color code.

    Returns:
        - str: Colored text.
    """

    return '%{F' + color + '}' + text + '%{F-}'
