"""
This file uses the RofiLessonManager.courses module to create a new course.
"""

from rofi import Rofi

from RofiLessonManager import Basis as Basis
from RofiLessonManager.courses import Course as Course
from RofiLessonManager.courses import Courses as Courses
import RofiLessonManager.utils as utils


def main():
    """ This function creates a new course. """

    b = Basis()
    r = Rofi()

    name = r.text_entry('Course Name')

    if not name:
        return

    name = name.replace(' ', '-').replace('_', '-').lower()

    if '{}/{}'.format(b.root, name) in Courses().paths:
        utils.rofi.error_message('Course already exists')
        return

    Course('{}/{}'.format(b.root, name))


if __name__ == "__main__":
    main()
