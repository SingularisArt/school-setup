#!/usr/bin/env python3

from rofi import Rofi

from RofiLessonManager.lectures import Lecture as Lecture
from RofiLessonManager.lectures import Lectures as Lectures


def main():
    lectures = Lectures()

    rofi = Rofi()
    n = rofi.integer_entry("Enter lecture number")
    if int(n) < 10:
        n = f"0{n}"

    if n:
        Lecture(f"{lectures.current_course}/lectures/lec-{n}.tex")


if __name__ == "__main__":
    main()
