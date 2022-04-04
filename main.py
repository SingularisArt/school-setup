#!/usr/bin/env python3


import argparse

import RofiLessonManager.change_course as cc
import RofiLessonManager.commands as cm
import RofiLessonManager.new_lesson as nl
import RofiLessonManager.projects as pr
import RofiLessonManager.view_lessons as vl


def Main():
    parser = argparse.ArgumentParser(description='Lesson Manager')
    parser.add_argument('-c', '--change-course', help='Change course',
                        action='store_true')
    parser.add_argument('-m', '--commands', help='Commands',
                        action='store_true')
    parser.add_argument('-n', '--new-lesson', help='Create new lesson',
                        action='store_true')
    parser.add_argument('-p', '--projects', help='Projects',
                        action='store_true')
    parser.add_argument('-l', '--lessons', help='View all Lessons',
                        action='store_true')

    args = parser.parse_args()

    if args.change_course:
        cc.main()
    elif args.commands:
        cm.main()
    elif args.new_lesson:
        nl.main()
    elif args.projects:
        pr.main()
    elif args.lessons:
        vl.main()


if __name__ == "__main__":
    Main()
