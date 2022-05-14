import os
import sys

from RofiLessonManager.classes.assignments import Assignments as Assignments
import RofiLessonManager.utils as utils


def main():
    """
    This function will run the program
    """

    assignment = Assignments()

    key, index, selected = utils.rofi('Select Assignment',
                                      assignment.rofi_names,
                                      assignment.rofi_options)

    if index < 0:
        sys.exit(0)

    assignment_file = assignment.assignments[index]

    second_key, second_index, second_selected = utils.rofi(
        'Which One for assignment: {}'.format(
            assignment[index]),
        assignment.second_options, assignment.rofi_options)

    os.chdir(assignment.assignments_folder)

    if second_selected == assignment.second_options[0]:
        utils.open_file('xfce4-terminal', 'nvim',
                        assignment.assignments_folder,
                        assignment_file, type='assignment')
    elif second_selected == assignment.second_options[1]:
        utils.open_file('xfce4-terminal', 'nvim',
                        assignment.assignments_folder,
                        assignment.yaml_files[index], type='assignment')
    elif second_selected == assignment.second_options[2]:
        os.system('zathura {}/{}'.format(assignment.assignments_pdf_folder,
                  assignment.pdf_files[index]))


if __name__ == "__main__":
    main()
