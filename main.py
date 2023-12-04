#!/usr/bin/env python3

import argparse
import os
import sys
import config


def main():
    parser = argparse.ArgumentParser(description="Lesson Manager:")

    parser.add_argument(
        "-ca",
        "--calendar",
        help="Parse google calendar.",
        action="store_true",
    )
    parser.add_argument(
        "-gc",
        "--get-course",
        metavar="CRN",
        help="Get course info from CRN number. Seperate by comma.",
    )
    parser.add_argument(
        "-ic",
        "--init-courses",
        help="Initalize all courses.",
        action="store_true",
    )
    parser.add_argument(
        "-ra",
        "--rofi-assignments",
        help="View assignments.",
        action="store_true",
    )
    parser.add_argument(
        "-rb",
        "--rofi-books",
        help="View books.",
        action="store_true",
    )
    parser.add_argument(
        "-rc",
        "--rofi-courses",
        help="View courses.",
        action="store_true",
    )
    parser.add_argument(
        "-rn",
        "--rofi-notes",
        help="View notes.",
        action="store_true",
    )
    parser.add_argument(
        "-rsn",
        "--rofi-strip-notes",
        help="Strip Notes.",
        action="store_true",
    )
    parser.add_argument(
        "-rsno",
        "--rofi-strip-notes-output",
        help="Stripped notes output.",
        default="output.tex",
    )
    parser.add_argument(
        "-sn",
        "--source-notes",
        help="Source notes.",
        action="store_true",
    )
    parser.add_argument(
        "-yn",
        "--sync-notes",
        help="Sync notes to google drive.",
        action="store_true",
    )

    args = parser.parse_args()

    os.chdir(sys.path[0])

    if args.calendar:
        import src.countdown as ca

        print("Waiting for connection")
        ca.check_internet()
        ca.main()
    if args.get_course:
        import src.get_course as gc

        gc.main(args.get_course)
    if args.init_courses:
        import src.init_courses as ic

        ic.main()
    if args.rofi_assignments:
        import src.rofi_assignments as ra

        ra.main()
    if args.rofi_books:
        import src.rofi_books as rb

        rb.main()
    if args.rofi_courses:
        import src.rofi_courses as rc

        rc.main()
    if args.rofi_notes:
        import src.rofi_notes as rn

        rn.main()
    if args.rofi_strip_notes:
        import src.rofi_strip_notes as rsn

        rsn.main(args.rofi_strip_notes_output)
    if args.source_notes:
        import src.source_notes as sn

        sn.main()
    if args.sync_notes:
        import src.sync_notes as sy

        sy.main()


if __name__ == "__main__":
    main()
