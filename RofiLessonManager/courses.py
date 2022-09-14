#!/usr/bin/env python3

from glob import glob
import os
import yaml

from config import (
    current_course,
    base_url,
    folders,
    root,
)

from RofiLessonManager.lectures import Lectures as Lectures
from RofiLessonManager import utils as utils


class Course:
    def __init__(self, path: str) -> None:
        """
        Initialize the Course class.

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
        name = self.name.replace(" ", "_").title()

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

        categories = ["Science", "Math", "Writing", "English"]
        types = ["In Person", "Online", "Remote"]

        topic = utils.rofi.select(
            "Select category of class",
            [c for c in categories],
            ["-auto-select", "-no-custom", "-lines", len(categories)],
        )[2]

        calendar_title = utils.folder_to_name(name)
        short = utils.rofi.input("Short version of course name")[1]
        start_date = utils.rofi.input("Start Date (08-31-22)")[1]
        end_date = utils.rofi.input("End Date (08-31-22)")[1]
        url = (
            base_url
            + "/"
            + utils.rofi.input("Enter last 5 digits of url to the course")[1]
        )
        type = utils.rofi.select(
            "Select type of class",
            [t for t in types],
            ["-auto-select", "-no-custom", "-lines", len(types)],
        )[2]

        values = [
            utils.folder_to_name(name),
            topic,
            calendar_title,
            short,
            start_date,
            end_date,
            url,
            type,
        ]

        os.makedirs(self.path)
        for folder in folders:
            os.makedirs("{}/{}".format(self.path, folder))

        info = open("{}/info.yaml".format(self.path), "w")

        for key, value in zip(keys, values):
            info.write("{}: {}\n".format(key, value))

    @property
    def lectures(self):
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __repr__(self):
        return "<Course: {}>".format(self.name)

    def __eq__(self, other):
        return self.path == str(other.resolve())


class Courses(list):
    def __init__(self):
        list.__init__(self, self.read_files())

        self.names = [c.info["title"] for c in self]
        self.paths = [c.path for c in self]

    def read_files(self):
        courses = glob("{}/*".format(root))
        return sorted((Course(f) for f in courses), key=lambda c: c.name)

    @property
    def current(self):
        return Course(current_course.resolve()).name

    @current.setter
    def current(self, course):
        current_course.unlink()
        current_course.symlink_to(course.path)
        current_course.lstat

    def __len__(self):
        return len(self.read_files())
