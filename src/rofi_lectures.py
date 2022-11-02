#!/usr/bin/env python3

import os

from RofiLessonManager import utils as utils
from RofiLessonManager.courses import Courses as Courses
from config import current_course, date_format, rofi_options


def main():
    lectures = Courses().current.lectures

    if not lectures:
        utils.rofi.msg("No lectures found!", err=True)
        exit(1)

    sorted_lectures = sorted(lectures, key=lambda l: -int(l.number))

    options = [
        f"{utils.display_number(str(lec.number)): >2}. "
        + f"<b>{utils.generate_short_title(lec.title, 26): <{26}} </b> "
        + f"<span size='smaller'>{lec.date.strftime(date_format): <{15}} "
        + f"(Week: {lec.week})</span>"
        for lec in sorted_lectures
    ]
    print(options)

    _, index, _ = utils.rofi.select("Select Lecture", options, rofi_options)

    if index < 0:
        exit(1)

    os.chdir("{}/lectures".format(current_course))
    sorted_lectures[index].edit()


if __name__ == "__main__":
    main()
