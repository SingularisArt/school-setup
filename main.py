#!/usr/bin/env python3


import argparse

from RofiLessonManager import Basis as Basis
import RofiLessonManager.view_assignments as va
import RofiLessonManager.new_assignment as na
import RofiLessonManager.change_course as cc
import RofiLessonManager.change_path_to_classes as ch
import RofiLessonManager.commands as cm
import RofiLessonManager.new_lesson as nl
import RofiLessonManager.projects as pr
import RofiLessonManager.view_lessons as vl


def Main():
    parser = argparse.ArgumentParser(description='Lesson Manager')

    parser.add_argument('-na', '--new-assignment',
                        help='Create new assignment', action='store_true')
    parser.add_argument('-va', '--view-assignments',
                        help='View all assignments', action='store_true')
    parser.add_argument('-cc', '--change-course',
                        help='Change course', action='store_true')
    parser.add_argument('-cp', '--change-path',
                        help='Change path to classes', action='store_true')
    parser.add_argument('-m', '--commands',
                        help='Commands', action='store_true')
    parser.add_argument('-nl', '--new-lesson',
                        help='Create new lesson', action='store_true')
    parser.add_argument('-p', '--projects',
                        help='Projects', action='store_true')
    parser.add_argument('-vl', '--view-lessons',
                        help='View all Lessons', action='store_true')

    args = parser.parse_args()

    if args.new_assignment:
        na.main()
    if args.view_assignments:
        va.main()
    if args.change_course:
        cc.main()
    if args.change_path:
        ch.main()
    elif args.commands:
        cm.main()
    elif args.new_lesson:
        nl.main()
    elif args.projects:
        pr.main()
    elif args.view_lessons:
        vl.main()


if __name__ == "__main__":
    Main()
