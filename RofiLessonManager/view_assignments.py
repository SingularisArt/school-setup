#!/usr/bin/env python3

import os
import yaml

from RofiLessonManager import Basis as Basis
from RofiLessonManager import utils as utils


class ViewAssignments(Basis):
    """
    This class will allow us to view the assignments in the current course.
    """

    def __init__(self):
        """ Initialize the class """

        Basis.__init__(self)

        self.assignments_name, self.assignments_due_dates, \
            self.assignments_submitted = self.get_assignment_info()
        self.options = self.get_assignments_ready_to_be_viewed()
        self.second_options = [
                '<span color="yellow">View Assignment</span>',
                '<span color="yellow">View Assignment Yaml</span>',
                '<span color="yellow">View Assignment PDF</span>'
                              ]

    def get_assignment_info(self):
        """
        This function will get the assignment information from the yaml file.

        Returns:
            assignments_name (list): The name of the assignment.
            assignments_due_dates (list): The due date of the assignment.
            assignments_submitted (list): The status of the assignment.
        """
        assignments_name = []
        assignments_due_dates = []
        assignments_submitted = []

        for file in sorted(self.yaml_files):
            try:
                info = self.assignments_folder + '/' + file
                with open(info, 'r') as info:
                    file_info = yaml.load(info, Loader=yaml.FullLoader)

                    name = file_info['name']
                    due_date = file_info['due_date']
                    submitted = file_info['submitted']

                    assignments_name.append(name)
                    assignments_due_dates.append(due_date)
                    assignments_submitted.append(submitted)
            except Exception:
                pass

        return assignments_name, assignments_due_dates, assignments_submitted

    def get_assignments_ready_to_be_viewed(self):
        """
        This function will transform the list of assignments we already have
        and turn it into a pretty list that we can display.
        """

        options = []

        for assignment_number, assignment_name, assignment_due_date, \
                assignment_submitted in zip(self.assignments,
                                            self.assignments_name,
                                            self.assignments_due_dates,
                                            self.assignments_submitted):
            assignment_number = assignment_number[5:-4]
            fancy_assignment_style = ''

            logo, due_date_formatted = utils.check_if_assignment_is_due(
                    assignment_due_date, assignment_submitted)

            color = 'green'
            submit = 'Yes'

            if not assignment_submitted:
                color = 'red'
                submit = 'No'
                due_date_formatted += logo

            fancy_assignment_style = \
                "<span color='red'>{number: >2}</span>. " \
                "<b><span color='blue'>{title: <{fill}}</span>" \
                "</b> <i><span color='yellow' size='smaller'> Due By: " \
                "{date: <{fill}}</span></i> <i><span color='{color}'>" \
                "Submitted: {submit}</span></i>".format(
                    fill=24,
                    number=assignment_number,
                    title=assignment_name,
                    date=due_date_formatted,
                    color=color,
                    submit=submit
                )

            options.append(fancy_assignment_style)

        return options


def main():
    """ This function will run the program """

    assignment = ViewAssignments()

    key, index, selected = utils.rofi('Select Assignment', assignment.options,
                                      assignment.rofi_options)
    assignment_file = assignment.assignments[index]

    second_key, second_index, second_selected = utils.rofi(
            'Which One', assignment.second_options, assignment.rofi_options)

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
