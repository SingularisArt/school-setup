#!/usr/bin/env python3

from glob import glob
import os

from natsort import natsorted

import RofiLessonManager.utils as utils
from config import (
    editor,
    my_assignments_latex_folder,
    my_assignments_pdf_folder,
    my_assignments_yaml_folder,
    pdf_viewer,
    terminal,
    terminal_commands,
)


class Assignment:
    def __init__(self, path):
        self.path = path

        self.name = os.path.basename(path)
        self.number = str(utils.filename_to_number(self.name))

        self.tex_file = f"{my_assignments_latex_folder}/week-{self.number}.tex"
        self.yaml_file = f"{my_assignments_yaml_folder}/week-{self.number}.yaml"
        self.pdf_file = f"{my_assignments_pdf_folder}/week-{self.number}.pdf"

        self.info = utils.load_data(self.yaml_file, "yaml")

        try:
            self.number, self.title, self.due_date, self.submit = self.get_info()
        except Exception:
            pass

        self.terminal = f"{terminal} {terminal_commands}"

    def parse_command(self, cmd):
        path = (
            self.tex_file
            if cmd == "edit_latex"
            else self.yaml_file
            if cmd == "edit_yaml"
            else self.pdf_file
            if cmd == "open_pdf"
            else None
        )

        full_command = (
            f"{terminal} {terminal_commands} '{editor} {path}'"
            if cmd != "open_pdf"
            else f"{pdf_viewer} {path}"
        )

        os.system(full_command)

    def get_info(self):
        due_date = self.info["due_date"]
        submit = self.info["submitted"]
        title = self.info["name"]
        number = self.name[5:-4]

        logo, due_date, late = utils.check_if_assignment_is_due(due_date, submit)

        if not submit:
            submit = "No"
            due_date += logo
        else:
            submit = "Yes"

        due_date = utils.generate_short_title(due_date, 28)

        return number, title, due_date, submit

    def __str__(self):
        return f"<Assignment: {self.number}. {self.name} {self.info['due_date']}>"

    def __eq__(self, other):
        return self.number == other.number

    def __len__(self, other):
        return self.number


class Assignments(list):
    def __init__(self):
        list.__init__(self, self.read_files())

        self.titles = [a.name for a in self]

    def read_files(self):
        files = natsorted(glob(f"{my_assignments_latex_folder}/*.tex"))

        return sorted((Assignment(f) for f in files), key=lambda a: a.number)
