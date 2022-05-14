#!/usr/bin/env python3

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


def number2filename(n):
    return 'lec_{}.tex'.format(n)


def filename2number(s):
    return int(str(s).replace('.tex', '').replace('lec-', ''))


class Lecture(Basis):
    """
    Attributes:
        file_path:  Path to the lecture file.
        date_str:   Date of the lecture.
        date:       Date of the lecture, which isn't meant to be outputted.
                        This date is used to get the week number of theme
                        lecture.
        week:       Week number of the lecture.
        number:     Number of the lecture.
        title:      Title of the lecture.
        rofi_title: Title of the lecture, which is meant to be outputted via
                    rofi.

    Methods:
        -----------------------------------------------------------------------
        | edit: Edit the lecture file.                                        |
        -----------------------------------------------------------------------
    """

    def __init__(self, file_path):
        """
        Initialize the Lecture object.

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
        self.number = filename2number(os.path.basename(file_path))
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
        """
        Edit the lecture file
        """

        os.system('xfce4-terminal -e "nvim {}/lectures/lec-{}.tex"'.format(
            self.current_course, self.number))

    def __str__(self):
        """
        Return a string representation of the lecture

        Returns:
            str: String representation of the lecture
        """

        return '<Lecture Title: {}" {} {}>'.format(
            self.title, self.number, self.week
        )


class Lectures(Basis, list):
    """
    Inheritance:
        This class inherits from the RofiLessonManager.Basis class.
        This class inherits from the list class.

    This class is a list of Lecture objects.

    Attributes:
        rofi_titles: A list of all the lectures in the current course, which
                     will be passed to rofi for the user to select one.

    Methods:
        -----------------------------------------------------------------------
        | read_files: Reads all the files in the lectures directory and       |
        |             returns a list of Lecture objects.                      |
        |                                                                     |
        | Returns:                                                            |
        |     A list of Lecture objects.                                      |
        -----------------------------------------------------------------------

        -----------------------------------------------------------------------
        | compile_master: Compiles the master file.                           |
        |                                                                     |
        | Returns:                                                            |
        |   The code returned by the compilation process.                     |
        |   0 if the compilation was successful.                              |
        |   1 if the compilation failed.                                      |
        -----------------------------------------------------------------------
    """

    def __init__(self):
        """ Initialize the Lectures object """

        Basis.__init__(self)

        list.__init__(self, self.read_files())
        self.rofi_titles = [lec.rofi_title for lec in self]

        # Check if we have any lectures
        # If we don't, just give an error and return
        if not self:
            utils.error_message('No lectures found')
            sys.exit(1)

    def read_files(self):
        """
        Reads all the files in the lectures directory and returns a list of
        Lecture objects.

        Returns:
            A list of Lecture objects.
        """

        files = glob('{}/lectures/*.tex'.format(self.current_course))
        return sorted((Lecture(f) for f in files), key=lambda l: l.number)

    def compile_master(self):
        """
        Compiles the master file.

        Returns:
            The code returned by the compilation process.
            0 if the compilation was successful.
            1 if the compilation failed.
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
        return len(self.read_files())
