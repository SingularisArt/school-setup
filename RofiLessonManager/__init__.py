#!/usr/bin/env python3

from pathlib import Path

import RofiLessonManager.utils as utils


class Basis(object):
    def __init__(self):
        """Initializes the class."""

        # Load the data from the config file
        self.data = utils.load_data()

        # Assign the data to the variables
        self.calendar_id = self.data["calendar_id"]
        self.base_url = self.data["base_url"]
        self.code_dir = self.data["code_dir"]
        self.editor = self.data["editor"]
        self.viewer = self.data["viewer"]
        self.terminal = self.data["terminal"]

        self.notes_dir = self.data["notes_dir"]
        self.root = self.data["root"]
        self.current_course = Path(self.data["current_course"]).expanduser()
        self.master_file = self.data["master_file"]
        self.source_lessons_location = self.data["source_lessons_location"]

        self.assignments_dir = self.data["assignments_dir"]
        self.graded_assignments_folder = self.data["graded_assignments_folder"]
        self.online_assignments_folder = self.data["online_assignments_folder"]
        self.my_assignments_latex_folder = self.data["my_assignments_latex_folder"]
        self.my_assignments_yaml_folder = self.data["my_assignments_yaml_folder"]
        self.my_assignments_pdf_folder = self.data["my_assignments_pdf_folder"]

        self.home = self.data["home"]
        self.user = self.data["user"]

        self.rofi_options = self.data["rofi_options"]
        self.tex_types = self.data["tex_types"]
        self.discourage_folders = self.data["discourage_folders"]
        self.folders = self.data["folders"]

        self.placeholder = self.get_placeholder()
        self.date_format = "%b %d %Y %a (%H:%M:%S)"
        self.lecture_regex = r"lesson\{(.*?)\}\{(.*?)\}\{(.*)\}"

    def get_placeholder(self):
        len_of_notes_dir = int(len(self.notes_dir) + 1)

        return self.root[len_of_notes_dir:]
