#!/usr/bin/env python3

import os

from RofiLessonManager import utils as utils
from RofiLessonManager.lectures import Lectures as Lectures
from config import current_course, date_format, rofi_options


def main():
    # Get all our assignments.
    lectures = Lectures()

    # Check if we have any assignments
    # If we don't, just give an error and return
    if not lectures:
        utils.rofi.msg("You don't have any assignments.")
        exit(1)

    # Sort the assignments by reverse order. The latest assignment must show up
    # first.
    sorted_lectures = sorted(lectures, key=lambda l: -int(l.number))

    # Create the assignment options for the user to select from.
    options = [
        f"{utils.display_number(str(lec.number)): >2}. "
        + f"<b>{utils.generate_short_title(lec.title, 27): <{27}} </b> "
        + f"<span size='smaller'>{lec.date.strftime(date_format): <{15}} "
        + f"(Week: {lec.week})</span>"
        for lec in sorted_lectures
    ]

    # Check if we have any lectures
    # If we don't, just give an error and return
    if not lectures:
        utils.rofi.msg("No lectures found")
        exit(1)

    # Ask the user to select one.
    _, index, _ = utils.rofi.select(
        "Select Lecture", options, rofi_options
    )

    # If the user didn't select one, exit.
    if index < 0:
        exit(1)

    os.chdir("{}/lectures".format(current_course))
    sorted_lectures[index].edit()


if __name__ == "__main__":
    main()
