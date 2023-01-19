#!/usr/bin/env python3

import os
import sys

import utils
from config import my_assignments_folder, rofi_options
from RofiLessonManager.assignments import Assignments


def main():
    assignments = sorted(Assignments(), key=lambda lec: -int(lec.number))

    if not assignments:
        utils.rofi.msg("You don't have any assignments.", err=True)
        exit(1)

    options = []

    fill = 50

    for a in assignments:
        number = a.number
        title = utils.generate_short_title(a.title, fill)
        due_date = a.due_date
        days_left = a.days_left
        grade = f"({a.grade}%)" if isinstance(a.grade, int) else "(NA)"

        fill_for_due_date = abs(len(due_date) + len(days_left) + len(grade))
        # fill = len(due_date) + len(days_left) + len(grade) - MAX_ROFI_LENGTH
        # fill = abs(fill)

        a_string = f"{number: >2}. <b>{title: <{fill_for_due_date}}</b>"
        # a_string += f"<i><span size='smaller'>{due_date} {days_left} {grade}"
        a_string += f"<i><span size='smaller'>{due_date}"
        a_string += "</span></i>"

        options.append(a_string)

    _, index, _ = utils.rofi.select(
        "Select Assignment",
        options,
        rofi_options,
    )

    if index < 0:
        exit(1)

    commands = assignments[index].options
    _, second_index, selection = utils.rofi.select(
        "Select command",
        commands,
        rofi_options,
    )

    if second_index < 0:
        sys.exit(0)

    os.chdir(my_assignments_folder)
    assignments[index].parse_command(commands[selection])


if __name__ == "__main__":
    main()
