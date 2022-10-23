#!/usr/bin/env python3

from RofiLessonManager.courses import Courses as Courses


def main():
    courses = Courses()
    current = courses.current
    index = 0

    for x, course in enumerate(courses):
        if course.name == current:
            index = x

        courses.current = course
        lectures = course.lectures

        r = lectures.parse_range_string("all")
        lectures.update_lectures_in_master(r)
        lectures.compile_master()

    courses.current = courses[index]
