#!/usr/bin/env python3

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Lesson Manager")

    parser.add_argument(
        "-ca",
        "--calendar",
        help="Parse google calendar",
        action="store_true",
    )
    parser.add_argument(
        "-ra",
        "--rofi-assignments",
        help="View assignments",
        action="store_true",
    )
    parser.add_argument(
        "-rc",
        "--rofi-courses",
        help="View courses",
        action="store_true",
    )
    parser.add_argument(
        "-rl",
        "--rofi-lectures",
        help="View lectures",
        action="store_true",
    )
    parser.add_argument(
        "-sl",
        "--source-lectures",
        help="Source lectures",
        action="store_true",
    )
    parser.add_argument(
        "-sn",
        "--sync-notes",
        help="Sync notes to google drive",
        action="store_true",
    )
    parser.add_argument(
        "-ic",
        "--init-courses",
        help="Initalize all courses",
        action="store_true",
    )

    args = parser.parse_args()

    os.chdir(sys.path[0])

    if args.calendar:
        import src.countdown as ca

        print("Waiting for connection")
        ca.check_internet()
        ca.main()
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
    elif args.sync_notes:
        import src.sync_notes as sn

        sn.main()
    elif args.init_courses:
        import src.init_courses as ic

        ic.main()


if __name__ == "__main__":
    main()
