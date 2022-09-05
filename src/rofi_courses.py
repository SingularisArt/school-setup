"""
This file uses the RofiLessonManager.courses module to help switch between
different courses.
"""

from RofiLessonManager.courses import Courses as Courses
from RofiLessonManager import utils as utils


def main():
    """This main function will change the current course."""

    courses = Courses()
    current = courses.current
    options = [
        "<b>{title: <{fill}}</b> <i>({topic}: <b>{number})</b></i>".format(
            title=utils.generate_short_title(c.info["title"]),
            topic=c.info["topic"],
            fill=34,
            number=c.info["class_number"],
        )
        for c in courses
    ]
    print(options[0])

    try:
        current_index = courses.index(current)
        args = ["-a", current_index]
    except Exception:
        args = []

    key, index, selected = utils.rofi.select(
        "Select course",
        options,
        [
            "-lines",
            len(courses),
            "-markup-rows",
            "-kb-row-down",
            "Down",
            "-kb-custom-1",
            "Ctrl+n",
        ]
        + args,
    )

    if index >= 0:
        courses.current = courses[index]


if __name__ == "__main__":
    main()
