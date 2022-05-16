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

    key, index, selected = utils.rofi('Select Lesson', lectures.rofi_titles,
                                      lectures.rofi_options)

    if index >= 0:
        os.chdir('{}/lectures'.format(lectures.current_course))
        lectures[index].edit()


if __name__ == "__main__":
    main()
