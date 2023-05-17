#!/usr/bin/env python3

import os

import config
import utils


class Assignment:
    def __init__(self, root):
        self.root = root

        self.name = self.root.stem

        self.tex_file_path = (
            config.my_assignments_latex_folder / f"{self.name}.tex"
        )
        self.yaml_file_path = (
            config.my_assignments_yaml_folder / f"{self.name}.yaml"
        )
        self.pdf_file_path = (
            config.my_assignments_pdf_folder / f"{self.name}.pdf"
        )
        self.online_pdf_file_path = (
            config.online_assignments_folder / f"{self.name}.pdf"
        )
        self.graded_pdf_file_path = (
            config.graded_assignments_folder / f"{self.name}.pdf"
        )

        self.options = {}

        if self.tex_file_path.exists():
            self.options["View LaTeX File"] = "open_latex"
        if self.yaml_file_path.exists():
            self.options["View YAML File"] = "open_yaml"
        if self.pdf_file_path.exists():
            self.options["View PDF File"] = "open_my_pdf"
        if self.online_pdf_file_path.exists():
            self.options["View Online PDF File"] = "open_online_pdf"
        if self.graded_pdf_file_path.exists():
            self.options["View Graded PDF File"] = "open_graded_pdf"

        self.progress_options = [
            "not started",
            "pending",
            "done",
        ]

        self.commands = {
            "latex": "open_latex",
            "yaml": "open_yaml",
            "pdf": "open_my_pdf",
            "online": "open_online_pdf",
            "graded": "open_graded_pdf",
        }

        self.info = utils.load_data(self.yaml_file_path, "yaml")
        if not self.info:
            self.info = False

        try:
            self.title = self.info["title"]
            self.grade = self.info["grade"]
            self.submitted = self.info["submitted"]
            self.number = self.info["number"]
            self.due_date, self.days_left = self.get_due_date()
        except Exception:
            pass

    def get_due_date(self):
        due_date = self.info["due_date"]

        days_left, due_date = utils.check_if_assignment_is_due(
            due_date,
            self.submitted,
        )

        due_date = utils.generate_short_title(due_date, 28)

        return due_date, days_left

    def parse_command(self, cmd):
        if cmd == self.commands["latex"]:
            return self.edit(cmd, self.tex_file_path)
        elif cmd == self.commands["yaml"]:
            return self.edit(cmd, self.yaml_file_path)
        elif cmd == self.commands["pdf"]:
            return self.edit(cmd, self.pdf_file_path)
        elif cmd == self.commands["online"]:
            return self.edit(cmd, self.online_pdf_file_path)
        elif cmd == self.commands["graded"]:
            return self.edit(cmd, self.graded_pdf_file_path)

    def edit(self, cmd, root):
        if "pdf" in cmd:
            os.system(f"{config.pdf_viewer} {root}")

            return

        listen_location = "/tmp/nvim.pipe"
        arguments = []

        if os.path.exists(listen_location):
            arguments = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            arguments = ["--listen", "/tmp/nvim.pipe"]

        arguments = " ".join(str(e) for e in arguments if e)

        os.system(
            f"{config.terminal} {config.editor} {arguments} {root}"
        )

    def __repr__(self):
        return f"<Assignment #{self.number}: {self.name}>"


class Assignments(list):
    def __init__(self):
        super().__init__(self.read_files())

        self.titles = [assignment.name for assignment in self]

    def read_files(self):
        latex_assignments = []
        for yaml_file in config.my_assignments_yaml_folder.glob("*.yaml"):
            yaml_file = Assignment(yaml_file)

            if yaml_file.info:
                latex_assignments.append(yaml_file)

        return sorted(latex_assignments, key=lambda assignment: assignment.number)
