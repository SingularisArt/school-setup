"""
A simple gui interface for managing my school notes.
"""

from rofi import Rofi

import RofiLessonManager.utils as utils


class Basis(object):
    def __init__(self):
        """"""

        # Load the data from the config file
        self.data = utils.load_data()

        # Assign the data to the variables
        self.editor = self.data['editor']
        self.viewer = self.data['viewer']
        self.terminal = self.data['terminal']
        self.notes_dir = self.data['notes_dir']
        self.root = self.data['root']
        self.current_course = self.data['current_course']
        self.projects_dir = self.data['projects_dir']
        print(self.projects_dir)
        self.source_lessons_location = self.data['source_lessons_location']
        self.unit_info_name = self.data['unit_info_name']
        self.new_chap = self.data['new_chap']
        self.home = self.data['home']
        self.user = self.data['user']
        self.lesson_regex = r'\\lesson\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}'
        self.rofi = Rofi()
        self.LESSON_RANGE_NUMBER = self.data['LESSON_RANGE_NUMBER']
        self.rofi_options = self.data['rofi_options']
        self.tex_types = self.data['tex_types']
        self.discourage_folders = self.data['discourage_folders']
