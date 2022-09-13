#!/usr/bin/env python3.10

import re

import RofiLessonManager.utils as utils


def summary(text: str) -> str:
    """
    Summary of the text.

    Args:
    -----
        text (str): The text to summarize.

    Returns:
    --------
        str: The summary of the text.
    """

    return utils.generate_short_title(
        re.sub(r"X[0-9A-Za-z]+", "", text).strip(), MAX_LENGTH=45
    )
