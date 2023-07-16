import re

import utils


def summary(text):
    if not isinstance(text, str):
        raise TypeError("text must be of str type")
    return utils.generate_short_title(
        re.sub(r"X[0-9A-Za-z]+", "", text).strip(), MAX_LENGTH=45
    )
