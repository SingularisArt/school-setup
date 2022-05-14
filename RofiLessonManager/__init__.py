"""
A simple gui interface for managing my school notes.
"""

import difflib
import os
from rofi import Rofi
from pathlib import Path

import RofiLessonManager.utils as utils


class Basis(object):
    """
    This is the basis class for all of the other classes.
    It has all of the default variables and methods.

    Attributes:
        data:                       The data from the config file.
        calendar_id:                The primary calendar id.
        code_dir:                   The directory where the source code is
                                        located.
        editor:                     The text editor that I will use to open
                                        files and folders.
        viewer:                     The pdf viewer that I will use to open
                                        pdf files.
        terminal:                   The terminal that I'll use to open the
                                        text editor with.
        notes_dir:                  The master directory where I store my
                                        notes.
        root:                       The directory where I store my class notes.
        current_course:             The directory where I store my current
                                        course symlink.
        projects_dir:               The directory where I store my projects.
        assignments_dir:            The directory where I store my assignments.
        assignments_folder:         The directory where I store my latex
                                        assignments.
        assignments_pdf_folder:     The directory where I store my pdf.
                                        assignments.
        yaml_extensions:            The extensions that I use for my yaml
                                        files.
        assignments:                The list of assignments that I have.
        yaml_files:                 The list of yaml files that I have.
        pdf_files:                  The list of pdf files that I have.
        source_lectures_location:   The location where I store my source
                                        lectures file.
        unit_info_name:             The name of the unit info file.
        new_chap:                   Variable that stores if there is a new
                                        chapter or not.
        home:                       The home directory of the user.
        user:                       The user that is logged in.
        lecture_regex:              The regex that I use to find the lecture
                                        information from the lecture files.
        rofi:                       The rofi object that I use to display my
                                        options.
        LESSON_RANGE_NUMBER:        The number of lessons that I check for.
        rofi_options:               The list that I pass to rofi for its
                                        configuration.
        tex_types:                  The list of tex types that I use.
        discourage_folders:         The list of folders that I don't want
                                        to show.
        placeholder:                The placeholder that I use when I change
                                        root directory.

    Methods:
        -----------------------------------------------------------------------
        | Gets the current location where I store my classes.                 |
        |                                                                     |
        | Returns:                                                            |
        |   placeholder (str): The current location where I store my classes. |
        -----------------------------------------------------------------------
    """

    def __init__(self):
        """
        Initializes the class.
        """

        # Load the data from the config file
        self.data = utils.load_data()

        # Assign the data to the variables
        self.calendar_id = self.data['calendar_id']
        self.code_dir = self.data['code_dir']
        self.editor = self.data['editor']
        self.viewer = self.data['viewer']
        self.terminal = self.data['terminal']
        self.notes_dir = self.data['notes_dir']
        self.root = self.data['root']
        # self.current_course = self.data['current_course']
        self.current_course = Path(self.data['current_course']).expanduser()
        self.master_file = self.data['master_file']
        self.projects_dir = self.data['projects_dir']
        self.assignments_dir = self.data['assignments_dir']
        self.assignments_folder = self.data['assignments_folder']
        self.assignments_pdf_folder = self.assignments_dir + '/pdf-files'
        self.yaml_extensions = ['.yaml', '.yml']
        self.assignments = []
        self.yaml_files = []
        self.pdf_files = []

        for file in os.listdir(self.assignments_folder):
            if os.path.isfile(os.path.join(self.assignments_folder, file)):
                if os.path.splitext(file)[1] == '.tex':
                    self.assignments.append(file)

        for file in os.listdir(self.assignments_folder):
            if os.path.isfile(os.path.join(self.assignments_folder, file)):
                if os.path.splitext(file)[1] in self.yaml_extensions:
                    self.yaml_files.append(file)

        for file in os.listdir(self.assignments_pdf_folder):
            if os.path.isfile(os.path.join(self.assignments_pdf_folder, file)):
                if os.path.splitext(file)[1] == '.pdf':
                    self.pdf_files.append(file)

        self.assignments = sorted(self.assignments)
        self.yaml_files = sorted(self.yaml_files)
        self.pdf_files = sorted(self.pdf_files)

        self.source_lectures_location = self.data['source_lessons_location']
        self.unit_info_name = self.data['unit_info_name']
        self.new_chap = self.data['new_chap']
        self.home = self.data['home']
        self.user = self.data['user']
        self.lecture_regex = r'lesson\{(.*?)\}\{(.*?)\}\{(.*)\}'
        self.rofi = Rofi()
        self.LESSON_RANGE_NUMBER = self.data['LESSON_RANGE_NUMBER']
        self.rofi_options = self.data['rofi_options']
        self.tex_types = self.data['tex_types']
        self.discourage_folders = self.data['discourage_folders']
        self.placeholder = self.get_placeholder()
        self.date_format = '%b %d %Y %a (%H:%M:%S)'

    def get_placeholder(self):
        """
        Gets the current location where I store my classes.

        Returns:
            placeholder (str): The current location where I store my classes.
        """

        placeholder = ''

        # Get the placeholder
        for i, s in enumerate(difflib.ndiff(self.notes_dir, self.root)):
            if s[0] == '+':
                placeholder += s[-1]

        # Remove the / from the beginning
        placeholder = placeholder[1:]

        # Return the placeholder
        return placeholder
