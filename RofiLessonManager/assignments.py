#!/usr/bin/env python3

from rofi import Rofi
from glob import glob
from natsort import natsorted
import os
import yaml

from RofiLessonManager import Basis as Basis
import RofiLessonManager.utils as utils


class Assignment(Basis):
    def __init__(self, path):
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

        self.number, self.title, \
            self.due_date, self.submit = self.get_info()

    def parse_command(self, cmd):
        if cmd == 'edit_latex':
            os.system('xfce4-terminal -e "nvim {}/week-{}.tex"'.format(
                self.assignments_latex_folder, self.number))
        elif cmd == 'edit_yaml':
            os.system('xfce4-terminal -e "nvim {}/week-{}.yaml"'.format(
                self.assignments_latex_folder, self.number))
        elif cmd == 'open_pdf':
            if not os.path.exists(
                    '{}/week-{}.pdf'.format(
                        self.assignments_pdf_folder, self.number)):
                utils.error_message(
                    'No PDF file found for assignment number {}'.format(
                        self.number))
                exit(1)

            os.system('zathura {}/week-{}.pdf'.format(
                self.assignments_pdf_folder, self.number))

    def new(self):
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

    def get_info(self):
        due_date = self.info['due_date']
        submit = self.info['submitted']
        title = utils.generate_short_title(self.info['name'],
                                           22)
        number = self.name[5:-4]

        logo, due_date, late = utils.check_if_assignment_is_due(
            due_date, submit)

        submit = 'Yes'

        if not submit and late:
            submit = 'No'
            due_date += logo
        elif not submit:
            submit = 'No'
            due_date += logo

        due_date = utils.generate_short_title(
            due_date, 28)

        return number, title, due_date, submit

    def __str__(self):
        return '<Assignment: {}. {} Due By: {}>'.format(self.number, self.name,
                                                        self.info['due_date'])

    def __eq__(self, other):
        return self.number == other.number


class Assignments(Basis, list):
    def __init__(self):
        Basis.__init__(self)
        list.__init__(self, self.read_files())
        self.names = [a.name for a in self]

        self.second_options = [
            '<span color="yellow">View Assignment LaTeX</span>',
            '<span color="yellow">View Assignment Yaml</span>',
            '<span color="yellow">View Assignment PDF</span>'
        ]

    def read_files(self):
        assignments = glob('{}/*.tex'.format(self.assignments_latex_folder))
        assignments = natsorted(assignments)
        return [Assignment(a) for a in assignments]

    def __len__(self):
        return len(self)
