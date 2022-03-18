import os
from pathlib import Path
from rofi import Rofi


class Configuration:
    """
    This is the basis class. It has all of the defaults that you need including
    helper functions, variables, etc. The helper functions are used to get the
    unit folders, classes, grades, etc.

    Methods:
    --------
    rofi: This is a wrapper function that helps you ask the user for input
    """

    def __init__(self):
        """
        Attributes:
        -----------
        editor: The editor to use
        viewer: The pdf viewer to use
        terminal: The terminal to use
        notes_dir: The base path to the notes directory
        root: The base directory for your classes
        current_course: Path to current course
        source_lessons_location: The path to the source-lessons.tex file
        r: An instance of the Rofi class
        text_types: A list of file types that are considered latex files
        new_chap: A boolean indicating if we need to create a new chapter
        discourage_folders: A list of folders that should not be considered
        home: The home directory
        user: The user name
        """

        self.editor = 'nvim'
        self.viewer = 'zathura'
        self.terminal = 'xfce4-terminal'
        self.notes_dir = Path('~/Documents/notes').expanduser()
        self.root = '{}/Grade-10/semester-2'.format(self.notes_dir)
        self.current_course = '{}/current-course'.format(self.notes_dir)
        self.source_lessons_location = '{}/source-lessons.tex'.format(
            self.current_course)

        self.r = Rofi()

        self.tex_types = ['.tex', '.latex']
        self.discourage_folders = ['images', 'assignments', 'figures',
                                   'projects', '.git', 'media',
                                   'current-course']
        self.new_chap = False

        self.unit_info_name = 'unit-info.tex'

        self.home = Path.home()
        self.user = os.getenv('USER')

        # This gets all of the folders within the current course
        # The folders_head stores the absolute path to each folder
        # The folders_tail stores the folder name
        self.folders_head, self.folders_tail = self.get_all_folders()

        # This gets all of the units within the current course
        # The units_head stores the absolute path to each unit
        # The units_tail stores the unit folder name
        self.units_head, self.units_tail = self._get_all_units()

        # This gets all of the lessons within the current course
        # The lessons_head stores the absolute path to each lesson
        # The lessons_tail stores the lesson file name
        self.lessons_head, self.lessons_tail, \
            self.all_lessons = self._get_all_lessons()

        # This gets the last two lessons, and the last unit number along with
        # its name
        self.last_lesson_head, \
            self.last_lesson_tail, \
            self.second_to_last_lesson_head, \
            self.second_to_last_lesson_tail, \
            self.last_unit_name, \
            self.last_unit_number = self._get_latest_lesson(
                self.lessons_head)

        self.lesson_regex = r'\\lesson\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}'
        self.LESSON_RANGE_NUMBER = 1000
        self.rofi_options = [
            '-lines', 5,
            '-markup-rows',
            '-kb-row-down', 'Down',
            '-kb-custom-1', 'Ctrl+n'
        ]

        self.classes = sorted(self._get_classes())

    def _update_selection(self, selection):
        self.selected = selection


config = Configuration()
