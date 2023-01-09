#!/usr/bin/env python3

"""
This script provides a Rofi menu for selecting/editing lectures in a course.

The courses and lectures are defined in the `RofiLessonManager` module. The
configuration for the Rofi menu is read from the `config` module.
"""

import os
from typing import List

import config
import utils
from RofiLessonManager.courses import Courses as Courses


def generate_options(lectures: List, date_format: str) -> List[str]:
    """
    Generate the options for the Rofi menu.

    Args:
        lectures (List): The list of lectures.
        date_format (str): The format to use for the date strings.

    Returns:
        List[str]: The options for the Rofi menu.
    """

    options = []
    for lec in lectures:
        option = (
            f"{utils.display_number(str(lec.number)): >2}. "
            + f"<b>{utils.generate_short_title(lec.title, 26): <{26}} </b> "
            + f"<span size='smaller'>{lec.date.strftime(date_format): <{15}} "
            + f"(Week: {lec.week})</span>"
        )
        options.append(option)
    return options


def main() -> None:
    """
    The main function of the program.
    """

    courses: Courses = Courses()
    current_course: str = courses.current
    lectures: List = current_course.lectures

    if not lectures:
        utils.rofi.msg("No lectures found!", err=True)
        exit(1)

    # Sort the lectures in descending order by their number
    sorted_lectures = sorted(lectures, key=lambda lec: -int(lec.number))

    # Generate the options for the Rofi menu
    options = generate_options(sorted_lectures, config.date_format)

    # Display the Rofi menu and get the user's selection
    _, index, _ = utils.rofi.select(
        "Select Lecture",
        options,
        config.rofi_options,
    )

    if index < 0:
        exit(1)

    # Change to the "lectures" directory for the current course
    os.chdir(f"{config.current_course}/lectures")

    # Edit the selected lecture
    sorted_lectures[index].edit()


if __name__ == "__main__":
    main()
