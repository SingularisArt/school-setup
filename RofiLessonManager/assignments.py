#!/usr/bin/env python3

import os

import RofiLessonManager.utils as utils
from config import (
    editor,
    my_assignments_latex_folder,
    my_assignments_pdf_folder,
    my_assignments_yaml_folder,
    online_assignments_folder,
    graded_assignments_folder,
    pdf_viewer,
    terminal,
    terminal_commands,
)


class Assignment:
    def __init__(self, root):
        self.root = root

        self.name = self.root.stem

        self.tex_file = my_assignments_latex_folder / f"{self.name}.tex"
        self.yaml_file = my_assignments_yaml_folder / f"{self.name}.yaml"
        self.pdf_file = my_assignments_pdf_folder / f"{self.name}.pdf"
        self.online_pdf_file = online_assignments_folder / f"{self.name}.pdf"
        self.graded_pdf_file = graded_assignments_folder / f"{self.name}.pdf"

        options = {}

        if self.tex_file.exists():
            options["View LaTeX File"] = "open_latex"
        if self.yaml_file.exists():
            options["View Yaml File"] = "open_yaml"
        if self.pdf_file.exists():
            options["View PDF File"] = "open_my_pdf"
        if self.online_pdf_file.exists():
            options["View Online PDF File"] = "open_online_pdf"
        if self.graded_pdf_file.exists():
            options["View Graded PDF File"] = "open_graded_pdf"

        self.options = options

        self.info = utils.load_data(self.yaml_file, "yaml")
        if not self.info:
            return

        try:
            self.title = self.info["title"]
            self.submit = self.info["submitted"]
            self.score = self.info["score"]
            self.number = self.info["number"]
            self.due_date, self.submit = self.get_due_date()
        except Exception:
            pass

        self.terminal = f"{terminal} {terminal_commands}"

    def parse_command(self, cmd):
        root = ""

        if cmd == "open_latex":
            root = self.tex_file
        elif cmd == "open_yaml":
            root = self.yaml_file
        elif cmd == "open_my_pdf":
            root = self.pdf_file
        elif cmd == "open_online_pdf":
            root = self.online_pdf_file
        elif cmd == "open_graded_pdf":
            root = self.graded_pdf_file

        self.edit(cmd, root)

    def edit(self, cmd, root):
        if "pdf" in cmd:
            os.system(f"{pdf_viewer} {root}")

            return

        listen_location = "/tmp/nvim.pipe"
        args = []

        if os.path.exists(listen_location):
            args = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            args = ["--listen", "/tmp/nvim.pipe"]

        args = " ".join(str(e) for e in args if e)

        os.system(
            f"{self.terminal} '{editor} {args} {root}'"
        )

    def get_due_date(self):
        due_date = self.info["due_date"]
        submit = self.info["submitted"]

        logo, due_date, _ = utils.check_if_assignment_is_due(
            due_date,
            submit,
        )

        if not submit:
            submit = "No"
            due_date += logo
        else:
            submit = "Yes"

        due_date = utils.generate_short_title(due_date, 28)

        return due_date, submit

    def __repr__(self):
        return f"<Assignment #{self.number}: {self.name}>"


class Assignments(list):
    def __init__(self):
        list.__init__(self, self.read_files())

        self.titles = [a.name for a in self]

    def read_files(self):
        latex_assignments = [
            Assignment(x) for x in my_assignments_latex_folder.glob("*.tex")
        ]

        return sorted(latex_assignments, key=lambda a: a.number)
