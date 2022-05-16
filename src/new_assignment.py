"""
This file uses the RofiLessonManager.lectures module to help open and edit
lectures.
"""

from rofi import Rofi

from RofiLessonManager.assignments import Assignment as Assignment
from RofiLessonManager.assignments import Assignments as Assignments


def main():
    """ This main function will open and edit the selected lecture. """

    assignments = Assignments()

    rofi = Rofi()
    n = rofi.integer_entry('Enter assignment number')

    if not n:
        return

    Assignment('{}/week-{}.tex'.format(
        assignments.assignments_latex_folder, n))


if __name__ == "__main__":
    main()
