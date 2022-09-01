#!/usr/bin/env python3

import os

from RofiLessonManager.lectures import Lectures as Lectures
from RofiLessonManager import utils as utils


def main():
    lectures = Lectures()
    sorted_lectures = sorted(lectures, key=lambda l: -int(l.number))

    options = [
        "{number: >2}. <b>{title: <{fill}} </b> <span size='smaller'>{date: <{fill_2}} (Week: {week})</span>".format(
            fill=38,
            number=utils.display_number(lecture.number),
            title=utils.generate_short_title(lecture.title, 39),
            date=lecture.date.strftime("%a %d %b (%I:%M %p)"),
            fill_2=25,
            week=lecture.week,
        )
        for lecture in sorted_lectures
    ]

    # Check if we have any lectures
    # If we don't, just give an error and return
    if not lectures:
        utils.rofi.error_message("No lectures found")
        exit(1)

    key, index, selected = utils.rofi.select(
        "Select Lesson", options, lectures.rofi_options
    )

    if index >= 0:
        os.chdir("{}/lectures".format(lectures.current_course))
        sorted_lectures[index].edit()


if __name__ == "__main__":
    main()
