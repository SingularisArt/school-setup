import os

import yaml

from RofiLessonManager.notes import Notes as Notes
import config


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

        self._notes = None

    @property
    def notes(self):
        if not self._notes:
            self._notes = Notes(self)
        return self._notes

    def __eq__(self, other):
        if other is None:
            return False
        return self.root == other.root

    def __repr__(self):
        return f"<Course: {self.name}>"


class Courses(list):
    def __init__(self):
        list.__init__(self, self.read_files())

        self.names = [c.info["title"] for c in self]
        self.root = [c.root for c in self]

    def read_files(self):
        course_directories = [
            course for course in config.root.iterdir() if course.is_dir()
        ]
        courses = []

        for course in course_directories:
            course = Course(course)
            if course.exists:
                courses.append(course)

        return sorted(courses, key=lambda c: c.name)

    @property
    def current(self):
        return Course(config.current_course.resolve())

    @current.setter
    def current(self, course):
        config.current_course.unlink()
        config.current_course.symlink_to(course.root)
        config.current_course.lstat
        config.current_course_watch_file.write_text(
            f"{course.info['short']}\n",
        )
