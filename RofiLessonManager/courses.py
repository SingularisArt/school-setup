#!/usr/bin/env python3

"""
This module contains the RofiLessonManager.Course and
RofiLessonManager.Courses classes.

- Class Course:
    - RofiLessonManager.courses.Course

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific Course. For
    example: Course(path-to-course). Then, it has all the information on that
    course from the course's yaml file, respectively.

    Args:
        - path: The path to the course.

    Attributes:
        - path: The path to the course.
        - name: The name of the course.
        - info: The info for the course, which comes from the info.yaml file
            located in the course folder.

    Methods:
        - create_course: Create a new course.

        - lectures: Gets a list of all lectures in the course.

            Returns:
                - list: List of Lectures.

        - __str__: This will return a string representation of the class.

            Returns:
                - str: String representation of the class.

        _ __eq__: This will compare two courses.

            Args:
                other (Course): The other course.

            Returns:
                - bool: True if the courses are equal, False otherwise.

- Class Courses:
    - RofiLessonManager.courses.Courses

    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class is used to hold information about all the courses.
    We can use this class to switch between courses.

    Attributes:
        - names: A list of all the names of the courses.
        - rofi_names: A list of all the names of the courses, formatted to
            be outputted by rofi.
        - paths: A list of all the paths of the courses.

    Methods:
        - read_files: This will read all the courses in the root folder.

            Returns:
                - list: List of Course objects, pointing to the courses.

        - current: Gets the current course.

            Returns:
                - Course: The current course.

        - current: Sets the current course.

            Args:
                - course (str): The name of the course.
"""


from glob import glob
import os
import yaml

from RofiLessonManager import Basis as Basis
from RofiLessonManager.lectures import Lectures as Lectures


class Course(Basis):
    """
    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific Course. For
    example: Course(path-to-course). Then, it has all the information on that
    course from the course's yaml file, respectively.

    Args:
        - path: The path to the course.

    Attributes:
        - path: The path to the course.
        - name: The name of the course.
        - info: The info for the course, which comes from the info.yaml file
            located in the course folder.

    Methods:
        - create_course: Create a new course.

        - lectures: Gets a list of all lectures in the course.

            Returns:
                - list: List of Lectures.

        - __str__: This will return a string representation of the class.

            Returns:
                - str: String representation of the class.

        _ __eq__: This will compare two courses.

            Args:
                other (Course): The other course.

            Returns:
                - bool: True if the courses are equal, False otherwise.
    """

    def __init__(self, path):
        """
        This will initialize the class.

        Args:
            path (str): The path to the course.
        """

        self.path = path
        self.name = os.path.basename(path)

        if not os.path.exists(path):
            self.create_course()

        info = open("{}/info.yaml".format(path))
        self.info = yaml.load(info, Loader=yaml.FullLoader)
        self._lectures = None

    def create_course(self):
        """Create a new course."""

        name = self.name.replace(" ", "_").replace(" ", "-").title()

        assignment_folders = ["image-files",
                              "latex-files", "pdf-files", "yaml-files"]
        folders = [
            "lectures",
            "assignments",
            "figures",
            "UltiSnips",
        ]

        [
            folders.append("assignments/{}".format(folder))
            for folder in assignment_folders
        ]

        keys = [
            "title",
            "topic",
            "calendar_title",
            "short",
            "start_date",
            "end_date",
            "url",
            "type",
        ]

        topic = ""
        calendar_title = name
        short = ""
        start_date = ""
        end_date = ""
        url = ""
        type = ""

        values = [
            name,
            topic,
            calendar_title,
            short,
            start_date,
            end_date,
            url,
            type,
        ]
        print(values)

        os.makedirs(self.path)
        for folder in folders:
            os.makedirs("{}/{}".format(self.path, folder))

        info = open("{}/info.yaml".format(self.path), "w")

        for key, value in zip(keys, values):
            info.write("{}: {}\n".format(key, value))

    @property
    def lectures(self):
        """
        Gets a list of all lectures in the course.

        Returns:
            - list: List of Lectures.
        """

        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __str__(self):
        """
        This will return a string representation of the class.

        Returns:
            - str: String representation of the class.
        """

        return "<Course: {}>".format(self.name)

    def __eq__(self, other):
        """
        This will compare two courses.

        Args:
            other (Course): The other course.

        Returns:
            - bool: True if the courses are equal, False otherwise.
        """

        if not other:
            return False
        return self.path == other.path


class Courses(Basis, list):
    """
    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class is used to hold information about all the courses.
    We can use this class to switch between courses.

    Attributes:
        - names: A list of all the names of the courses.
        - rofi_names: A list of all the names of the courses, formatted to
            be outputted by rofi.
        - paths: A list of all the paths of the courses.

    Methods:
        - read_files: This will read all the courses in the root folder.

            Returns:
                - list: List of Course objects, pointing to the courses.

        - current: Gets the current course.

            Returns:
                - Course: The current course.

        - current: Sets the current course.

            Args:
                - course (str): The name of the course.
    """

    def __init__(self):
        """This will initialize the class."""

        Basis.__init__(self)
        list.__init__(self, self.read_files())
        self.rofi_options.append(len(self))
        self.names = [c.info["title"] for c in self]
        self.rofi_names = []
        self.paths = [c.path for c in self]

        for name in self.names:
            self.rofi_names.append('<span color="blue">{}</span>'.format(name))

    def read_files(self):
        """
        This will read all the courses in the root folder.

        Returns:
            - list: List of Course objects, pointing to the courses.
        """

        courses = glob("{}/*".format(self.root))
        return sorted((Course(f) for f in courses), key=lambda c: c.name)

    @property
    def current(self):
        """
        Gets the current course.

        Returns:
            - Course: The current course.
        """

        return Course(self.current_course.resolve()).name

    @current.setter
    def current(self, course):
        """
        Sets the current course.

        Args:
            - course (str): The name of the course.
        """

        self.current_course.unlink()
        self.current_course.symlink_to(course.path)
        self.current_course.lstat

    def __len__(self):
        return len(self.read_files())
