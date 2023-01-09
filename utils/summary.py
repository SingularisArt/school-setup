#!/usr/bin/env python3.10

import re

import utils


def summary(text: str) -> str:
    return utils.generate_short_title(
        re.sub(r"X[0-9A-Za-z]+", "", text).strip(), MAX_LENGTH=45
    )
