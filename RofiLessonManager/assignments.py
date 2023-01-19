#!/usr/bin/env python3

import os
from typing import Dict, List, Union

import yaml

import config
import utils


class Assignment:
    def __init__(self, root):
        self.root: os.PathLike = root

        self.name: str = self.root.stem

        self.tex_file: os.PathLike = (
            config.my_assignments_latex_folder / f"{self.name}.tex"
        )
        self.yaml_file: os.PathLike = (
            config.my_assignments_yaml_folder / f"{self.name}.yaml"
        )
        self.pdf_file: os.PathLike = (
            config.my_assignments_pdf_folder / f"{self.name}.pdf"
        )
        self.online_pdf_file: os.PathLike = (
            config.online_assignments_folder / f"{self.name}.pdf"
        )
        self.graded_pdf_file: os.PathLike = (
            config.graded_assignments_folder / f"{self.name}.pdf"
        )

        options: Dict[str, str] = {}

        if self.tex_file.exists():
            options["View LaTeX File"] = "open_latex"
        if self.yaml_file.exists():
            options["View YAML File"] = "open_yaml"
        if self.pdf_file.exists():
            options["View PDF File"] = "open_my_pdf"
        if self.online_pdf_file.exists():
            options["View Online PDF File"] = "open_online_pdf"
        if self.graded_pdf_file.exists():
            options["View Graded PDF File"] = "open_graded_pdf"

        self.options: Dict[str, str] = options
        self.progress_options: List[str] = [
            "not started",
            "pending",
            "done",
        ]

        self.info: Dict[str, Union[str, bool, int]] = utils.load_data(
            self.yaml_file, "yaml"
        )
        if not self.info:
            self.info = False

        try:
            self.title: str = self.info["title"]
            self.due_date, self.days_left = self.get_due_date()
            self.grade: int = self.info["grade"]
            self.status: bool = self.info["status"]
            self.number: int = self.info["number"]
        except Exception as e:
            print(e)
            # pass

        self.terminal: str = f"{config.terminal} {config.terminal_commands}"

    def parse_command(self, cmd):
        root: os.PathLike = ""

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

    def edit(self, cmd: str, root: os.PathLike) -> None:
        due_date: str = self.info["due_date"]
        status: str = self.info["status"]
        submit = False if status != "done" else True

        days_left, due_date = utils.check_if_assignment_is_due(
            due_date,
            submit,
        )

        due_date = utils.generate_short_title(due_date, 28)

        return due_date, days_left

    def __repr__(self):
        return f"<Assignment #{self.number}: {self.name}>"


class Assignments(list):
    def __init__(self) -> None:
        super().__init__(self.read_files())

        self.titles: List[str] = [a.name for a in self]

    def read_files(self) -> List[Assignment]:
        latex_assignments: List[Assignment] = []
        for x in config.my_assignments_yaml_folder.glob("*.yaml"):
            x = Assignment(x)

            if x.info:
                latex_assignments.append(x)

        return sorted(latex_assignments, key=lambda a: a.number)
