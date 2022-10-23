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
    """
    Display all the assignments to the user to select from.

    Example:
        There're 10 different possible outputs based on the data from each
        assignment. Here're all the possible outputs.

        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                                       Jun 18 (Sat) |
        |  9. Week 9 Graded Assignment                         Jun 04 (Sat) |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                         Jun 18 (Sat) (2 DAYS LATE) |
        |  9. Week 9 Graded Assignment           Jun 04 (Sat)               |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                         Jun 18 (Sat) (2 DAYS LEFT) |
        |  9. Week 9 Graded Assignment           Jun 04 (Sat)               |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                            Jun 18 (Sat) (TOMORROW) |
        |  9. Week 9 Graded Assignment              Jun 04 (Sat)            |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                           Jun 18 (Sat) (YESTERDAY) |
        |  9. Week 9 Graded Assignment             Jun 04 (Sat)             |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                                       Jun 18 (Sat) |
        |  9. This is a very long title, because I need  ...   Jun 04 (Sat) |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                         Jun 18 (Sat) (2 DAYS LATE) |
        |  9. This is a very long title, be ...  Jun 04 (Sat)               |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                         Jun 18 (Sat) (2 DAYS LEFT) |
        |  9. This is a very long title, be ...  Jun 04 (Sat)               |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                            Jun 18 (Sat) (TOMORROW) |
        |  9. This is a very long title, becau ...  Jun 04 (Sat)            |
        |                                                                   |
        |-------------------------------------------------------------------|
        |                                                                   |
        | 10. Final Exam                           Jun 18 (Sat) (YESTERDAY) |
        |  9. This is a very long title, beca ...  Jun 04 (Sat)             |
        |                                                                   |
        |-------------------------------------------------------------------|
    """

    # The different commands we'll use later.
    commands = ["edit_latex", "edit_yaml", "open_pdf"]
    # The list of sub commands we'll use later.
    second_options = []

    # Get all our assignments.
    assignments = Assignments()

    # Check if we have any assignments
    # If we don't, just give an error and return
    if not assignments:
        utils.rofi.msg("You don't have any assignments.")
        exit(1)

    # Sort the assignments by reverse order. The latest assignment must show up
    # first.
    sorted_assignments = sorted(assignments, key=lambda l: -int(l.number))
    # Get all the due dates.
    due_dates = [a.due_date for a in sorted_assignments]

    # Get the biggest due date string
    fill = len(max(due_dates, key=len))
    if fill == 12:
        fill += 35
    else:
        fill += 35 - fill

    # Create the assignment options for the user to select from.
    options = [
        f"{utils.display_number(a.number): >2}. "
        + f"<b>{utils.generate_short_title(a.title, fill-2): <{fill}}</b>"
        + f"<i><span size='smaller'>{a.due_date}</span></i>"
        for a in sorted_assignments
    ]

    # Ask the user to select one.
    _, index, _ = utils.rofi.select(
        "Select Assignment",
        options,
        rofi_options,
    )

    # If the user didn't select one, exit.
    if index < 0:
        exit(1)

    assignment = sorted_assignments[index].number
    # Create the path to the latex file for the selected assignment.
    tex_path = f"{my_assignments_latex_folder}/week-" + f"{assignment}.tex"
    # Create the path to the yaml file for the selected assignment.
    yaml_path = f"{my_assignments_yaml_folder}/week-" + f"{assignment}.yaml"
    # Create the path to the pdf file for the selected assignment.
    pdf_path = f"{my_assignments_pdf_folder}/week-" + f"{assignment}.pdf"

    # If the latex file exists, add the command `view latex`.
    second_options.append("View LaTeX") if os.path.exists(tex_path) else ""
    # If the yaml file exists, add the command `view yaml`.
    second_options.append("View YAML") if os.path.exists(yaml_path) else ""
    # If the pdf file exists, add the command `view pdf`.
    second_options.append("View PDF") if os.path.exists(pdf_path) else ""

    _, second_index, _ = utils.rofi.select(
        f"Which one for assignment: {sorted_assignments[index].title}",
        second_options,
        rofi_options,
    )

    # If the user didn't select one, exit.
    if second_index < 0:
        sys.exit(0)

    # Execute the selected command.
    sorted_assignments[index].parse_command(commands[second_index])


if __name__ == "__main__":
    main()
