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
        "-rn",
        "--rofi-notes",
        help="View notes",
        action="store_true",
    )
    parser.add_argument(
        "-sn",
        "--source-notes",
        help="Source notes",
        action="store_true",
    )
    parser.add_argument(
        "-sy",
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
    elif args.rofi_notes:
        import src.rofi_notes as rn

        rn.main()
    elif args.source_notes:
        import src.source_notes as sn

        sn.main()
    elif args.sync_notes:
        import src.sync_notes as sy

        sy.main()
    elif args.init_courses:
        import src.init_courses as ic

        ic.main()


if __name__ == "__main__":
    main()
