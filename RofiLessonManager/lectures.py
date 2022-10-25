#!/usr/bin/env python3

from datetime import datetime
import locale
import os
import re
import subprocess

import yaml

import RofiLessonManager.utils as utils
import config


locale.setlocale(locale.LC_TIME, "en_US.utf8")

info = open("{}/info.yaml".format(config.current_course))
info = yaml.load(info, Loader=yaml.FullLoader)


class Lecture:
    def __init__(self, file_path):
        self.file_path = file_path

        lecture_match = ""

        with open(file_path) as f:
            for line in f:
                lecture_match = re.search(
                    r"lecture\{(.*?)\}\{(.*)\}",
                    line,
                )
                if lecture_match:
                    break

        date_str = lecture_match.group(1)
        date = datetime.strptime(date_str, config.date_format)
        week = utils.get_week(date)

        title = lecture_match.group(2)

        self.file_path = file_path
        self.date = date
        self.week = week
        self.number = utils.filename_to_number(file_path.stem)
        self.title = title

    def edit(self):
        listen_location = "/tmp/nvim.pipe"
        args = []

        if os.path.exists(listen_location):
            args = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            args = ["--listen", "/tmp/nvim.pipe"]

        args = " ".join(str(e) for e in args if e)

        terminal_cmd = f"{config.terminal} {config.terminal_commands}"

        os.system(
            f"{terminal_cmd} '{config.editor} {args} "
            + f"{config.current_course}/lectures/lec-{self.number}.tex'"
        )


class Lectures(list):
    def __init__(self, course):
        self.root = course.root
        self.master_file = self.root / "master.tex"

        list.__init__(self, self.read_files())

    def read_files(self):
        files = self.root.glob("lectures/lec-*.tex")
        return sorted((Lecture(f) for f in files), key=lambda l: l.number)

    def parse_lecture_spec(self, string):
        all_numbers = [int(lecture.number) for lecture in self]

        if len(self) == 0:
            return 0

        if string.isdigit():
            return [int(string)]
        elif string == "last":
            return [all_numbers[-1]]
        elif string == "prev_last":
            return [all_numbers[-1] - 1, all_numbers[-1]]
        elif string == "all":
            return all_numbers
        elif string == "prev":
            return all_numbers[0:-1]

    def get_header_footer(self, lec_path):
        part = 0

        header = ""
        footer = ""

        with lec_path.open() as f:
            for line in f:
                if "end lectures" in line:
                    part = 2

                if part == 0:
                    header += line

                if part == 2:
                    footer += line

                if "start lectures" in line:
                    part = 1

        return (header, footer)

    def parse_range_string(self, arg):
        if "-" in arg:
            start, end = [
                self.parse_lecture_spec(bit)
                for bit in arg.split(
                    "-",
                )
            ]
            return list(range(start, end + 1))

        return self.parse_lecture_spec(arg)

    def update_lectures_in_master(self, numbers):
        header, footer = self.get_header_footer(self.master_file)

        body = "".join(
            r"  \input{lectures/" + utils.number_to_filename(number) + "}\n"
            for number in numbers
            if os.path.exists(
                f"{config.current_course}/lectures/"
                f"{utils.number_to_filename(number)}"
            )
        )

        self.master_file.write_text(header + body + footer)

    def compile_master(self):
        result = subprocess.run(
            ["make"],
            cwd=str(config.current_course),
        )

        if result.returncode == 0:
            utils.rofi.msg("Compilation successful!", err=False)
        else:
            utils.rofi.msg("Compilation failed!", err=True)
