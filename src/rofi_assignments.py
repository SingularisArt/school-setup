import os
import sys
from RofiLessonManager.assignments import Assignments
from config import assignments_dir, rofi_options
import utils


def format_option(assignment):
    number = assignment.number
    title = utils.generate_short_title(assignment.title, 20)
    due_date = utils.generate_short_title(assignment.due_date, 15)
    days_left = utils.generate_short_title(assignment.days_left, 16)
    grade = f"({assignment.grade}%)"
    if not isinstance(assignment.grade, (int, float)):
        grade = "(NA)"

    column_1 = f"<b>{number: >2}. {title: <25}</b>"
    column_2 = f"<i><span size='smaller'>{due_date: <15}</span></i>"
    column_3 = f"<i><span size='smaller'>{days_left: <15}</span></i>"
    column_4 = f"<i><span size='smaller'>{grade: >7}</span></i>"

    return f"{column_1} {column_2} {column_3} {column_4}"


def main():
    assignments = sorted(Assignments(), key=lambda lec: -int(lec.number))

    if not assignments:
        utils.rofi.msg("You don't have any assignments.", err=True)
        exit(1)

    options = [format_option(assignment) for assignment in assignments]

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

    os.chdir(assignments_dir)
    assignments[index].parse_command(commands[selection])


if __name__ == "__main__":
    main()
