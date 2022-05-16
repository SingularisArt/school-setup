#!/usr/bin/env python3

"""
This module contains the RofiLessonManager.assignments.Assignment and
RofiLessonManager.assignments.Assignments classes.

Class Assignment:
    - RofiLessonManager.Assignment

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific assignment.
    For example: Assignment(path-to-assignment). Then, it has all the
    information on that assignment from the assignment's yaml file,
    respectively.

    Args:
        - path (str): The path to the assignment.

    Attributes:
        - path (str): The path to the assignment.
        - name (str): The name of the assignment, which is the name of the
            file.
        - info (json): The information from the yaml file.

    Methods:
        - edit_latex: Opens the tex file of the assignment.

        - edit_yaml: Opens the yaml file of the assignment.

        - open_pdf: Opens the pdf file of the assignment.

        - new: Creates a new assignment.

        - __str__: Returns a string representation of the Assignment object.

            Returns:
                - str: A string representation of the Assignment object.

        - __eq__: Checks if two lectures are equal.

            Args:
                - other (Lecture): Lecture to compare with.

            Returns:
                - bool: True if equal, False otherwise.

Class Assignments:
    - RofiLessonManager.Assignments

    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class holds a list of all the assignments, which are located in the
    assignments folder, which can be modified from the config.yaml file. Each
    assignment is an instance from the
    RofiLessonManager.assignments.Assignment.

    Attributes:
        - names (list): A list of names for all the assignments.
        - rofi_names (list): A list of names for rofi to display.
        - second_options (list): The commands for Rofi to display for the user
            to select.

    Methods:
        - read_files: Reads all the files in the assignments folder and returns
            a list of Assignment objects.

            Returns:
                - assignments (list): A list of Assignment objects.

        - get_rofi_names: Returns a list of names for rofi to display.

            Returns:
                - options (list): A list of names for rofi to display.

        - __len__: Gets the number of assignments.

            Returns:
                - int: The number of assignments.
"""


from rofi import Rofi
from glob import glob
from natsort import natsorted
import os
import yaml

from RofiLessonManager import Basis as Basis
import RofiLessonManager.utils as utils


class Assignment(Basis):
    """
    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific assignment.
    For example: Assignment(path-to-assignment). Then, it has all the
    information on that assignment from the assignment's yaml file,
    respectively.

    Args:
        - path (str): The path to the assignment.

    Attributes:
        - path (str): The path to the assignment.
        - name (str): The name of the assignment, which is the name of the
            file.
        - info (json): The information from the yaml file.

    Methods:
        - edit_latex: Opens the tex file of the assignment.

        - edit_yaml: Opens the yaml file of the assignment.

        - open_pdf: Opens the pdf file of the assignment.

        - new: Creates a new assignment.

        - __str__: Returns a string representation of the Assignment object.

            Returns:
                - str: A string representation of the Assignment object.

        - __eq__: Checks if two lectures are equal.

            Args:
                - other (Lecture): Lecture to compare with.

            Returns:
                - bool: True if equal, False otherwise.
    """

    def __init__(self, path):
        """
        Initializes the Assignment object.

        Args:
            path (str): The path to the assignment.
        """

        Basis.__init__(self)

        self.path = path

        if not os.path.exists(self.path):
            self.new()

        self.name = os.path.basename(path)
        self.number = self.name.replace(
            'week-', '').replace('.yaml', '').replace('.tex', '')
        info_file_name = self.name.replace('tex', 'yaml')
        info = open('{}/{}'.format(self.assignments_latex_folder,
                                   info_file_name))
        self.info_file = '{}/{}'.format(self.assignments_latex_folder,
                                        info_file_name)
        self.info = yaml.load(info, Loader=yaml.FullLoader)
        self.title = self.info['name']

    def edit_latex(self):
        """ Opens the tex file of the assignment. """

        os.system('xfce4-terminal -e "nvim {}/week-{}.tex"'.format(
            self.assignments_latex_folder, self.number))

    def edit_yaml(self):
        """ Opens the yaml file of the assignment. """

        os.system('xfce4-terminal -e "nvim {}/week-{}.yaml"'.format(
            self.assignments_latex_folder, self.number))

    def open_pdf(self):
        """ Opens the pdf file of the assignment. """

        if not os.path.exists('zathura {}/week-{}.pdf'.format(
            self.assignments_pdf_folder, self.number
        )):
            utils.error_message(
                'No PDF file found for assignment number {}'.format(
                    self.number))
            exit(1)

        os.system('zathura {}/week-{}.pdf'.format(
            self.assignments_pdf_folder, self.number))

    def new(self):
        """ Creates a new assignment. """

        rofi = Rofi()
        title = rofi.text_entry('Title')
        due_date = rofi.date_entry('Due Date (ex: 05-30-22)',
                                   formats=['%m-%d-%y'])
        due_date = due_date.strftime('%m-%d-%y')
        _, _, selected = utils.rofi('Submitted', ['Yes', 'No'])

        yaml_file = self.path.replace('.tex', '.yaml')

        with open(self.path, 'x') as file:
            pass
        with open(yaml_file, 'x') as file:
            pass

        with open(yaml_file, 'w') as file:
            file.write('name: {}\n'.format(title))
            file.write('due_date: {}\n'.format(due_date))
            file.write('submitted: {}\n'.format(selected))

    def __str__(self):
        """
        Returns a string representation of the Assignment object.

        Returns:
            - str: A string representation of the Assignment object.
        """

        return '<Assignment: {}. {} Due By: {}>'.format(self.number, self.name,
                                                        self.info['due_date'])

    def __eq__(self, other):
        """
        Checks if two lectures are equal.
        Args:
            - other (Lecture): Lecture to compare with.
        Returns:
            - bool: True if equal, False otherwise.
        """

        return self.number == other.number


