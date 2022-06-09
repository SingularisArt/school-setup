#!/usr/bin/env python3

"""
This file uses the RofiLessonManager.lectures module to help open and edit
lectures.
"""

from rofi import Rofi

from RofiLessonManager.lectures import Lecture as Lecture
from RofiLessonManager.lectures import Lectures as Lectures


def main():
    """ This main function will open and edit the selected lecture. """

    lectures = Lectures()

    rofi = Rofi()
    n = rofi.integer_entry('Enter lecture number')
    if n < 10:
        n = '0{}'.format(n)

    if n:
        Lecture('{}/lectures/lec-{}.tex'.format(lectures.current_course, n))


if __name__ == "__main__":
    main()
