#!/usr/bin/env python3

"""
Author: Hashem Damrah
Date: 2020-04-24
"""

from glob import glob
import os
import sys

from RofiLessonManager import Basis
import RofiLessonManager.utils as utils


class Project(Basis):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.chapters = self.get_chapters()

    def get_chapters(self):
        chapters = glob('{}/chapters/*.tex'.format(self.path))
        return sorted(chapters)

    def add_chapter(self, n):
        with open('{}/chapters/chap-{}.tex'.format(self.path, n), 'w') as f:
            f.write('')

    def remove_chapter(self, n):
        try:
            os.remove('{}/chapters/chap-{}.tex'.format(self.path, n))
        except Exception:
            pass

    def __str__(self):
        return '<Project: {}>'.format(self.name)


class Projects(Basis, list):
    def __init__(self):
        Basis.__init__(self)
        list.__init__(self, self.read_files())
        self.names = [p.name for p in self]
        self.rofi_names = []

        for name in self.names:
            self.rofi_names.append('<span color="blue">{}</span>'.format(
                name
            ))

        self.commands = ['<span color="purple">Open PDF</span>',
                         '<span color="purple">Open Source</span>',
                         '<span color="blue">Open Notes</span>',
                         '<span color="blue">New Chapter</span>',
                         '<span color="brown">Copy PDF to flash drive</span>',
                         '<span color="green">Mark as Complete</span>',
                         '<span color="green">Mark as Incomplete</span>',
                         '<span color="red">Delete</span>',
                         '<span color="yellow">Exit</span>']

    def read_files(self):
        projects = glob('{}/*'.format(self.projects_dir))
        return sorted((Project(f) for f in projects), key=lambda c: c.name)

    def run_func_based_on_command(self, command, project_name):
        """
        This function runs the function based on the command.

        Args:
            command (str): The command.
            project_name (str): The name of the project.
        """

        # Run the function based on the command
        if command == self.commands[0]:
            utils.open_pdf(project_name, self.projects_dir)
        elif command == self.commands[1]:
            utils.open_source(project_name, self.projects_dir)
        elif command == self.commands[2]:
            utils.open_notes(project_name, self.projects_dir)
        elif command == self.commands[3]:
            utils.chapter(project_name, self.projects_dir, self.rofi_options)
        elif command == self.commands[4]:
            utils.copy_pdf(project_name, self.projects_dir, self.rofi_options,
                           self.user)
        elif command == self.commands[5]:
            utils.mark_project(project_name, 'complete', self.projects_dir)
        elif command == self.commands[6]:
            utils.mark_project(project_name, 'incomplete', self.projects_dir)
        elif command == self.commands[7]:
            utils.delete(project_name, self.projects_dir, self.rofi_options)
        elif command == self.commands[8]:
            sys.exit()
