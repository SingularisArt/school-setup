def generate_short_title(title, MAX_LENGTH=36):
    """
    Shorten a title of too long in length.

    Args:
        title (str): The title to shorten.
        MAX_LENGTH (int): The maximum length of the title. (Default: 36)

    Returns:
        str: The shortened title.
    """

    if len(title) > MAX_LENGTH:
        title = title[:MAX_LENGTH - len(' ...')] + '...'
    return title
