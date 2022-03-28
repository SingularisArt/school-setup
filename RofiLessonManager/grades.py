#!/usr/bin/env python3

"""
rofi-grades.py - A python script that parses my school website and displays
                 the grades for the current semester.
"""

from bs4 import BeautifulSoup
from rofi import Rofi
import requests
import operator
import sys
import os
import re


class Grades:
    def __init__(self):
        """ This is the constructor of the Grades class """

        self.home = os.path.expanduser("~")
        sys.path.insert(0, "{}/Singularis/local/scripts/school/".format(
            self.home))

        from cookie import headers
        from config import CURRENT_COURSE, SOURCE_LESSONS_LOCATION
        from config import EDITOR, VIEWER, TERMINAL, NOTES_DIR, ROOT
        from config import tex_types, new_chap, discourage_folders, rofi

        self.headers = headers

        self.tex_types = tex_types
        self.new_chap = new_chap
        self.discourage_folders = discourage_folders

        self.rofi = rofi
        self.r = Rofi()

        self.editor = EDITOR
        self.viewer = VIEWER
        self.terminal = TERMINAL
        self.notes_dir = NOTES_DIR
        self.root = ROOT
        self.current_course = CURRENT_COURSE
        self.source_lesson_location = SOURCE_LESSONS_LOCATION

        self.src, self.soup = self.get_src()

        (
            self.classes,
            self.grades,
            self.classes_and_grades,
        ) = self.get_classes_and_grades()

    def get_src(self):
        """
        This function gets the source code of the grades page

        Returns:
            src (str):              The source code of the grades page
            soup (BeautifulSoup):   The soup object of the source code
        """

        result = requests.get('https://bakercharters.instructure.com/grades',
                              headers=self.headers)

        src = result.content
        soup = BeautifulSoup(src, "lxml")

        return src, soup

    def get_classes_and_grades(self):
        """ This function gets the classes and grades from the source code

        Returns:
            classes (list):             The list of classes
            grades (list):              The list of grades
            classes_and_grades (dict):  The list of classes and grades
        """

        links = self.soup.find_all("a")
        classes = []

        for link in links:
            try:
                link_id = re.search(
                    r"/courses/([0-9]+)/grades/([0-9]+)", link.attrs["href"]
                )
                link_id = link_id.group(1)
                classes.append(link.text)
            except Exception:
                pass

        grades = self.soup.find_all("td", {"class": "percent"})
        cleaned_grades = []

        for grade in grades:
            grade = (
                grade.text.replace("        ", "").replace("\n", "").replace(
                    "    ", "")
            )
            cleaned_grades.append(grade)

        grades = cleaned_grades

        classes_and_grades = {}

        for key in classes:
            for grade in grades:
                classes_and_grades[key] = grade
                grades.remove(grade)
                break

        classes_and_grades = sorted(
            classes_and_grades.items(), key=operator.itemgetter(0)
        )

        return classes, grades, classes_and_grades

    def output_info(self):
        """ This function outputs the information of the grades """

        information = ''
        for class_and_grade in self.classes_and_grades:
            for x, class_or_grade in enumerate(class_and_grade):
                try:
                    information += "{} - {}\n".format(class_or_grade,
                                                      class_and_grade[x + 1])
                except Exception:
                    pass

        self.r.error(information)


grades = Grades()
grades.output_info()
