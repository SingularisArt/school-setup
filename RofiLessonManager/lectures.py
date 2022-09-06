#!/usr/bin/env python3

import os
from datetime import datetime
from glob import glob
import locale
import re
import subprocess
import yaml

from config import current_course, master_file, editor, date_format

import RofiLessonManager.utils as utils


locale.setlocale(locale.LC_TIME, "en_US.utf8")

info = open("{}/info.yaml".format(current_course))
info = yaml.load(info, Loader=yaml.FullLoader)


class Lecture:
    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.isfile(file_path):
            self.new()

        with open(file_path) as f:
            for line in f:
                lecture_match = re.search(
                    r"lesson\{(.*?)\}\{(.*?)\}\{(.*)\}", line)
                if lecture_match:
                    break

        date_str = lecture_match.group(2)
        date = datetime.strptime(date_str, date_format)
        start_date_str = info["start_date"]
        start_date = datetime.strptime(start_date_str, date_format)
        week = int(utils.get_week(date)) - int(utils.get_week(start_date)) + 1
        title = lecture_match.group(3)

        self.date_str = date_str
        self.date = date
        self.week = week
        self.number = utils.filename_to_number(os.path.basename(file_path))
        self.title = title

    def edit(self):
        listen_location = "/tmp/nvim.pipe"
        args = []

        if os.path.exists(listen_location):
            args = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            args = ["--listen", "/tmp/nvim.pipe"]
        args = " ".join(str(e) for e in args if e)

        os.system(
            f"xfce4-terminal -e '{editor} {args} "
            + f"{current_course}/lectures/lec-{self.number}.tex'"
        )

    def new(self):
        title = utils.rofi.input("Title")
        date = datetime.now().strftime(self.course_and_lecture_date_format)
        number = utils.filename_to_number(os.path.basename(self.file_path))
        label = "les_{}:{}".format(number, title.lower().replace(" ", "_"))

        template = [
            rf"\lesson{{{number}}}{{{date}}}{{{title}}}",
            rf"\label{{{label}}}",
            "",
            "",
            "",
            r"\newpage",
        ]

        with open(self.file_path, "w") as f:
            f.write("\n".join(template))

    def __str__(self):
        return "<Lecture: {} {} {}>".format(self.title, self.number, self.week)

    def __eq__(self, other):
        return self.number == other.number


class Lectures(list):
    def __init__(self):
        list.__init__(self, self.read_files())
        self.titles = [lec.title for lec in self]

    def read_files(self):
        files = glob("{}/lectures/*.tex".format(current_course))
        return sorted((Lecture(f) for f in files), key=lambda l: l.number)

    def parse_lecture_spec(self, string):
        if len(self) == 0:
            return 0

        if string.isdigit():
            return int(string)
        elif string == "last":
            return self[-1].number
        elif string == "prev":
            return self[-1].number - 1

    def parse_range_string(self, arg):
        all_numbers = [lecture.number for lecture in self]
        if "all" in arg:
            return all_numbers

        if "-" in arg:
            start, end = [self.parse_lecture_spec(
                bit) for bit in arg.split("-")]
            return list(range(start, end + 1))

        return [self.parse_lecture_spec(arg)]

    def update_lectures_in_master(self, r):
        body = ""
        for n in r:
            try:
                self[int(n) - 1].file_path
                body += r"\input{lectures/" + \
                    utils.number_to_filename(n) + "}\n"
            except IndexError:
                pass

        with open(self.source_lectures_location, "w") as f:
            f.write(body)

    def compile_master(self):
        result = subprocess.run(
            ["pdflatex", str(master_file)], cwd=str(current_course))

        if result.returncode == 0:
            utils.rofi.msg("Compilation successful", err=False)
        else:
            utils.rofi.msg("Compilation failed")

        return result.returncode

    def __len__(self):
        return len(self.read_files())
