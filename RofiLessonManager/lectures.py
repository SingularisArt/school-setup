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


from rofi import Rofi
import os
from datetime import datetime
from glob import glob
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

        self.file_path = file_path

        if not os.path.isfile(file_path):
            self.new()

        with open(file_path) as f:
            for line in f:
                lecture_match = re.search(self.lecture_regex, line)
                if lecture_match:
                    break

        date_str = lecture_match.group(2)
        date = datetime.strptime(date_str, self.date_format)
        week = utils.get_week(date)
        title = lecture_match.group(3)

        self.date_str = date_str
        self.date = date
        self.week = week
        self.number = utils.filename2number(os.path.basename(file_path))
        self.title = title

    def edit(self):
        """ Edits the lecture. """

        listen_location = '/tmp/nvim.pipe'
        args = []

        if os.path.exists(listen_location):
            args = ['--server', '/tmp/nvim.pipe', '--remote']
        elif not os.path.exists(listen_location):
            args = ['--listen', '/tmp/nvim.pipe']
        args = ' '.join(str(e) for e in args if e)
        print(args)

        os.system('xfce4-terminal -e "nvim {} {}/lectures/lec-{}.tex"'.format(
            args, self.current_course, self.number))

    def new(self):
        """ Creates the lecture if it doesn't exist. """

        rofi = Rofi()
        title = rofi.text_entry('Title')
        date = datetime.now().strftime(self.date_format)
        number = utils.filename2number(os.path.basename(self.file_path))

        template = [fr'\lesson{{{number}}}{{{date}}}{{{title}}}',
                    '',
                    '',
                    '',
                    r'\newpage']

        with open(self.file_path, 'w') as f:
            f.write('\n'.join(template))

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

    def read_files(self):
        """
        Reads all the lecture files and returns a list of Lecture objects.
        Returns:
            - list: List of Lecture objects.
        """

        files = glob('{}/lectures/*.tex'.format(self.current_course))
        return sorted((Lecture(f) for f in files), key=lambda l: l.number)

    def parse_lecture_spec(self, string):
        if len(self) == 0:
            return 0

        if string.isdigit():
            return int(string)
        elif string == 'last':
            return self[-1].number
        elif string == 'prev':
            return self[-2].number

    def parse_range_string(self, arg):
        all_numbers = [lecture.number for lecture in self]

        if 'all' in arg:
            return all_numbers
        if 'prev_last' == arg:
            return all_numbers[-2:]
        if 'prev' == arg:
            return all_numbers[:-1]
        if '-' in arg:
            start, end = arg.split('-')
            return list(range(int(start), int(end)+1))

        return [self.parse_lecture_spec(arg)]

    def update_lectures_in_master(self, r):
        body = ''.join(r'\input{lectures/' +
                       utils.number2filename(number) + '}\n' for number in r)
        with open(self.source_lectures_location, 'w') as f:
            f.write(body)

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
