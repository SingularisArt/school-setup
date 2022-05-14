#!/usr/bin/env python3


import argparse

import RofiLessonManager.src.view_assignments as va
import RofiLessonManager.src.rofi_courses as rc
import RofiLessonManager.src.change_path as ch
import RofiLessonManager.src.commands as cm
import RofiLessonManager.src.projects as pr
import RofiLessonManager.src.rofi_lectures as rl
import RofiLessonManager.src.new_course as nc


def main():
    parser = argparse.ArgumentParser(description='Lesson Manager')

    parser.add_argument('-va', '--view-assignments',
                        help='View all assignments', action='store_true')
    parser.add_argument('-cc', '--change-course',
                        help='Change course', action='store_true')
    parser.add_argument('-cp', '--change-path',
                        help='Change path to classes', action='store_true')
    parser.add_argument('-m', '--commands',
                        help='Commands', action='store_true')
    parser.add_argument('-p', '--projects',
                        help='Projects', action='store_true')
    parser.add_argument('-vl', '--view-lessons',
                        help='View all Lessons', action='store_true')
    parser.add_argument('-nc', '--new-course',
                        help='Create a new course', action='store_true')

    args = parser.parse_args()

    if args.view_assignments:
        va.main()
    if args.change_course:
        rc.main()
    if args.new_course:
        nc.main()
    if args.change_path:
        ch.main()
    elif args.commands:
        cm.main()
    elif args.projects:
        pr.main()
    elif args.view_lessons:
        rl.main()


if __name__ == "__main__":
    main()
