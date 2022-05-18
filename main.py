#!/usr/bin/env python3


import argparse

import src.calendar as ca
import src.change_path as cp
import src.source_lectures as sl
import src.new_assignment as na
import src.new_course as nc
import src.new_lecture as nl
import src.projects as pr
import src.rofi_assignments as ra
import src.rofi_courses as rc
import src.rofi_lectures as rl


def main():
    parser = argparse.ArgumentParser(description='Lesson Manager')

    parser.add_argument('-ca', '--calendar',
                        help='Parse google calendar', action='store_true')
    parser.add_argument('-cp', '--change-path',
                        help='Change path to classes', action='store_true')
    parser.add_argument('-na', '--new-assignment',
                        help='Create a new assignment', action='store_true')
    parser.add_argument('-nc', '--new-course',
                        help='Create a new course', action='store_true')
    parser.add_argument('-nl', '--new-lecture',
                        help='Create a new lecture', action='store_true')
    parser.add_argument('-pr', '--projects',
                        help='Projects', action='store_true')
    parser.add_argument('-ra', '--rofi-assignments',
                        help='View all assignments', action='store_true')
    parser.add_argument('-rc', '--rofi-courses',
                        help='Change course', action='store_true')
    parser.add_argument('-rl', '--rofi-lectures',
                        help='View all Lectures', action='store_true')
    parser.add_argument('-sl', '--source-lectures',
                        help='Source lectures', action='store_true')

    args = parser.parse_args()

    if args.calendar:
        ca.main()
    if args.change_path:
        cp.main()
    elif args.new_course:
        nc.main()
    elif args.new_assignment:
        na.main()
    elif args.new_lecture:
        nl.main()
    elif args.projects:
        pr.main()
    elif args.rofi_assignments:
        ra.main()
    elif args.rofi_courses:
        rc.main()
    elif args.rofi_lectures:
        rl.main()
    elif args.source_lectures:
        sl.main()


if __name__ == "__main__":
    main()
