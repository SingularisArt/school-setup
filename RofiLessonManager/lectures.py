#!/usr/bin/env python3

import os
from datetime import datetime
from glob import glob
import locale
import re
import subprocess
import yaml

from config import (
    current_course,
    master_file,
    editor,
    date_format,
    terminal,
    terminal_commands,
)

import RofiLessonManager.utils as utils


locale.setlocale(locale.LC_TIME, "en_US.utf8")

info = open("{}/info.yaml".format(current_course))
info = yaml.load(info, Loader=yaml.FullLoader)


class Lecture:
    """
    A class to represent a lecture.

    Attributes:
    -----------
        file_path (str): The path to the lecture file.
        date (datetime.strptime): The date of the lecture in a datetime obejct.
        week (int): The week of the lecture.
        number (int): The lecture number.
        title (str): The lecture title.

    Methods:
    --------
        edit() -> None: Edit the current lecture.
        new() -> None: Create a new lecture.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the Lecture class.

        Args:
        -----
            file_path (str): The path to the lecture file.
        """

        self.file_path: str = file_path

        # If the lecture file doesn't exist, create a new one.
        if not os.path.isfile(file_path):
            self.new()

        # Parse the lecture file, getting all the required information.
        with open(file_path) as f:
            for line in f:
                lecture_match = re.search(
                    r"lesson\{(.*?)\}\{(.*?)\}\{(.*)\}",
                    line,
                )
                if lecture_match:
                    break

        # Get the lecture date.
        date_str = lecture_match.group(2)

        # Format the date.
        date = datetime.strptime(date_str, date_format)

        # Get the start date of the course.
        # The reason I'm doing this is because we need to get the week of the
        # note was created. To do this, we need to start somewhere. For example
        # if the notes was taken on June 02, 2022, that would be week number
        # 23, which is correct, but not what I want. I want the week, starting
        # from the start date of the course. If we start from the start date of
        # the course, the week would be number 9, instead of 23.
        start_date_str = info["start_date"]

        # Format the date.
        start_date = datetime.strptime(start_date_str, date_format)

        # Get the week the notes were taken.
        week = int(utils.get_week(date)) - int(utils.get_week(start_date)) + 1

        # Get the title.
        title = lecture_match.group(3)

        self.date = date
        self.week = week
        self.number = utils.filename_to_number(os.path.basename(file_path))
        self.title = title

    def edit(self) -> None:
        """Edit the current lecture."""

        listen_location = "/tmp/nvim.pipe"
        args = []

        if os.path.exists(listen_location):
            args = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            args = ["--listen", "/tmp/nvim.pipe"]
        args = " ".join(str(e) for e in args if e)

        terminal_cmd = f"{terminal} {terminal_commands}"

        os.system(
            f"{terminal_cmd} '{editor} {args} "
            + f"{current_course}/lectures/lec-{self.number}.tex'"
        )

    def new(self) -> None:
        """Create a new lecture."""

        # Ask the user for the title of the lecture, via Rofi.
        title = utils.rofi.input("Title")

        # Get the current date.
        date = datetime.now().strftime(self.course_and_lecture_date_format)

        # Get the lecture number.
        number = utils.filename_to_number(os.path.basename(self.file_path))

        # Create the label.
        label = f"les_{number}:{title.lower().replace().replace(' ', '_')}"

        # Create the lecture template.
        template = [
            rf"\lesson{{{number}}}{{{date}}}{{{title}}}",
            rf"\label{{{label}}}",
            "",
            "",
            "",
            r"\newpage",
        ]

        # Open the lecture file.
        with open(self.file_path, "w") as f:
            # Write the template to the lecture file.
            f.write("\n".join(template))


