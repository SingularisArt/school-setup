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
        self.number = utils.filename2number(os.path.basename(path), "assignment")

        info_file_name = self.name.replace("tex", "yaml")
        info = open("{}/{}".format(self.assignments_yaml_folder, info_file_name))
        self.info_file = "{}/{}".format(self.assignments_latex_folder, info_file_name)
        self.info = yaml.load(info, Loader=yaml.FullLoader)

        self.number, self.title, self.due_date, self.submit = self.get_info()

    def parse_command(self, cmd):
        terminal = "xfce4-terminal -e"
        editor = self.editor if cmd != "open_pdf" else "zathura"

        tex_path = "{}/week-{}".format(self.assignments_latex_folder, self.number)
        yaml_path = "{}/week-{}".format(self.assignments_yaml_folder, self.number)
        pdf_path = "{}/week-{}".format(self.assignments_pdf_folder, self.number)

        tex_extension = '.tex'
        yaml_extension = '.yaml'
        pdf_extension = '.pdf'

        path = (
            tex_path + tex_extension
            if cmd == "edit_latex"
            else yaml_path + yaml_extension
            if cmd == "edit_yaml"
            else pdf_path + pdf_extension
            if cmd == "open_pdf"
            else None
        )

        full_command = (
            '{} "{} {}"'.format(terminal, editor, path)
            if cmd != "open_pdf"
            else "{} {}".format(editor, path)
        )
        os.system(full_command)

    def new(self):
        rofi = Rofi()
        title = rofi.text_entry("Title")
        due_date = rofi.date_entry("Due Date (ex: 05-30-22)", formats=["%m-%d-%y"])
        due_date = due_date.strftime("%m-%d-%y")
        _, _, submitted = utils.rofi("Submitted", ["Yes", "No"])

        yaml_file = "{}/week-{}.yaml".format(self.assignments_yaml_folder, self.number)

        with open(self.path, "x") as file:
            pass
        with open(yaml_file, "x") as file:
            pass

        with open(yaml_file, "w") as file:
            file.write("name: {}\n".format(title))
            file.write("due_date: {}\n".format(due_date))
            file.write("submitted: {}\n".format(submitted))

    def get_info(self):
        due_date = self.info["due_date"]
        submit = self.info["submitted"]
        title = utils.generate_short_title(self.info["name"], 22)
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
        return "<Assignment: {}. {} Due By: {}>".format(
            self.number, self.name, self.info["due_date"]
        )

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
        files = natsorted(glob("{}/*.tex".format(self.assignments_latex_folder)))

        return sorted((Assignment(f) for f in files), key=lambda a: a.number)

    def __len__(self):
        return len(self.read_files())