class Assignments(Basis, list):
    """
    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class holds a list of all the assignments, which are located in the
    assignments folder, which can be modified from the config.yaml file. Each
    assignment is an instance from the
    RofiLessonManager.assignments.Assignment.

    Attributes:
        - names (list): A list of names for all the assignments.
        - rofi_names (list): A list of names for rofi to display.
        - second_options (list): The commands for Rofi to display for the user
            to select.

    Methods:
        - read_files: Reads all the files in the assignments folder and returns
            a list of Assignment objects.

            Returns:
                - assignments (list): A list of Assignment objects.

        - get_rofi_names: Returns a list of names for rofi to display.

            Returns:
                - options (list): A list of names for rofi to display.

        - __len__: Gets the number of assignments.

            Returns:
                - int: The number of assignments.
    """

    def __init__(self):
        """ Initializes the class. """

        Basis.__init__(self)
        list.__init__(self, self.read_files())
        self.names = [a.name for a in self]
        self.rofi_names = self.get_rofi_names()

        self.second_options = [
            '<span color="yellow">View Assignment LaTeX</span>',
            '<span color="yellow">View Assignment Yaml</span>',
            '<span color="yellow">View Assignment PDF</span>'
        ]

    def read_files(self):
        """
        Reads all the files in the assignments folder and returns a list of
        Assignment objects.

        Returns:
            - assignments (list): A list of Assignment objects.
        """

        assignments = glob('{}/*.tex'.format(self.assignments_latex_folder))
        assignments = natsorted(assignments)
        return [Assignment(a) for a in assignments]

    def get_rofi_names(self):
        """
        Returns a list of names for rofi to display.

        Returns:
            - options (list): A list of names for rofi to display.
        """

        options = []

        for project in self:
            assignment_due_date = project.info['due_date']
            assignment_submitted = project.info['submitted']
            assignment_name = utils.generate_short_title(project.info['name'],
                                                         22)
            assignment_number = project.name[5:-4]

            fancy_assignment_style = ''

            logo, due_date_formatted, late = utils.check_if_assignment_is_due(
                assignment_due_date, assignment_submitted)

            color = 'green'
            submit = 'Yes'

            if not assignment_submitted and late:
                color = 'red'
                submit = 'No'
                due_date_formatted += logo
            elif not assignment_submitted:
                color = 'purple'
                submit = 'No'
                due_date_formatted += logo

            due_date_formatted = utils.generate_short_title(
                due_date_formatted, 28)

            fancy_assignment_style = \
                "<span color='red'>{number: >2}</span>. " \
                "<b><span color='blue'>{title: <{fill}}</span>" \
                "</b> <i><span color='yellow' size='smaller'> Due By: " \
                "{date: <{fill_2}}</span></i> <i><span color='{color}'>" \
                "Submitted: {submit}</span></i>".format(
                    fill=22,
                    number=assignment_number,
                    title=assignment_name,
                    date=due_date_formatted,
                    color=color,
                    submit=submit,
                    fill_2=27,
                )

            options.append(fancy_assignment_style)

        return options

    def __len__(self):
        """
        Gets the number of assignments.

        Returns:
            - int: The number of assignments.
        """

        return len(self)
