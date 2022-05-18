"""
This file uses the RofiLessonManager.lectures module to help open and edit
lectures.
"""

import os

from RofiLessonManager.lectures import Lectures as Lectures
from RofiLessonManager import utils as utils


def main():
    """ This main function will open and edit the selected lecture. """

    lectures = Lectures()

    options = [
        "{number: >2}. <b>{title: <{fill}}</b> <span size='smaller'>{date}  ({week})</span>".format(
            fill=36,
            number=lecture.number,
            title=utils.generate_short_title(lecture.title),
            date=lecture.date.strftime('%a %d %b'),
            week=lecture.week
        )
        for lecture in lectures
    ]

    # Check if we have any lectures
    # If we don't, just give an error and return
    if not lectures:
        utils.error_message('No lectures found')
        exit(1)

    key, index, selected = utils.rofi('Select Lesson', options,
                                      lectures.rofi_options)

    if index >= 0:
        os.chdir('{}/lectures'.format(lectures.current_course))
        lectures[index].edit()


if __name__ == "__main__":
    main()
