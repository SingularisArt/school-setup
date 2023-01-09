#!/usr/bin/env python3

"""
This module provides an API for accessing the current course's assignments.

It provides a way of viewing the actual latex code, the yaml code, the final
pdf, the graded results, and the online assignment. All if they exist. If they
don't, it won't be shown.
"""

import os
from typing import Dict, List, Union

import notion_client
import yaml

import config
import utils

api_key = "secret_pV3mZ775Pdp2AmmduGNlAlfmPqQwz7Se2twgu8oHAZb"
database_id = "ea28de8e9cca4f62b4c4da3522869d03"

notion = notion_client.Client(auth=api_key)

new_record = {
    "Name": {"title": [{"text": {"content": "John Smith"}}]},
}

notion.pages.create(parent={"database_id": database_id}, properties=new_record)


class Assignment:
    """
    An Assignment represents a set of files for a single assignment, including
    LaTeX, YAML, and PDF files. It provides methods for viewing and editing
    these files.

    Attributes:
        root (os.PathLike): The root directory of the assignment files.
        name (str): The name of the assignment.
        tex_file (os.PathLike): The LaTeX file for the assignment.
        yaml_file (os.PathLike): The YAML file for the assignment.
        pdf_file (os.PathLike): The PDF file for the assignment.
        online_pdf_file (os.PathLike): The online PDF file for the assignment.
        graded_pdf_file (os.PathLike): The graded PDF file for the assignment.
        options (Dict[str, str]): The options for viewing the assignment files.
        info (Union[Dict, bool]): The information about the assignment.
        title (str): The title of the assignment.
        submit (bool): Whether the assignment has been submitted.
        score (int): The score received on the assignment.
        number (int): The number of the assignment.
        due_date (str): The due date of the assignment.
        terminal (str): The terminal command to use.

    Methods:
        parse_command(cmd: str): Parse a command and execute the corresponding action.
        edit(cmd: str, root: os.PathLike): Open the root file with the appropriate editor.
        get_due_date(): Get the due date of the assignment and whether it has been submitted.
    """

    def __init__(self, root):
        """
        Initialize the Assignment object with the root directory of the
        assignment files.

        Args:
            root (os.PathLike): The root directory of the assignment files.
        """

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
            self.submit: bool = self.info["submitted"]
            self.score: int = self.info["score"]
            self.number: int = self.info["number"]
            self.due_date, self.submit = self.get_due_date()
        except Exception:
            pass

        self.terminal: str = f"{config.terminal} {config.terminal_commands}"

    def parse_command(self, cmd: str) -> None:
        """
        Parse the command and determine which file to open.

        Args:
            cmd (str): The command to parse.
        """

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
        """
        Edit the specified file using the specified command.

        Args:
            cmd (str): The command to use.
            root (os.PathLike): The file to edit.
        """

        if "pdf" in cmd:
            os.system(f"{config.pdf_viewer} {root}")
            return

        listen_location: str = "/tmp/nvim.pipe"
        args: List[Union[str, int]] = []

        if os.path.exists(listen_location):
            args = ["--server", "/tmp/nvim.pipe", "--remote"]
        elif not os.path.exists(listen_location):
            args = ["--listen", "/tmp/nvim.pipe"]

        args = " ".join(str(e) for e in args if e)

        os.system(f"{self.terminal} '{config.editor} {args} {root}'")

    def get_due_date(self):
        """
        Get the due date and submission status of the assignment.

        Returns:
            Tuple[str, str]: The due date and submission of the assignment.
        """

        due_date: str = self.info["due_date"]
        submit: str = self.info["submitted"]

        logo, due_date = utils.check_if_assignment_is_due(due_date, submit)

        if not submit:
            submit = "No"
            due_date += logo
        else:
            submit = "Yes"

        due_date = utils.generate_short_title(due_date, 28)

        return due_date, submit

    def create_new_assignment(self) -> None:
        if self.tex_file.exists() or self.yaml_file.exists():
            return

        name: str = input("Enter the name of the assignment: ")
        number: str = input("Enter the number of the assignment: ")
        due_date: str = input("Enter the due date of the assignment: ")
        course: str = ""

        grade: str = "NA"
        progress: str = "not started"

        data: Dict[str, str] = {
            "title": name,
            "number": number,
            "due_date": due_date,
            "grade": grade,
            "progress": progress,
        }

        with self.yaml_file.open("w") as f:
            yaml.dump(data, f)

        with self.tex_file.open("w") as f:
            f.write("")

        self.add_assignment_to_notion(name, course, due_date, grade, progress)

    def add_assignment_to_notion(
        self,
        name: str,
        course: str,
        due_date: str,
        grade: str,
        progress: str,
        page_id: Union[str, None] = None,
    ) -> None:
        """
        Add the information of a new assignment to a Notion page.

        Args:
            name (str): The name of the assignment.
            course (str): The course the assignment is for.
            due_date (str): The due date of the assignment.
            grade (str): The grade received on the assignment.
            progress (str): The progress made on the assignment.
            page_id (Union[str, None], optional): The ID of the Notion page to add the information to.
                If no ID is provided, the information will be added to the default page set in the
                configuration file. Defaults to None.
        """

        if page_id is None:
            page_id = config.notion_page_id

        new_page = {
            "title": {
                "title": {
                    "text": {
                        "content": name,
                    }
                }
            },
            "course": {
                "rich_text": [
                    {
                        "text": {
                            "content": course,
                        }
                    }
                ]
            },
            "due_date": {
                "date": {
                    "start": due_date,
                }
            },
            "grade": {
                "rich_text": [
                    {
                        "text": {
                            "content": grade,
                        }
                    }
                ]
            },
            "progress": {
                "rich_text": [
                    {
                        "text": {
                            "content": progress,
                        }
                    }
                ]
            },
        }
        notion.pages.create(
            parent={"database_id": database_id},
            properties=new_page,
        )

    def __repr__(self):
        return f"<Assignment #{self.number}: {self.name}>"


class Assignments(list):
    """
    A class representing a list of Assignment objects.

    Attributes:
        titles (List[str]): A list of the names of the assignments.

    Methods:
        read_files(): Read the assignment files from the
            `my_assignments_yaml_folder` and return a list of Assignment
            objects.
    """

    def __init__(self) -> None:
        """
        Initialize the Assignments object as a list of Assignment objects.
        """

        super().__init__(self.read_files())

        self.titles: List[str] = [a.name for a in self]

    def read_files(self) -> List[Assignment]:
        """
        Read the assignment files from the `my_assignments_yaml_folder` and
        return a list of Assignment objects.

        Returns:
            List[Assignment]: The list of Assignment objects.
        """

        latex_assignments: List[Assignment] = []
        for x in config.my_assignments_yaml_folder.glob("*.yaml"):
            x = Assignment(x)

            if x.info:
                latex_assignments.append(x)

        return sorted(latex_assignments, key=lambda a: a.number)
