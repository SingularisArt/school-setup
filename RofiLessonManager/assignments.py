#!/usr/bin/env python3

import os

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
    def __init__(self, root):
        self.root = root

        self.name = self.root.stem
        self.number = str(utils.filename_to_number(self.name))

        self.tex_file = my_assignments_latex_folder / f"week-{self.number}.tex"
        self.yaml_file = my_assignments_yaml_folder / f"week-{self.number}.yaml"
        self.pdf_file = my_assignments_pdf_folder / f"week-{self.number}.pdf"

        options = []
        if self.tex_file.exists():
            options.append("View LaTeX File")
        if self.yaml_file.exists():
            options.append("View Yaml File")
        if self.pdf_file.exists():
            options.append("View PDF File")

        self.options = options

        self.info = utils.load_data(self.yaml_file, "yaml")

        try:
            self.title, self.due_date, self.submit = self.get_info()
        except Exception:
            pass

        self.terminal = f"{terminal} {terminal_commands}"

    def parse_command(self, cmd):
        root = (
            self.tex_file
            if cmd == "edit_latex"
            else self.yaml_file
            if cmd == "edit_yaml"
            else self.pdf_file
            if cmd == "open_pdf"
            else None
        )

        full_command = (
            f"{terminal} {terminal_commands} '{editor} {root}'"
            if cmd != "open_pdf"
            else f"{pdf_viewer} {root}"
        )

        os.system(full_command)

    def get_info(self):
        due_date = self.info["due_date"]
        submit = self.info["submitted"]
        title = self.info["name"]

        logo, due_date, late = utils.check_if_assignment_is_due(due_date, submit)

        if not submit:
            submit = "No"
            due_date += logo
        else:
            submit = "Yes"

        due_date = utils.generate_short_title(due_date, 28)

        return title, due_date, submit

    def __repr__(self):
        return f"<Assignment: {self.number}. {self.name} {self.info['due_date']}>"


class Assignments(list):
    def __init__(self):
        list.__init__(self, self.read_files())

        self.titles = [a.name for a in self]

    def read_files(self):
        latex_assignments = [Assignment(x) for x in my_assignments_latex_folder.glob("*.tex")]

        return sorted(latex_assignments, key=lambda a: a.number)
