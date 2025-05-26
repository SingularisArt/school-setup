def generate_short_title(title, MAX_LENGTH=34):
    ellipsis = " ..."
    if len(title) < MAX_LENGTH:
        return title

    return title[: MAX_LENGTH - len(ellipsis)] + ellipsis
