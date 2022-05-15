#!/usr/bin/env python3

"""
This module contains the RofiLessonManager.Lecture and
RofiLessonManager.Lectures classes.

Class Lecture:
    - RofiLessonManager.Lecture

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific lecture. For
    example: Lecture(path-to-lecture). Then, it has all the information on that
    lecture from the lecture's yaml file, respectively.

    Attributes:
        - file_path (str): Path to the lecture file.
        - date_str (str): Date of the lecture as a string.
        - date (datetime.datetime): Date of the lecture as a datetime object.
        - week (int): Number of week when the lecture notes were written.
        - number (int): Number of the lecture.
        - title (str): Title of the lecture.
        - rofi_title (str): Title of the lecture as a fancy string for rofi.

    Args:
        - file_path (str): Path to the lecture file.

    Methods:
        - edit: Edits the lecture.

        - __str__: Returns the lecture as a string.

            Returns:
                - str: Lecture as a string.

        - __eq__: Checks if two lectures are equal.

            Args:
                - other (Lecture): Lecture to compare with.

            Returns:
                - bool: True if equal, False otherwise.

Class Lectures:
    - RofiLessonManager.Lectures

    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the List class.

    This class holds a list of all the lectures, which are located in the
    lectures folder, which can be modified from the config.yaml file. Each
    lecture is an instance from the RofiLessonManager.lectures.Lecture class.

    Attributes:
        - rofi_titles (list): List of titles for rofi.
        - titles (list): List of titles.

    Args:
        - file_path (str): Path to the lecture file.

    Methods:
        - read_files: Reads all the lecture files and returns a list of Lecture
            objects.

            Returns:
                - list: List of Lecture objects.

        - compile_master: Compiles the master file.

            Returns:
                - int: 0 if successful, 1 otherwise.

        - __len__: Gets the number of lectures.

            Returns:
                - int: Number of lectures.
"""


import os
from datetime import datetime
from glob import glob
import sys
import locale
import re
import subprocess

from RofiLessonManager import Basis as Basis
import RofiLessonManager.utils as utils


locale.setlocale(locale.LC_TIME, "en_US.utf8")


class Lecture(Basis):
    """
    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific lecture. For
    example: Lecture(path-to-lecture). Then, it has all the information on that
    lecture from the lecture's yaml file, respectively.

    Attributes:
        - file_path (str): Path to the lecture file.
        - date_str (str): Date of the lecture as a string.
        - date (datetime.datetime): Date of the lecture as a datetime object.
        - week (int): Number of week when the lecture notes were written.
        - number (int): Number of the lecture.
        - title (str): Title of the lecture.
        - rofi_title (str): Title of the lecture as a fancy string for rofi.

    Args:
        - file_path (str): Path to the lecture file.

    Methods:
        - edit: Edits the lecture.

        - __str__: Returns the lecture as a string.

            Returns:
                - str: Lecture as a string.

        - __eq__: Checks if two lectures are equal.

            Args:
                - other (Lecture): Lecture to compare with.

            Returns:
                - bool: True if equal, False otherwise.
    """

    def __init__(self, file_path):
        """
        Initializes the class.

        Args:
            file_path (str): Path to the lecture file.
        """

        Basis.__init__(self)

        with open(file_path) as f:
            for line in f:
                lecture_match = re.search(self.lecture_regex, line)
                if lecture_match:
                    break

        date_str = lecture_match.group(2)
        date = datetime.strptime(date_str, self.date_format)
        week = utils.get_week(date)
        title = lecture_match.group(3)

        self.file_path = file_path
        self.date_str = date_str
        self.date = date
        self.week = week
        self.number = utils.filename2number(os.path.basename(file_path))
        self.title = title

        self.rofi_title = "<span color='red'>{number: >2}</span>. " \
            "<b><span color='blue'>{title: <{fill}}</span>" \
            "</b> <i><span color='yellow' size='smaller'>" \
            "{date: <{fill}}</span></i><b>({week})</b>".format(
                fill=35,
                number=self.number,
                title=utils.generate_short_title(self.title),
                date=utils.generate_short_title(self.date_str),
                week=self.week
            )

    def edit(self):
        """ Edits the lecture. """

        os.system('xfce4-terminal -e "nvim {}/lectures/lec-{}.tex"'.format(
            self.current_course, self.number))

    def __str__(self):
        """
        Returns the lecture as a string.

        Returns:
            - str: Lecture as a string.
        """

        return '<Lecture Title: {}" {} {}>'.format(
            self.title, self.number, self.week
        )

    def __eq__(self, other):
        """
        Checks if two lectures are equal.

        Args:
            - other (Lecture): Lecture to compare with.

        Returns:
            - bool: True if equal, False otherwise.
        """

        return self.number == other.number


class Lectures(Basis, list):
    """
    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the List class.

    This class holds a list of all the lectures, which are located in the
    lectures folder, which can be modified from the config.yaml file. Each
    lecture is an instance from the RofiLessonManager.lectures.Lecture class.

    Attributes:
        - rofi_titles (list): List of titles for rofi.
        - titles (list): List of titles.

    Args:
        - file_path (str): Path to the lecture file.

    Methods:
        - read_files: Reads all the lecture files and returns a list of Lecture
            objects.

            Returns:
                - list: List of Lecture objects.

        - compile_master: Compiles the master file.

            Returns:
                - int: 0 if successful, 1 otherwise.

        - __len__: Gets the number of lectures.

            Returns:
                - int: Number of lectures.
    """

    def __init__(self):
        """ Initializes the class. """

        Basis.__init__(self)

        list.__init__(self, self.read_files())
        self.titles = [lec.title for lec in self]
        self.rofi_titles = [lec.rofi_title for lec in self]

        # Check if we have any lectures
        # If we don't, just give an error and return
        if not self:
            utils.error_message('No lectures found')
            sys.exit(1)

    def read_files(self):
        """
        Reads all the lecture files and returns a list of Lecture objects.

        Returns:
            - list: List of Lecture objects.
        """

        files = glob('{}/lectures/*.tex'.format(self.current_course))
        return sorted((Lecture(f) for f in files), key=lambda l: l.number)

    def compile_master(self):
        """
        Compiles the master file.

        Returns:
            - int: 0 if successful, 1 otherwise.
        """

        result = subprocess.run(
            ['pdflatex', str(self.master_file)],
            cwd=str(self.current_course)
        )

        if result.returncode == 0:
            utils.success_message('Compilation successful')
        else:
            utils.error_message('Compilation failed')

        return result.returncode

    def __len__(self):
        """
        Gets the number of lectures.

        Returns:
            - int: Number of lectures.
        """

        return len(self.read_files())
