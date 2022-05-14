#!/usr/bin/env python3

from glob import glob
import os
import yaml

from RofiLessonManager import Basis as Basis
from RofiLessonManager.classes.lectures import Lectures as Lectures


class Course(Basis):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

        if not os.path.exists(path):
            self.create_course()

        info = open('{}/info.yaml'.format(path))
        self.info = yaml.load(info, Loader=yaml.FullLoader)
        self._lectures = None

    def create_course(self):
        name = self.name.replace(' ', '_').replace(' ', '-').title()

        folders = ['lectures', 'assignments', 'figures', 'UltiSnips',
                   'assignments/latex-files', 'assignments/pdf-files']
        keys = ['title', 'short', 'url', 'calendar_name']
        values = [name, name[:3], 'https://', name]

        os.makedirs(self.path)
        for folder in folders:
            os.makedirs('{}/{}'.format(self.path, folder))

        info = open('{}/info.yaml'.format(self.path), 'w')

        for key, value in zip(keys, values):
            info.write('{}: {}\n'.format(key, value))

    @property
    def lectures(self):
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __str__(self):
        return '<Course: {}>'.format(self.name)

    def __eq__(self, other):
        if not other:
            return False
        return self.path == other.path


class Courses(Basis, list):
    """
    Inheritance:
        This class inherits from the RofiLessonManager.Basis class.
        This class inherits from the list class.

    This class will allow us to view all of our current classes and select
    which one we would like to change to.

    Attributes:
        classes:    A list of all of the classes that we are currently taking.
        titles:     A list of all of the titles of the classes.

    Methods:
        -----------------------------------------------------------------------
        | activate: This will activate the class that the user selects.       |
        |                                                                     |
        | Args:                                                               |
        |     index (int): The index of the class that the user selects.      |
        |                                                                     |
        | Returns:                                                            |
        |     None                                                            |
        -----------------------------------------------------------------------

        -----------------------------------------------------------------------
        | get_titles: This will return the titles of the classes.             |
        |                                                                     |
        | Returns:                                                            |
        |     titles (list): A list of all of the titles of the classes.      |
        -----------------------------------------------------------------------
    """

    def __init__(self):
        """
        This will initialize the class.
        """

        Basis.__init__(self)
        list.__init__(self, self.read_files())
        self.rofi_options.append(len(self))
        self.names = [c.info['title'] for c in self]
        self.rofi_names = []
        self.paths = [c.path for c in self]

        for name in self.names:
            self.rofi_names.append('<span color="blue">{}</span>'.format(name))

    def read_files(self):
        courses = glob('{}/*'.format(self.root))
        return sorted((Course(f) for f in courses), key=lambda c: c.name)

    @property
    def current(self):
        return Course(self.current_course.resolve()).name

    @current.setter
    def current(self, course):
        self.current_course.unlink()
        self.current_course.symlink_to(course.path)

    def __len__(self):
        return len(self.read_files())
