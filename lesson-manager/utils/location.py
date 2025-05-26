import utils


def location(text):
    if not text:
        return ""

    return f"{utils.colored_text('in')} {text}"
