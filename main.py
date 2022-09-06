#!/usr/bin/env python3


import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Lesson Manager")

    parser.add_argument(
        "-ca", "--calendar", help="Parse google calendar", action="store_true"
    )
    parser.add_argument("-cp", "--change-path",
                        help="Change path", action="store_true")
    parser.add_argument(
        "-na", "--new-assignment", help="New assignment", action="store_true"
    )
    parser.add_argument("-nc", "--new-course",
                        help="New course", action="store_true")
    parser.add_argument("-nl", "--new-lecture",
                        help="New lecture", action="store_true")
    parser.add_argument(
        "-ra", "--rofi-assignments", help="View assignments", action="store_true"
    )
    parser.add_argument(
        "-rc", "--rofi-courses", help="View courses", action="store_true"
    )
    parser.add_argument(
        "-rl", "--rofi-lectures", help="View lectures", action="store_true"
    )
    parser.add_argument(
        "-sl", "--source-lectures", help="Source lectures", action="store_true"
    )

    args = parser.parse_args()

    os.chdir(sys.path[0])

    if args.calendar:
        import src.calendar as ca
        print("Waiting for connection")
        ca.check_internet()
        ca.main()
    elif args.new_course:
        import src.new_course as nc
        nc.main()
    elif args.new_assignment:
        import src.new_assignment as na
        na.main()
    elif args.new_lecture:
        import src.new_lecture as nl
        nl.main()
    elif args.rofi_assignments:
        import src.rofi_assignments as ra
        ra.main()
    elif args.rofi_courses:
        import src.rofi_courses as rc
        rc.main()
    elif args.rofi_lectures:
        import src.rofi_lectures as rl
        rl.main()
    elif args.source_lectures:
        import src.source_lectures as sl
        sl.main()


if __name__ == "__main__":
    main()
