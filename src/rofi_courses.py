"""
This file uses the RofiLessonManager.courses module to help switch between
different courses.
"""

from RofiLessonManager.courses import Courses as Courses
from RofiLessonManager import utils as utils


def main():
    """ This main function will change the current course. """

    courses = Courses()
    current = courses.current

    try:
        current_index = courses.index(current)
        args = ['-a', current_index]
    except Exception:
        args = []

    key, index, selected = utils.rofi(
        'Select course', [c.info['title'] for c in courses], [
            '-auto-select',
            '-no-custom',
            '-lines', len(courses)
        ] + args)

    if index >= 0:
        courses.current = courses[index]


if __name__ == "__main__":
    main()
