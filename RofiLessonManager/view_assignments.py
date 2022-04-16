#!/usr/bin/env python3

import datetime
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

            logo = self.check_if_assignment_is_due(assignment_due_date,
                                                   assignment_submitted)

            if not assignment_submitted:
                fancy_assignment_style = \
                    "<span color='red'>{number: >2}</span>. " \
                    "<b><span color='blue'>{title: <{fill}}</span>" \
                    "</b> <i><span color='yellow' size='smaller'> Due By: " \
                    "{date: <{fill}}</span></i> <i><span color='red'>" \
                    "Submitted: {submitted}</span></i>".format(
                        fill=23,
                        number=assignment_number,
                        title=assignment_name,
                        date=assignment_due_date + logo,
                        submitted=assignment_submitted
                    )
            else:
                fancy_assignment_style = \
                    "<span color='red'>{number: >2}</span>. " \
                    "<b><span color='blue'>{title: <{fill}}</span>" \
                    "</b> <i><span color='yellow' size='smaller'> Due By: " \
                    "{date: <{fill}}</span></i> <i><span color='green'>" \
                    "Submitted: Yes</span></i>".format(
                        fill=23,
                        number=assignment_number,
                        title=assignment_name,
                        date=assignment_due_date,
                    )

            options.append(fancy_assignment_style)

        return options

    def check_if_assignment_is_due(self, assignment_due_date,
                                   assignment_submitted):
        now = datetime.datetime.now()
        assignment_date = datetime.datetime.strptime(assignment_due_date,
                                                     '%m-%d-%y')
        logo = ''

        # Check if the assignment is due today
        if now.date() == assignment_date.date():
            logo = ' (TODAY)'
        # Check if the assignment is due tomorrow
        elif now.date() + datetime.timedelta(days=1) == \
                assignment_date.date():
            logo = ' (TOMORROW)'
        # Check if the assignment is due in the past
        elif now.date() > assignment_date.date() and \
                not assignment_submitted:
            logo = ' (LATE)'
        else:
            days = int((assignment_date - now).days) + 1
            logo = ' (DAYS: {})'.format(days)

        return logo


def main():
    """ This function will run the program """

    assignment = ViewAssignments()

    key, index, selected = utils.rofi('Select Assignment', assignment.options,
                                      assignment.rofi_options)
    assignment_file = assignment.assignments[index]

    utils.open_file('xfce4-terminal', 'nvim', assignment.assignments_folder,
                    assignment_file, type='assignment')


if __name__ == "__main__":
    main()
