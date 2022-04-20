"""
A simple gui interface for managing my school notes.
"""

import difflib
import os
from rofi import Rofi

import RofiLessonManager.utils as utils


class Basis(object):
    def __init__(self):
        """"""

        # Load the data from the config file
        self.data = utils.load_data()

        # Assign the data to the variables
        self.code_dir = self.data['code_dir']
        self.editor = self.data['editor']
        self.viewer = self.data['viewer']
        self.terminal = self.data['terminal']
        self.notes_dir = self.data['notes_dir']
        self.root = self.data['root']
        self.current_course = self.data['current_course']
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

    def get_placeholder(self):
        placeholder = ''

        # Get the placeholder
        for i, s in enumerate(difflib.ndiff(self.notes_dir, self.root)):
            if s[0] == '+':
                placeholder += s[-1]

        # Remove the / from the beginning
        placeholder = placeholder[1:]

        # Return the placeholder
        return placeholder
