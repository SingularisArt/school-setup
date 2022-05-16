#!/usr/bin/env python3


import argparse

import src.change_path as cp
import src.commands as cm
import src.new_course as nc
import src.projects as pr
import src.rofi_assignments as ra
import src.rofi_courses as rc
import src.rofi_lectures as rl


def main():
    parser = argparse.ArgumentParser(description='Lesson Manager')

    parser.add_argument('-cp', '--change-path',
                        help='Change path to classes', action='store_true')
    parser.add_argument('-cm', '--commands',
                        help='Commands', action='store_true')
    parser.add_argument('-nc', '--new-course',
                        help='Create a new course', action='store_true')
    parser.add_argument('-pr', '--projects',
                        help='Projects', action='store_true')
    parser.add_argument('-ra', '--rofi-assignments',
                        help='View all assignments', action='store_true')
    parser.add_argument('-rc', '--rofi-course',
                        help='Change course', action='store_true')
    parser.add_argument('-rl', '--rofi-lectures',
                        help='View all Lectures', action='store_true')

    args = parser.parse_args()

    if args.change_path:
        cp.main()
    elif args.commands:
        cm.main()
    elif args.new_course:
        nc.main()
    elif args.projects:
        pr.main()
    elif args.rofi_assignments:
        ra.main()
    elif args.rofi_course:
        rc.main()
    elif args.rofi_lectures:
        rl.main()


if __name__ == "__main__":
    main()
