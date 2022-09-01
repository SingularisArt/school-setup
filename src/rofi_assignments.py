import os
import sys

from RofiLessonManager.assignments import Assignments
import RofiLessonManager.utils as utils


def main():
    commands = ["edit_latex", "edit_yaml", "open_pdf"]
    second_options = []

    assignments = Assignments()
    if len(assignments) == 0:
        utils.rofi.error_message("You don't have any assignments.")
        return
    sorted_assignments = sorted(assignments, key=lambda l: -int(l.number))
    due_dates = [a.due_date for a in sorted_assignments]

    fill = len(max(due_dates, key=len))
    if int(fill) == 12:
        fill += 5
    else:
        pass

    options = [
        "{number: >2}. <b>{title: <{fill}}</b> <i><span size='smaller'>Due By: {date: <{fill_2}}</span></i> Submitted: {submit}".format(
            fill=22,
            number=utils.display_number(assignment.number),
            title=assignment.title,
            date=assignment.due_date,
            submit=assignment.submit,
            fill_2=fill,
        )
        for assignment in sorted_assignments
    ]

    # Check if we have any assignments
    # If we don't, just give an error and return
    if not assignments:
        utils.rofi.error_message("No assignments found")
        exit(1)

    key, index, selected = utils.rofi.select(
        "Select Assignment", options, assignments.rofi_options
    )

    if index < 0:
        sys.exit(0)

    tex_path = "{}/week-{}".format(
        assignments.my_assignments_latex_folder, sorted_assignments[index].number
    )
    yaml_path = "{}/week-{}".format(
        assignments.my_assignments_yaml_folder, sorted_assignments[index].number
    )
    pdf_path = "{}/week-{}".format(
        assignments.my_assignments_pdf_folder, sorted_assignments[index].number
    )

    second_options.append("View LaTeX") if os.path.exists(
        "{}.tex".format(tex_path)
    ) else ""
    second_options.append("View YAML") if os.path.exists(
        "{}.yaml".format(yaml_path)
    ) else ""
    second_options.append("View PDF") if os.path.exists(
        "{}.pdf".format(pdf_path)
    ) else ""

    second_key, second_index, second_selected = utils.rofi.select(
        "Which One for assignment: {}".format(sorted_assignments[index].title),
        second_options,
        assignments.rofi_options,
    )

    if second_index < 0:
        sys.exit(0)

    os.chdir(assignments.my_assignments_latex_folder)

    sorted_assignments[index].parse_command(commands[second_index])


if __name__ == "__main__":
    main()
