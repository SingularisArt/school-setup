#!/usr/bin/env python3

from glob import glob
import os
import yaml

from RofiLessonManager import Basis as Basis
import RofiLessonManager.utils as utils


class Assignment(Basis):
    def __init__(self, path):
        Basis.__init__(self)

        self.path = path
        self.name = os.path.basename(path)
        info_file_name = self.name.replace('tex', 'yaml')
        info = open('{}/{}'.format(self.assignments_folder, info_file_name))
        self.info = yaml.load(info, Loader=yaml.FullLoader)

    def __str__(self):
        return '<Assignment: {}>'.format(self.name)


class Assignments(Basis, list):
    def __init__(self):
        Basis.__init__(self)
        list.__init__(self, self.read_files())
        self.names = [a.name for a in self]
        self.rofi_names = self.get_rofi_names()
        print(self.rofi_names)

        self.second_options = [
                '<span color="yellow">View Assignment LaTeX</span>',
                '<span color="yellow">View Assignment Yaml</span>',
                '<span color="yellow">View Assignment PDF</span>'
                              ]

    def read_files(self):
        assignments = glob('{}/*.tex'.format(self.assignments_folder))
        return sorted((Assignment(a) for a in assignments),
                      key=lambda a: a.name)

    def get_rofi_names(self):
        """
        This function will transform the list of assignments we already have
        and turn it into a pretty list that we can display.
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
        return len(self)
