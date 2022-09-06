#!/usr/bin/env python3

from rofi import Rofi
from glob import glob
from natsort import natsorted
import os
import yaml

from RofiLessonManager import Basis as Basis
import RofiLessonManager.utils as utils


class Assignment(Basis):
    def __init__(self, path):
        Basis.__init__(self)

        self.path = path

        if not os.path.exists(self.path):
            self.new()

        self.name = os.path.basename(path)
        self.number = utils.filename_to_number(os.path.basename(path))

        self.tex_file = f"{self.my_assignments_latex_folder}/week-{self.number}.tex"
        self.yaml_file = f"{self.my_assignments_yaml_folder}/week-{self.number}.yaml"
        self.pdf_file = f"{self.my_assignments_pdf_folder}/week-{self.number}.pdf"

        self.info = utils.load_data(self.yaml_file, "yaml")

        try:
            self.number, self.title, self.due_date, self.submit = self.get_info()
        except Exception:
            pass

    def parse_command(self, cmd):
        terminal = f"{self.terminal} {self.terminal_command}"
        # xfce4-terminal -e
        editor = self.editor if cmd != "open_pdf" else self.pdf_viewer

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
            f"{terminal} '{editor} {path}'" if cmd != "open_pdf" else f"{editor} {path}"
        )

        os.system(full_command)

    def new(self):
        rofi = Rofi()
        title = rofi.text_entry("Title")
        due_date = rofi.date_entry(
            "Due Date (ex: 05-30-22)", formats=["%m-%d-%y"])
        due_date = due_date.strftime("%m-%d-%y")
        _, _, submitted = utils.rofi.select("Submitted", ["Yes", "No"])

        open(self.path, "x")
        open(self.yaml_file, "x")

        with open(self.yaml_file, "w") as file:
            file.write(f"name: {title}\n")
            file.write(f"due_date: {due_date}\n")
            file.write(f"submitted: {submitted}\n")

    def get_info(self):
        due_date = self.info["due_date"]
        submit = self.info["submitted"]
        title = self.info["name"]
        number = self.name[5:-4]

        logo, due_date, late = utils.check_if_assignment_is_due(
            due_date, submit)

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


class Assignments(Basis, list):
    def __init__(self):
        Basis.__init__(self)

        list.__init__(self, self.read_files())

        self.titles = [a.name for a in self]

    def read_files(self):
        files = natsorted(glob(f"{self.my_assignments_latex_folder}/*.tex"))

        return sorted((Assignment(f) for f in files), key=lambda a: a.number)