class Lectures(list):
    def __init__(self) -> None:
        """Initialize the Lectures class."""

        # Initialize the list class with all the lectures.
        list.__init__(self, self.read_files())

        # Get all the lecture titles.
        self.titles = [lec.title for lec in self]

    def read_files(self) -> list:
        """
        Get all the lectures within the current course, sorted from greatest
        to least using the lecture number.

        Returns:
        --------
            list: All the lectures, sorted from greatest to least using the
                lecture number.
        """

        files = glob("{}/lectures/*.tex".format(current_course))
        return sorted((Lecture(f) for f in files), key=lambda l: l.number)

    def parse_lecture_spec(self, string: str) -> int:
        """
        Get the lecture number based on the command.

        Args:
        -----
            string (str): The string to parse.

        Returns:
        --------
            int: Based on the string, it returns the n'th lecture.

        Example:
        --------
            parse_range_string("last") -> self[-1].number
                (The last lecture)
            parse_range_string("prev") -> self[-1].number - 1
                (The second to last)
            parse_range_string(4) -> 4
        """

        all_numbers = [int(lecture.number) for lecture in self]

        if len(self) == 0:
            return 0

        if string.isdigit():
            return int(string)
        elif string == "last":
            return [all_numbers[-1]]
        elif string == "prev_last":
            return [all_numbers[-1] - 1, all_numbers[-1]]
        elif string == "all":
            return all_numbers
        elif string == "prev":
            return all_numbers[0:-1]

    def get_header_footer(self, filepath: str) -> tuple:
        r"""
        Get the header and footer of the master.tex file.

        Here's an example master.tex file:

        -----------------------------------------------------------------------
            \documentclass{report}

            \input{preamble.tex}

            \title{Pre-calculus 2}
            \author{Hashem A. Damrah}
            \date{\today}

            \begin{document}
              \maketitle
              \tableofcontents
              \mbox{}\newpage
              % start lectures
              \input{lectures/lec-01.tex}
              ...
              \input{lectures/lec-n.tex}
              % end lectures
            \end{document}
        -----------------------------------------------------------------------

        Here's the functions thought process NOTE: The order of the if
            statements are important.
        1. It checks if we're below the "end lecture" section.
            If we are, then it'll get everything underneath as the footer.
        2. It checks if we're above the "start lecture" section.
            If we are, then it'll get everything above as the header.

        I do this by creating a variable, part, and assigning it a value for
        each section.

        1. If we're above the "start lecture" section, then it's value is 0.
        2. If it's within the "start lecture" section, then it's value is 1.
        3. If it's after the "end lecture" section, then it's value is 2.

        Args:
        -----
            filepath (str): Path to the master.tex file.

        Returns:
        --------
            tuple:
                The header of the file.
                The footer of the file.
        """

        # 0 = The header of the file.
        # 1 = The start of the lectures section.
        # 2 = The footer of the file.
        part = 0

        header = ""
        footer = ""

        with filepath.open() as f:
            for line in f:
                # Check if we've reached the end of the file.
                # If we have, set part = 2.
                if "end lectures" in line:
                    part = 2

                # Check if we're on the header of the file.
                # If we have, set part = 2.
                if part == 0:
                    header += line

                # Check if we're at the end of the file.
                if part == 2:
                    footer += line

                # Check if we're at the start lectures section of the file.
                if "start lectures" in line:
                    part = 1

        return (header, footer)

    def parse_range_string(self, arg: str) -> list:
        """
        A range of numbers.

        Args:
        -----
            arg (str): A string range of numbers.

        Returns:
        --------
            list: A list of all the numbers from beginning to end.

        Example:
        --------
            m = len(letures)

            parse_range_string("4-7") -> [4,5,6,7]
            parse_range_string("4") -> [4]
            parse_range_string("a-n") -> [a1,a2,a3,...n]

            parse_range_string("last") -> the last lecture: [20]
            parse_range_string("prev_last") -> the last two lectures: [19, 20]
            parse_range_string("all") -> all the lectures: [1,2,3,...20]
            parse_range_string("prev") -> all lectures except the
                current one: [1,2,3,...19]
        """

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
        """
        Update the lectures within the master.tex file.

        Args:
        -----
            numbers (int): A list with all the numbers.

        Example:
        --------
            update_lectures_in_master([1,2,3,...n]) -> will add n number of
                lectures to the master.tex file.
        """

        header, footer = self.get_header_footer(master_file)
        body = "".join(
            r"  \input{lectures/" + utils.number_to_filename(number) + "}\n"
            for number in numbers
            if os.path.exists(
                f"{current_course}/lectures/{utils.number_to_filename(number)}"
            )
        )

        master_file.write_text(header + body + footer)

    def compile_master(self) -> None:
        """Compile the master.tex file."""

        result = subprocess.run(
            ["pdflatex", str(master_file)],
            cwd=str(current_course),
        )

        if result.returncode == 0:
            utils.rofi.msg("Compilation successful!", err=False)
        else:
            utils.rofi.msg("Compilation failed!", err=True)
