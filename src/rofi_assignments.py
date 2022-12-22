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
    assignments = sorted(Assignments(), key=lambda lec: -int(lec.number))

    if not assignments:
        utils.rofi.msg("You don't have any assignments.", err=True)
        exit(1)

    due_dates = [a.due_date for a in assignments]

    fill = len(max(due_dates, key=len))
    if fill == 12:
        fill += 30
    else:
        fill += 35 - fill

    options = [
        f"{a.number: >2}. "
        + f"<b>{utils.generate_short_title(a.title, fill-2): <{fill}}</b>"
        + f"<i><span size='smaller'>{a.due_date}"
        + f"{'(' + str(a.score) + '%)' if a.submit != 'No' else ''}</span></i>"
        for a in assignments
    ]

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
