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
        path (str): The path to the project.
        chapters (list): A list of chapters.
        info (dict): The project's info from the info.yaml file.
        info_file (str): The path to the info.yaml file.
        name (str): The name of the project.
        status (str): The status of the project.
        rofi_name (str): The name of the project for rofi.

    Args:
        - path (str): The path to the project.

    Methods:
        - get_status: Returns the status of the project.

            Returns:
                str: The status of the project.

        - open_pdf: Opens the project's pdf.

        - open_source: Opens the project's source folder.

        - open_notes: Opens the project's notes.

        - open_chapter: Opens a chapter.

            Args:
                - n (int): The chapter number.

        - get_chapters: Returns a list of chapters.

            Returns:
                - list: A list of chapters.

        - add_chapter: Adds a chapter to the project.

            Args:
                - n (int): The chapter number.

        - remove_chapter: Removes a chapter from the project.

        - source_chapter: Sources a chapter.

        - copy_pdf_to_drive: Copies the project's pdf.

            Args:
                - user (str): The user's name.

        - mark_project: Marks a project.

            Args:
                - status (str): The status of the project.

        - delete: Deletes the project.

        - __str__: Returns a string representation of the project.

            Returns:
                str: A string representation of the project.

Class Projects:
    - RofiLessonManager.projects.Projects

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
                - index (int): The index of the project.
