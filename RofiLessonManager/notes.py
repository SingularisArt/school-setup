#!/usr/bin/env python3

import os
import re
from datetime import datetime

import config
import utils

info = utils.load_data(f"{config.current_course}/info.yaml", "yaml")
NOTES_TYPE = info["notes_type"]
LEC_OR_CHAP = "lec" if NOTES_TYPE == "lectures" else "chap"


class Note:
    def __init__(self, file_path):
        match = None

        with open(file_path) as f:
            for line in f:
                match = re.search(
                    r"(lecture|chapter)\{(.*?)\}\{(.*)\}",
                    line,
                )
                if match:
                    break

            if not match:
                return

        class_start_date_str = info["start_date"]
        date_str = match.group(2)
        date = datetime.strptime(date_str, config.date_format)
        class_start_date = datetime.strptime(
            class_start_date_str,
            config.date_format,
        )
        week = utils.get_week(date) - utils.get_week(class_start_date) + 1
        title = match.group(3)

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

        note_file = f"{NOTES_TYPE}/{LEC_OR_CHAP}-{self.number}.tex"

        cmd_part_1 = f"kitty --directory={config.current_course}"
        cmd_part_2 = f"{config.editor} {args} {note_file}"

        cmd = f"{cmd_part_1} {cmd_part_2}"
        os.system(cmd)


class Notes(list):
    def __init__(self, course):
        self.root = course.root
        self.master_file = self.root / "master.tex"
        self.path = self.root / NOTES_TYPE

        list.__init__(self, self.read_files())

    def read_files(self):
        files = self.root.glob(f"{NOTES_TYPE}/{LEC_OR_CHAP}-*.tex")

        return sorted((Note(f) for f in files), key=lambda note: note.number)

    def parse_note_spec(self, string):
        all_numbers = [int(note.number) for note in self]

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
                if "end notes" in line:
                    part = 2
                if part == 0:
                    header += line
                if part == 2:
                    footer += line
                if "start notes" in line:
                    part = 1

        return (header, footer)

    def parse_range_string(self, arg):
        if "-" in arg:
            try:
                start, end = map(int, arg.split("-"))
                return list(range(start, end + 1))
            except ValueError:
                return

        return self.parse_note_spec(arg)

    def update_notes_in_master(self, numbers):
        header, footer = self.get_header_footer(self.master_file)
        body = ""

        for number in numbers:
            file = utils.number_to_filename(number, LEC_OR_CHAP)
            if os.path.exists(f"{self.path}/{file}"):
                tab = " " * 2
                body += rf"{tab}\{LEC_OR_CHAP}{{{number}}}\n"

        self.master_file.write_text(header + body + footer)

    def compile_master(self):
        os.chdir(config.current_course)
        os.system("make")
