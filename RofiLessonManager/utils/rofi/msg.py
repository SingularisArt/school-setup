from RofiLessonManager.utils import rofi


def msg(msg: str, bold=True, italic=False, underline=False, err=False) -> None:
    """
    Display a message, via Rofi. The text provided will be colored red, if the
        message is an error. Else, the color will be green. The default styles
        are: Bold

    Args:
    -----
        msg (str): The string to display.
        bold (bool): String to be bold or not. Default: True.
        italic (bool): String to be italic or not. Default: False.
        underline (bool): String to be underlined or not. Default: False.
        err (bool): If the message is an error message or not. If it is, then
            the color of the text will be red. Else, green.
    """

    beginning = (
        f"{'<b>' if bold else ''}"
        + f"{'<i>' if italic else ''}"
        + f"{'<u>' if underline else ''}"
    )
    end = (
        f"{'</u>' if underline else ''}"
        + f"{'</i>' if italic else ''}"
        + f"{'</b>' if bold else ''}"
    )
    text = f"{beginning}{msg}{end}"

    rofi.display_text(
        f"<span color='{'red' if err else 'green'}'>{text}</span>",
    )