"""

from glob import glob
from rofi import Rofi
import os
import yaml

from RofiLessonManager import Basis
import RofiLessonManager.utils as utils


class Project(Basis):
    """
    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific project. For
    example: Project(path-to-project). Then, it has all the information on that
    project from the project's yaml file, respectively.

    Attributes:
        path (str): The path to the project.
        chapters (list): A list of chapters.
        info (dict): The project's info from the info.yaml file.
        info_file (str): The path to the info.yaml file.
        name (str): The name of the project.
        status (str): The status of the project.
        rofi_name (str): The name of the project for rofi.

    Args:
        - path (str): The path to the project.

    Methods:
        - get_status: Returns the status of the project.

            Returns:
                str: The status of the project.

        - open_pdf: Opens the project's pdf.

        - open_source: Opens the project's source folder.

        - open_notes: Opens the project's notes.

        - open_chapter: Opens a chapter.

            Args:
                - n (int): The chapter number.

        - get_chapters: Returns a list of chapters.

            Returns:
                - list: A list of chapters.

        - add_chapter: Adds a chapter to the project.

            Args:
                - n (int): The chapter number.

        - remove_chapter: Removes a chapter from the project.

        - source_chapter: Sources a chapter.

        - copy_pdf_to_drive: Copies the project's pdf.

            Args:
                - user (str): The user's name.

        - mark_project: Marks a project.

            Args:
                - status (str): The status of the project.

        - delete: Deletes the project.

        - __str__: Returns a string representation of the project.

            Returns:
                str: A string representation of the project.
    """

    def __init__(self, path):
        """
        Initializes the class.

        Args:
            path (str): The path to the project.
        """

        Basis.__init__(self)

        self.path = path
        self.chapters = self.get_chapters()

        info_file_name = '{}/info.yaml'.format(self.path)
        info = open(info_file_name)

        self.info = yaml.load(info, Loader=yaml.FullLoader)
        self.info_file = info_file_name
        self.name = utils.generate_short_title(self.info['name'], 20)
        self.status = self.get_status()

        if self.status == 'complete':
            self.status = 'Completed'
            self.status_color = '#00FF00'
        elif self.status == 'incomplete':
            self.status = 'Incomplete'
            self.status_color = '#FF0000'

        self.rofi_name = \
            '<span color="#0000FF">{name: <{fill}}</span>'.format(
                name=self.name, fill=10) + \
            '<span color="#FFFF00">Status: </span>' + \
            '<b><span color="{color}">{status}</span></b>'.format(
                color=self.status_color,
                status=self.status
            )

    def get_status(self):
        """
        Returns the status of the project.

        Returns:
            str: The status of the project.
        """

        with open('{}/status.txt'.format(self.path), 'r') as f:
            return f.read()

    def open_pdf(self):
        """ Opens the project's pdf. """

        os.system('zathura {}/master.pdf'.format(
            self.path))

    def open_source(self):
        """ Opens the project's source folder. """

        # Open source code
        os.system('xfce4-terminal -e "nvim {}"'.format(self.path))

    def open_notes(self):
        """ Opens the project's notes. """

        os.system('xfce4-terminal -e "nvim {}/notes.md"'.format(self.path))

    def open_chapter(self, n):
        """
        Opens a chapter.

        Args:
            n (int): The chapter number.
        """

        os.system('xfce4-terminal -e "nvim {}/chapters/chap-{}.tex"'.format(
            self.path, n))

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

        # Ask the user if they would like to open the new chapter
        key, index, selected = utils.rofi('Open new chapter?', ['Yes', 'No'])

        if selected == 'Yes':
            self.open_chapter(n)
        else:
            utils.success_message('Chapter added')

    def remove_chapter(self):
        """ Removes a chapter from the project. """

        rofi = Rofi()
        n = rofi.integer_entry('Enter chapter number')

        try:
            os.remove('{}/chapters/chap-{}.tex'.format(self.path, n))
            utils.success_message('Chapter removed')
        except Exception:
            utils.error_message('Chapter not found')

    def source_chapter(self):
        """ Sources a chapter. """

        if len(self.chapters) == 0:
            utils.error_message('No available chapters')
            return

        rofi = Rofi()
        n = rofi.integer_entry('Enter chapter number (or range: 1-{})'.format(
            len(self.chapters)
        ))

        source_chapters_path = '{}/source-chapters.tex'.format(self.path)
        chapter_path = '{}/chapters/chap-{}.tex'.format(self.path, n)

        if not os.path.exists(chapter_path):
            utils.error_message('Chapter does not exist.')
            return

        with open(source_chapters_path, 'a') as file:
            file.write('\\input{chapters/chap-' + str(n) + '}')

        utils.success_message('Chapter sourced')

    def copy_pdf_to_drive(self, user):
        """
        Copies the project's pdf.

        Args:
            - user (str): The user's name.
        """

        drives, drives_with_style = utils.get_flash_drives(user)

        # Ask the user which drive to use via rofi
        key, index, selected = utils.rofi('Select command',
                                          drives_with_style,
                                          self.rofi_options)

        master_path = '{}/master.pdf'.format(self.path)
        drive_path = '/run/media/{}/{}/'.format(
            user, drives[index]).replace(' ', '\\ ')

        try:
            os.system('cp {} {}'.format(master_path, drive_path))
        except Exception:
            rofi = Rofi()
            rofi.error('Couldn\'t move master.pdf to {}'.format(drive_path))
            exit(1)

        utils.success_message('Copied master.pdf to {}'.format(drive_path))

    def mark_project(self, status):
        """
        Marks a project.

        Args:
            - status (str): The status of the project.
        """

        with open('{}/status.txt'.format(self.path), 'w') as f:
            f.write(status)

    def delete(self):
        """ Deletes the project. """

        os.removedirs(self.path)
        utils.success_message('Project deleted')

    def __str__(self):
        """
        Returns a string representation of the project.

        Returns:
            str: A string representation of the project.
        """

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
                - index (int): The index of the project.
    """

    def __init__(self):
        """ Initializes the class. """

        Basis.__init__(self)
        list.__init__(self, self.read_files())
        self.names = [p.name for p in self]
        self.rofi_names = []

        for x, p in enumerate(self):
            fancy_name = '<span color="#FF0000">{}.</span> {}'.format(
                x + 1, p.rofi_name)
            self.rofi_names.append(fancy_name)

        self.commands = [
            '<span color="purple">Open PDF</span>',
            '<span color="purple">Open Source</span>',
            '<span color="blue">Open Notes</span>',
            '<span color="blue">New Chapter</span>',
            '<span color="blue">Remove a Chapter</span>',
            '<span color="blue">Source Chapter(s)</span>',
            '<span color="brown">Copy PDF to flash drive</span>',
            '<span color="green">Mark as Complete</span>',
            '<span color="green">Mark as Incomplete</span>',
            '<span color="red">Delete</span>'
        ]

    def read_files(self):
        """
        This function reads the files in the projects directory.

        Returns:
            - list: A list of Project objects for each project.
        """

        projects = glob('{}/*'.format(self.projects_dir))
        return sorted((Project(f) for f in projects), key=lambda c: c.name)

    def run_func_based_on_command(self, command, index):
        """
        This function runs the function based on the command.

        Args:
            - command (str): The command.
            - index (int): The index of the project.
        """

        # Run the function based on the command
        if command == self.commands[0]:
            self[index].open_pdf()
        elif command == self.commands[1]:
            self[index].open_source()
        elif command == self.commands[2]:
            self[index].open_notes()
        elif command == self.commands[3]:
            self[index].add_chapter(len(self[index].chapters) + 1)
        elif command == self.commands[4]:
            self[index].remove_chapter()
        elif command == self.commands[5]:
            self[index].source_chapter()
        elif command == self.commands[6]:
            self[index].copy_pdf_to_drive(self.user)
        elif command == self.commands[7]:
            self[index].mark_project('complete')
        elif command == self.commands[8]:
            self[index].mark_project('incomplete')
        elif command == self.commands[9]:
            self[index].delete()
