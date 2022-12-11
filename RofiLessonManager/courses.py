#!/usr/bin/env python3

import os

import yaml

from RofiLessonManager.lectures import Lectures as Lectures
from config import current_course
from config import current_course_watch_file, root


class Course:
    def __init__(self, root):
        self.root = root
        self.name = self.root.stem

        if not os.path.exists(root):
            self.create_course()

        if not os.path.exists(self.root / "info.yaml"):
            self.exists = False
            return

        info = open(self.root / "info.yaml")
        self.info = yaml.load(info, Loader=yaml.FullLoader)
        self.exists = True

        self._lectures = None

    @property
    def lectures(self):
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __repr__(self):
        return f"<Course: {self.name}>"

    def __eq__(self, other):
        return self.root == other.root


class Courses(list):
    def __init__(self):
        list.__init__(self, self.read_files())

        self.names = [c.info["title"] for c in self]
        self.root = [c.root for c in self]

    def read_files(self):
        course_directories = [x for x in root.iterdir() if x.is_dir()]
        _courses = []

        for course in course_directories:
            course = Course(course)
            if course.exists:
                _courses.append(course)

        return sorted(_courses, key=lambda c: c.name)

    @property
    def current(self):
        return Course(current_course.resolve())

    @current.setter
    def current(self, course):
        current_course.unlink()
        current_course.symlink_to(course.root)
        current_course.lstat
        current_course_watch_file.write_text(
            f"{course.info['short']}\n",
        )
