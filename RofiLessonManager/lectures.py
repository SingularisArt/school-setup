#!/usr/bin/env python3

import os
import re
import subprocess
from datetime import datetime

import yaml

import utils
import config

info = open("{}/info.yaml".format(config.current_course))
info = yaml.load(info, Loader=yaml.FullLoader)


class Lecture:
    """
    Represents a single lecture.

    Attributes:
        file_path: The file path of the lecture.
        date: The date of the lecture as a datetime object.
        week: The week number of the lecture.
        number: The number of the lecture.
        title: The title of the lecture.
        terminal: The terminal command to open the editor.
    """

    def __init__(self, file_path):
        """
        Initializes a new instance of the Lecture class.

        Args:
            file_path: The file path of the lecture.
        """

        lecture_match = ""

        # Read the file and search for the lecture metadata
        with open(file_path) as f:
            for line in f:
                lecture_match = re.search(
                    r"lecture(\[.*\])?\{(.*?)\}\{(.*)\}",
                    line,
                )
                if lecture_match:
                    break

            # Return if no match was found
            if not lecture_match:
                return

        # Load the class start date from the info YAML file
        with open("{}/info.yaml".format(config.current_course)) as info:
            class_start_date_str = yaml.load(info, Loader=yaml.FullLoader)["start_date"]

        # Convert the lecture date string to a datetime object
        date_str = lecture_match.group(2)
        date = datetime.strptime(date_str, config.date_format)
        # Convert the class start date string to a datetime object
        class_start_date = datetime.strptime(class_start_date_str, config.date_format)
        # Calculate the week number for the lecture
        week = utils.get_week(date) - utils.get_week(class_start_date) + 1

        # Extract the title from the match
        title = lecture_match.group(3)

        # Set the instance attributes
        self.file_path = file_path
        self.date = date
        self.week = week
        self.number = utils.filename_to_number(file_path.stem)
        self.title = title

        # Build the terminal command string to open the editor
        self.terminal = f"{config.terminal} {config.terminal_commands}"

    def edit(self):
        """
        Opens the lecture file using the specified text editor.

        If the specified editor is `nvim`, this function uses the `--server`
        and `--remote` arguments to send a command to a running instance of
        `nvim` if one exists, otherwise it creates a new instance and uses
        the `--listen` argument to listen for commands from subsequent
        invocations.
        """

        listen_location = "/tmp/nvim.pipe"
        args = []

        if os.path.exists(listen_location):
            # Send command to running instance of nvim
            args = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            # Start new instance of nvim and listen for commands
            args = ["--listen", "/tmp/nvim.pipe"]

        # Join arguments into a single string
        args = " ".join(str(e) for e in args if e)

        # Build the terminal command string
        terminal_cmd = f"{config.terminal} {config.terminal_commands}"

        # Open the lecture file using the specified text editor
        os.system(
            f"{terminal_cmd} '{config.editor} {config.args} {config.current_course}/lectures/lec-{self.number}.tex'"
        )


class Lectures(list):
    """
    A class representing a list of lectures for a course.

    This class is derived from the built-in `list` class and adds several
    additional methods for interacting with the list of lectures.

    Args:
        course (Course): The course object that the lectures belong to.

    Attributes:
        root (Path): The root directory of the course.
        master_file (Path): The path to the `master.tex` file for the course.
    """

    def __init__(self, course):
        self.root = course.root
        self.master_file = self.root / "master.tex"

        # Initialize the list with the lectures read from files
        list.__init__(self, self.read_files())

    def read_files(self):
        """
        Read the `.tex` files for each lecture in the course.

        Returns:
            list: A list of `Lecture` objects, sorted by their number.
        """

        files = self.root.glob("lectures/lec-*.tex")
        return sorted((Lecture(f) for f in files), key=lambda lec: lec.number)

    def parse_lecture_spec(self, string):
        """
        Parse a string specifying a range of lectures.

        This method can handle a variety of inputs, including a single number,
        the string "last" for the last lecture, the string "prev_last" for
        the last two lectures, the string "all" for all lectures, and the
        string "prev" for all lectures except the last.

        Args:
            string (str): The string specifying the range of lectures.

        Returns:
            list: A list of integers representing the lecture numbers.
        """

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
        """
        Get the header and footer of a `.tex` file.

        Args:
            lec_path (Path): The path to the `.tex` file.

        Returns:
            tuple: A tuple containing the header and footer as strings.
        """

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
            start = int(arg.split("-")[0])
            end = int(arg.split("-")[1])
            return list(range(start, end + 1))

        return self.parse_lecture_spec(arg)

    def update_lectures_in_master(self, numbers):
        header, footer = self.get_header_footer(self.master_file)

        body = "".join(
            r"  \lec{" + str(number) + "}\n"
            for number in numbers
            if os.path.exists(
                f"{config.current_course}/lectures/{utils.number_to_filename(number)}"
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
