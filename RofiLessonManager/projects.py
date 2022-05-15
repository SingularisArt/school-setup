#!/usr/bin/env python3

"""
This module contains the RofiLessonManager.projects.Project and
RofiLessonManager.projects.Projects classes.

Class Project:
    - RofiLessonManager.projects.Project

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific project. For
    example: Project(path-to-project). Then, it has all the information on that
    project from the project's yaml file, respectively.

    Attributes:
        - path (str): The path to the project.
        - name (str): The name of the project.
        - chapters (list): A list of chapters.

    Args:
        - path (str): The path to the project.

    Methods:
        - get_chapters: Returns a list of chapters.

            Returns:
                - list: A list of chapters.

        - add_chapter: Adds a chapter to the project.

            Args:
                - n (int): The chapter number.

        - remove_chapter: Removes a chapter from the project.

            Args:
                - n (int): The chapter number.

Class Projects:
    - RofiLessonManager.projects.Projects

    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class holds a list of all the projects, which are located in the
    projects folder, which can be modified from the config.yaml file. Each
    project is an instance from the RofiLessonManager.projects.Project class.

    Attributes:
        - names (list): A list of project names.
        - rofi_names (list): A list of project names formatted for rofi.
        - commands (list): A list of commands for the user to choose from.

    Methods:
        - read_files: This function reads the files in the projects directory.

            Returns:
                - list: A list of Project objects for each project.

        - run_func_based_on_command: This function runs the function based on
            the command.

            Args:
                - command (str): The command.
                - project_name (str): The name of the project.
"""

from glob import glob
import os
import sys

from RofiLessonManager import Basis
import RofiLessonManager.utils as utils


class Project(Basis):
    """
    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific project. For
    example: Project(path-to-project). Then, it has all the information on that
    project from the project's yaml file, respectively.

    Attributes:
        - path (str): The path to the project.
        - name (str): The name of the project.
        - chapters (list): A list of chapters.

    Args:
        - path (str): The path to the project.

    Methods:
        - get_chapters: Returns a list of chapters.

            Returns:
                - list: A list of chapters.

        - add_chapter: Adds a chapter to the project.

            Args:
                - n (int): The chapter number.

        - remove_chapter: Removes a chapter from the project.

            Args:
                - n (int): The chapter number.
    """

    def __init__(self, path):
        """
        Initializes the class.

        Args:
            path (str): The path to the project.
        """

        self.path = path
        self.name = os.path.basename(path)
        self.chapters = self.get_chapters()

    def get_chapters(self):
        """
        Returns a list of chapters.

        Returns:
            list: A list of chapters.
        """

        chapters = glob('{}/chapters/*.tex'.format(self.path))
        return sorted(chapters)

    def add_chapter(self, n):
        """
        Adds a chapter to the project.

        Args:
            n (int): The chapter number.
        """

        with open('{}/chapters/chap-{}.tex'.format(self.path, n), 'w') as f:
            f.write('')

    def remove_chapter(self, n):
        """
        Removes a chapter from the project.

        Args:
            n (int): The chapter number.
        """

        try:
            os.remove('{}/chapters/chap-{}.tex'.format(self.path, n))
        except Exception:
            pass

    def __str__(self):
        return '<Project: {}>'.format(self.name)


class Projects(Basis, list):
    """
    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class holds a list of all the projects, which are located in the
    projects folder, which can be modified from the config.yaml file. Each
    project is an instance from the RofiLessonManager.projects.Project.

    Attributes:
        - names (list): A list of project names.
        - rofi_names (list): A list of project names formatted for rofi.
        - commands (list): A list of commands for the user to choose from.

    Methods:
        - read_files: This function reads the files in the projects directory.

            Returns:
                - list: A list of Project objects for each project.

        - run_func_based_on_command: This function runs the function based on
            the command.

            Args:
                - command (str): The command.
                - project_name (str): The name of the project.
    """

    def __init__(self):
        """ Initializes the class. """

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
        """
        This function reads the files in the projects directory.

        Returns:
            - list: A list of Project objects for each project.
        """

        projects = glob('{}/*'.format(self.projects_dir))
        return sorted((Project(f) for f in projects), key=lambda c: c.name)

    def run_func_based_on_command(self, command, project_name):
        """
        This function runs the function based on the command.

        Args:
            - command (str): The command.
            - project_name (str): The name of the project.
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
