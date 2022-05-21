"""
This file uses the RofiLessonManager.assignments module to display all of the
assignments, via rofi.

Example Output from Rofi:

1. Week 1: Graded As ...     Due By: May 11 (Wen)                Submitted: Yes
2. Week 2: Graded As ...     Due By: May 12 (Thu) (3 DAYS LATE)  Submitted: No
3. Week 3: Graded As ...     Due By: May 13 (Fri) (2 DAYS LATE)  Submitted: No
4. Week 4: Graded As ...     Due By: May 14 (Sat) (YESTERDAY)    Submitted: No
5. Week 5: Graded As ...     Due By: May 15 (Sun) (TODAY)        Submitted: No
6. Week 6: Graded As ...     Due By: May 16 (Mon) (TOMORROW)     Submitted: No
7. Week 7: Graded As ...     Due By: May 17 (Tue) (2 DAYS LEFT)  Submitted: No
8. Week 8: Graded As ...     Due By: May 18 (Wen) (3 DAYS LEFT)  Submitted: No
9. Week 9: Graded As ...     Due By: May 19 (Thu)                Submitted: Yes
"""

import os
import sys

from RofiLessonManager.assignments import Assignments as Assignments
import RofiLessonManager.utils as utils


def main():
    """
    This main function will allow the user to select the assignment, and
    then select if they would like to open the LaTeX source code, the yaml
    file, or the pdf.
    """

    commands = ['edit_latex', 'edit_yaml', 'open_pdf']
    second_options = ['View LaTeX', 'View YAML', 'View PDF']

    assignments = Assignments()
    due_dates = [a.due_date for a in assignments]
    fill = len(max(due_dates, key=len))
    if int(fill) == 12:
        fill += 5
    else:
        fill += 1

    options = [
        "{number: >2}. <b>{title: <{fill}}</b> <i><span size='smaller'>Due By: {date: <{fill_2}}</span></i> Submitted: {submit}".format(
            fill=22,
            number=assignment.number,
            title=assignment.title,
            date=assignment.due_date,
            submit=assignment.submit,
            fill_2=fill,
        )
        for assignment in assignments
    ]

    key, index, selected = utils.rofi('Select Assignment',
                                      options,
                                      assignments.rofi_options)

    if index < 0:
        sys.exit(0)

    second_key, second_index, second_selected = utils.rofi(
        'Which One for assignment: {}'.format(
            assignments[index].title),
        second_options, assignments.rofi_options)

    os.chdir(assignments.assignments_latex_folder)

    assignments[index].parse_command(commands[second_index])


if __name__ == "__main__":
    main()
