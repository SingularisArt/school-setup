# !/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: Jan 23 2022 Sun (00:45:44)
This class is used to create a rofi menu for the user to select a command
to execute.
"""

import re
from rofi import Rofi
import os
import sys

from config import Configuration


class NewLesson(Configuration):
    def __init__(self):
        """ This function initializes the class """

        self.home = os.path.expanduser('~')
        sys.path.insert(0, '{}/Singularis/local/scripts/school/'.format(
                            self.home))

        from config import tex_types, new_chap, discourage_folders
        from config import EDITOR, VIEWER, TERMINAL, NOTES_DIR, ROOT
        from config import CURRENT_COURSE, SOURCE_LESSONS_LOCATION

        self.tex_types = tex_types
        self.new_chap = new_chap
        self.discourage_folders = discourage_folders

        self.unit_info_name = 'unit-info.tex'

        self.rofi = Rofi()

        self.editor = EDITOR
        self.viewer = VIEWER
        self.terminal = TERMINAL
        self.notes_dir = NOTES_DIR
        self.root = ROOT
        self.current_course = CURRENT_COURSE
        self.source_lesson_location = SOURCE_LESSONS_LOCATION
        self.date, self.time = self.get_current_date()
        self.file_path, self.lesson_name, self.module_name, \
            self.unit_number, self.lesson_number = self.get_info()

        self.write_info()

    def get_info(self):
        """ This function gets the information from the user """

        module_name = ''

        file_path = self.rofi.text_entry('File name EX: (unit-1/lesson-19)')

        # Perform the regex to get the unit number and lesson number
        lesson_match = re.search(r'unit-(\d+)/(lesson-\d+)\.tex', file_path)

        # Check if the file isn't a LaTeX file
        if file_path[-4:] not in self.tex_types:
            tex_types = ', '.join(self.tex_types)
            self.rofi.error(
                'Sorry! The file must a LaTeX file ({})'.format(tex_types))
            self.get_info()

        if os.path.exists('{}/{}'.format(self.current_course, file_path)):
            self.rofi.error(
                'Sorry! The file already exists in the current course')
            yn = self.rofi.text_entry('Would you like to overwrite it? [y/n]')

            if yn != 'y':
                self.get_info()

        lesson_name = self.rofi.text_entry('Lesson name')

        # If the lesson is the first lesson, then we ask for the module name
        try:
            if lesson_match.group(2) == 'lesson-1':
                module_name = self.rofi.text_entry('Enter module name')
        except Exception:
            pass

        try:
            os.makedirs('{}/unit-{}'.format(self.current_course,
                                            lesson_match.group(1)))
        except Exception:
            pass

        return file_path, lesson_name, module_name, lesson_match.group(1), \
            lesson_match.group(2)

    def write_info(self):
        """ This function writes the information to the file """

        lesson_info = '\\lesson{' + self.lesson_number[7:] + '}' + \
            '{' + self.date + ' ' + self.time + '}' + \
            '{' + self.lesson_name + '}' + \
            '{Unit ' + self.unit_number + '}\n\n\n\n' + \
            '\\newpage'

        # Write the information to the file that the user wants to create
        with open('{}/{}'.format(self.current_course, self.file_path),
                  'w') as new_file:
            new_file.write(lesson_info)

        if self.module_name:
            self.write_module_info()

    def write_module_info(self):
        """ This function writes the module information to the file """

        module_info = '\\chapter{' + self.module_name + '}'
        section_info = '\\section{Unit ' + self.unit_number + '}'

        with open('{}/unit-{}/{}'.format(self.current_course, self.unit_number,
                                         self.unit_info_name),
                  'w') as new_file:
            new_file.write(module_info)
            new_file.write('\n\n')
            new_file.write(section_info)


new = NewLesson()

os.system('~/Singularis/local/scripts/school/rofi-commands.py')

yn = new.rofi.text_entry('Would you like to open the new lesson? [y/n]')

if yn == 'y':
    os.system('{} -e "{} {}"'.format(new.terminal, new.editor,
                                     '{}/{}'.format(new.current_course,
                                                    new.file_path)))
