#!/usr/bin/env python3.10

import os
import sys

from RofiLessonManager.assignments import Assignments
import RofiLessonManager.utils as utils
from config import (
    my_assignments_latex_folder,
    my_assignments_pdf_folder,
    my_assignments_yaml_folder,
    rofi_options,
)


def main():
    commands = ["edit_latex", "edit_yaml", "open_pdf"]
    second_options = []

    assignments = Assignments()

    if not assignments:
        utils.rofi.msg("You don't have any assignments.")
        exit(1)

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

    assignment = sorted_assignments[index].number
    tex_path = f"{my_assignments_latex_folder}/week-" + f"{assignment}.tex"
    yaml_path = f"{my_assignments_yaml_folder}/week-" + f"{assignment}.yaml"
    pdf_path = f"{my_assignments_pdf_folder}/week-" + f"{assignment}.pdf"

    second_options.append("View LaTeX") if os.path.exists(tex_path) else ""
    second_options.append("View YAML") if os.path.exists(yaml_path) else ""
    second_options.append("View PDF") if os.path.exists(pdf_path) else ""

    _, second_index, _ = utils.rofi.select(
        f"Which one for assignment: {sorted_assignments[index].title}",
        second_options,
        rofi_options,
    )

    if second_index < 0:
        sys.exit(0)

    sorted_assignments[index].parse_command(commands[second_index])


if __name__ == "__main__":
    main()
