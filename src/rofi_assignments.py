#!/usr/bin/env python3

import os
import sys

from RofiLessonManager.assignments import Assignments
import RofiLessonManager.utils as utils
from config import (
    my_assignments_folder,
    rofi_options,
)


def main():
    assignments = Assignments()

    if not assignments:
        utils.rofi.msg("You don't have any assignments.", err=True)
        exit(1)

    commands = ["edit_latex", "edit_yaml", "open_pdf"]
    second_options = []

    sorted_assignments = sorted(assignments, key=lambda l: -int(l.number))
    due_dates = [a.due_date for a in sorted_assignments]

    fill = len(max(due_dates, key=len))
    if fill == 12:
        fill += 35
    else:
        fill += 35 - fill

    options = [
        f"{utils.display_number(a.number): >2}. "
        + f"<b>{utils.generate_short_title(a.title, fill-2): <{fill}}</b>"
        + f"<i><span size='smaller'>{a.due_date}</span></i>"
        for a in sorted_assignments
    ]

    _, index, _ = utils.rofi.select(
        "Select Assignment",
        options,
        rofi_options,
    )

    if index < 0:
        exit(1)

    _, second_index, _ = utils.rofi.select(
        "Select command",
        sorted_assignments[index].options,
        rofi_options,
    )

    if second_index < 0:
        sys.exit(0)

    os.chdir(my_assignments_folder)
    sorted_assignments[index].parse_command(commands[second_index])


if __name__ == "__main__":
    main()
