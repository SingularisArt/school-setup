from RofiLessonManager.utils import rofi


def msg(msg: str, bold=True, italic=False, underline=False, err=False) -> None:
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
