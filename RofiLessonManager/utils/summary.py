"""
Function summary:
    - RofiLessonManager.utils.summary

    Summary of the text.

    Args:
        - text (str): The text to summarize.

    Returns:
        - str: The summary of the text.
"""

import re

import RofiLessonManager.utils as utils


def summary(text):
    """
    Summary of the text.

    Args:
        - text (str): The text to summarize.

    Returns:
        - str: The summary of the text.
    """

    return utils.generate_short_title(re.sub(r'X[0-9A-Za-z]+',
                                             '', text).strip(), 50)
