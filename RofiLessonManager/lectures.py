#!/usr/bin/env python3

import os
from datetime import datetime
from glob import glob
import locale
import re
import subprocess
import yaml

import config

import RofiLessonManager.utils as utils


locale.setlocale(locale.LC_TIME, "en_US.utf8")

info: open = open("{}/info.yaml".format(config.current_course))
info: yaml.load = yaml.load(info, Loader=yaml.FullLoader)


class Lecture:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

        if not os.path.isfile(file_path):
            self.new()

        lecture_match = ""
        with open(file_path) as f:
            for line in f:
                lecture_match: re.search = re.search(
                    r"lecture\{(.*?)\}\{(.*)\}",
                    line,
                )
                if lecture_match:
                    break

        if lecture_match == "":
            return

        date_str: str = lecture_match.group(1)

        date: datetime.strptime = datetime.strptime(
            date_str,
            config.date_format,
        )

        start_date_str: str = info["start_date"]

        start_date: datetime.strptime = datetime.strptime(
            start_date_str,
            config.date_format,
        )

        week: int = (
            int(utils.get_week(date))
            - int(
                utils.get_week(start_date),
            )
            + 1
        )

        title: str = lecture_match.group(2)

        self.date: datetime.strptime = date
        self.week: int = week
        self.number: int = utils.filename_to_number(
            os.path.basename(file_path),
        )
        self.title: str = title

    def edit(self) -> None:
        listen_location: str = "/tmp/nvim.pipe"
        args: list = []

        if os.path.exists(listen_location):
            args: list = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            args: list = ["--listen", "/tmp/nvim.pipe"]

        args: str = " ".join(str(e) for e in args if e)

        terminal_cmd: str = f"{config.terminal} {config.terminal_commands}"

        os.system(
            f"{terminal_cmd} '{config.editor} {args} "
            + f"{config.current_course}/lectures/lec-{self.number}.tex'"
        )

    def new(self) -> None:
        title: title = utils.rofi.input("Title")

        date: datetime.now = datetime.now().strftime(
            self.course_and_lecture_date_format
        )

        number: int = utils.filename_to_number(
            os.path.basename(self.file_path),
        )

        label: str = f"les_{number}:{title.lower().replace(' ', '_')}"

        template: list[str] = [
            rf"\lecture{{{date}}}{{{title}}}",
            rf"\label{{{label}}}",
            "",
            "",
            "",
            r"\newpage",
        ]

        with open(self.file_path, "w") as f:
            f.write("\n".join(template))


class Lectures(list):
    def __init__(self) -> None:
        list.__init__(self, self.read_files())

    def read_files(self) -> list[Lecture]:
        files: list[str] = glob(f"{config.current_course}/lectures/*.tex")
        return sorted((Lecture(f) for f in files), key=lambda l: l.number)

    def parse_lecture_spec(self, string: str) -> int:
        all_numbers: list[int] = [int(lecture.number) for lecture in self]

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

    def get_header_footer(self, filepath: str) -> tuple:
        part: int = 0

        header: str = ""
        footer: str = ""

        with filepath.open() as f:
            for line in f:
                if "end lectures" in line:
                    part: int = 2

                if part == 0:
                    header += line

                if part == 2:
                    footer += line

                if "start lectures" in line:
                    part: str = 1

        return (header, footer)

    def parse_range_string(self, arg: str) -> list[int]:
        if "-" in arg:
            start, end = [
                self.parse_lecture_spec(bit)
                for bit in arg.split(
                    "-",
                )
            ]
            return list(range(start, end + 1))

        return self.parse_lecture_spec(arg)

    def update_lectures_in_master(self, numbers: list) -> None:
        header, footer = self.get_header_footer(config.master_file)

        body: str = "".join(
            r"  \input{lectures/" + utils.number_to_filename(number) + "}\n"
            for number in numbers
            if os.path.exists(
                f"{config.current_course}/lectures/"
                f"{utils.number_to_filename(number)}"
            )
        )

        config.master_file.write_text(header + body + footer)

    def compile_master(self) -> None:
        result: subprocess.run = subprocess.run(
            ["make"],
            cwd=str(config.current_course),
        )

        if result.returncode == 0:
            utils.rofi.msg("Compilation successful!", err=False)
        else:
            utils.rofi.msg("Compilation failed!", err=True)
