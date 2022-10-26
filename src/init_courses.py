#!/usr/bin/env python3

from os import symlink
from shutil import copy2

from RofiLessonManager.courses import Courses as Courses
from config import files, folders, templates_dir


def symlink_file(src, dst):
    try:
        symlink(src, dst)
    except FileExistsError:
        return
    except FileNotFoundError:
        return


def copy_file(src, dst):
    try:
        copy2(src, dst)
    except FileExistsError:
        return
    except FileNotFoundError:
        return


def main():
    for course in Courses():
        lectures = course.lectures

        # Create all the folders.
        for folder in folders:
            (lectures.root / folder).mkdir(exist_ok=True)

        # Grab all the files.
        for file in files:
            key = files[file]
            if key == "symlink":
                symlink_file(templates_dir / file, course.root / file)
            elif key == "copy":
                copy_file(templates_dir / file, course.root / file)
