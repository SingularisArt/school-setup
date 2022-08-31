#!/usr/bin/env python3

from glob import glob
import os
import yaml
from rofi import Rofi

from RofiLessonManager import Basis as Basis
from RofiLessonManager.lectures import Lectures as Lectures
from RofiLessonManager import utils as utils


class Course(Basis):
    def __init__(self, path):
        Basis.__init__(self)

        self.path = path
        self.name = os.path.basename(path)

        if not os.path.exists(path):
            self.create_course()

        info = open("{}/info.yaml".format(path))
        self.info = yaml.load(info, Loader=yaml.FullLoader)
        self._lectures = None

    def create_course(self):
        rofi = Rofi()

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

        _, _, topic = utils.rofi(
            "Select category of class",
            [c for c in categories],
            ["-auto-select", "-no-custom", "-lines", len(categories)],
        )

        calendar_title = utils.folder2name(name)
        short = rofi.text_entry(
            "Short version of course name ({})".format(utils.folder2name(name))
        )
        start_date = rofi.text_entry("Start Date (08-31-22)")
        end_date = rofi.text_entry("End Date (08-31-22)")
        url = self.base_url + rofi.text_entry(
            "Enter last 5 digits of url to the course"
        )
        _, _, type = utils.rofi(
            "Select type of class",
            [t for t in types],
            ["-auto-select", "-no-custom", "-lines", len(types)],
        )

        values = [
            utils.folder2name(name),
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
        for folder in self.folders:
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
        if not other:
            return False
        return self.path == other.path


class Courses(Basis, list):
    def __init__(self):
        Basis.__init__(self)
        list.__init__(self, self.read_files())

        self.names = [c.info["title"] for c in self]
        self.rofi_names = []
        self.paths = [c.path for c in self]

        for name in self.names:
            self.rofi_names.append('<span color="blue">{}</span>'.format(name))

    def read_files(self):
        courses = glob("{}/*".format(self.root))
        return sorted((Course(f) for f in courses), key=lambda c: c.name)

    @property
    def current(self):
        return Course(self.current_course.resolve()).name

    @current.setter
    def current(self, course):
        self.current_course.unlink()
        self.current_course.symlink_to(course.path)
        self.current_course.lstat

    def __len__(self):
        return len(self.read_files())
