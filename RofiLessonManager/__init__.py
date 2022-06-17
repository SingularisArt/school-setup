#!/usr/bin/env python3

"""
Module RofiLessonManager -- Module for managing my school notes.

Class Assignment:
    - RofiLessonManager.Assignment

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific assignment.
    For example: Assignment(path-to-assignment). Then, it has all the
    information on that assignment from the assignment's yaml file,
    respectively.

    Args:
        - path (str): The path to the assignment.

    Attributes:
        - path (str): The path to the assignment.
        - name (str): The name of the assignment, which is the name of the
            file.
        - info (json): The information from the yaml file.

    Methods:
        - edit_latex: Opens the tex file of the assignment.

        - edit_yaml: Opens the yaml file of the assignment.

        - open_pdf: Opens the pdf file of the assignment.

        - new: Creates a new assignment.

        - __str__: Returns a string representation of the Assignment object.

            Returns:
                - str: A string representation of the Assignment object.

        - __eq__: Checks if two lectures are equal.

            Args:
                - other (Lecture): Lecture to compare with.

            Returns:
                - bool: True if equal, False otherwise.

Class Assignments:
    - RofiLessonManager.Assignments

    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class holds a list of all the assignments, which are located in the
    assignments folder, which can be modified from the config.yaml file. Each
    assignment is an instance from the
    RofiLessonManager.assignments.Assignment.

    Attributes:
        - names (list): A list of names for all the assignments.
        - rofi_names (list): A list of names for rofi to display.
        - second_options (list): The commands for Rofi to display for the user
            to select.

    Methods:
        - read_files: Reads all the files in the assignments folder and returns
            a list of Assignment objects.

            Returns:
                - assignments (list): A list of Assignment objects.

        - get_rofi_names: Returns a list of names for rofi to display.

            Returns:
                - options (list): A list of names for rofi to display.

        - __len__: Gets the number of assignments.

            Returns:
                - int: The number of assignments.

Class Basis:
    - RofiLessonManager.Basis

    All the classes within this module inherit from this class.
    It has all the basic information, which comes from the config.yaml file.

    Attributes:
        - data (json): The data from the config.yaml file, stored in json
            format.
        - calendar_id (str): The google calendar id.
        - code_dir (str): The location of the code directory.
        - editor (str): The text editor to use when opening lectures and
            assignments.
        - viewer (str): The pdf viewer to use when opening notes and
            assignments.
        - terminal (str): The terminal to use when opening the pdf viewer and
            editor.
        - notes_dir (str): The head location of the notes.
        - root (str): The location to the folder, which stores all my class
            notes for each term.
        - current_course (pathlib.Path): The location to the current course,
            which is a symlink to the root folder.
        - master_file (str): The location to the master.tex file.
        - projects_dir (str): The location to the projects folder.
        - assignments_dir (str): The location to the assignments folder, which
            is located in the current course.
        - assignments_latex_folder (str): The location to the folder where the
            LaTex source code is stored for the assignments.
        - assignments_pdf_folder (str): The location to the folder where the
            pdf files are stored for the assignments.
        - yaml_extensions (list): The extensions of the yaml files.
        - source_lectures_location (str): The location to the file where all
            the lectures are sourced.
        - home (str): The location to the home folder.
        - user (str): The name of the user.
        - lecture_regex (str): The regex, which is used to parse the needed
            information about each lecture.
        - rofi (rofi.Rofi): The rofi object, which is used to display the
            options.
        - LESSON_RANGE_NUMBER (int): A number, which is used in a for loop
            range to check if the lecture exists or not.
        - rofi_options (list): The arguments in a list, which are passed to the
            rofi object.
        - tex_types (list): The types of tex files.
        - discourage_folders (list): The folders to ignore.
        - placeholder (str): The placeholder, which is used when the user wants
            to replace the root folder.
        - date_format (str): The format of the date.

    Methods:
        - get_placeholder: Gets the current location to my classes, which will
            then be used as a placeholder for asking the user to enter a new
            location.

            Returns:
                - placeholder (str): The current location to my classes.

Class Commands:
    - RofiLessonManager.commands.Commands

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to source lectures. It asks the user the amount of
    lectures they would like to select: current, last two, all, or a range.

    Attributes:
        - options (list): Options for the user to select from.
        - index (int): The index of the selected options.
        - selected (str): The selected option.

    Methods:
        - get_last_two_lectures: This function will get the last two lectures.

            Returns:
                - last_lec (str): The last lecture.
                - sec_lec (str): The second last lecture. If the second last
                    lecture doesn't exist, it will return None.

        - source_current_lecture: This function will source the last lecture.

        - source_last_two_lectures: This function will source the last two
            lectures.

        - source_all_lectures: This function will source all of the lectures.

        - source_range: This function will source a range of lectures.

            Args:
                - lecture_range (str): The range of lectures to source
                    (ex: 1-5)

        - check_selection: This function will check the selection.

Class Lecture:
    - RofiLessonManager.Lecture

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific lecture. For
    example: Lecture(path-to-lecture). Then, it has all the information on that
    lecture from the lecture's yaml file, respectively.

    Attributes:
        - file_path (str): Path to the lecture file.
        - date_str (str): Date of the lecture as a string.
        - date (datetime.datetime): Date of the lecture as a datetime object.
        - week (int): Number of week when the lecture notes were written.
        - number (int): Number of the lecture.
        - title (str): Title of the lecture.
        - rofi_title (str): Title of the lecture as a fancy string for rofi.

    Args:
        - file_path (str): Path to the lecture file.

    Methods:
        - edit: Edits the lecture.

        - __str__: Returns the lecture as a string.

            Returns:
                - str: Lecture as a string.

        - __eq__: Checks if two lectures are equal.

            Args:
                - other (Lecture): Lecture to compare with.

            Returns:
                - bool: True if equal, False otherwise.

Class Lectures:
    - RofiLessonManager.Lectures

    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the List class.

    This class holds a list of all the lectures, which are located in the
    lectures folder, which can be modified from the config.yaml file. Each
    lecture is an instance from the RofiLessonManager.lectures.Lecture class.

    Attributes:
        - rofi_titles (list): List of titles for rofi.
        - titles (list): List of titles.

    Args:
        - file_path (str): Path to the lecture file.

    Methods:
        - read_files: Reads all the lecture files and returns a list of Lecture
            objects.

            Returns:
                - list: List of Lecture objects.

        - compile_master: Compiles the master file.

            Returns:
                - int: 0 if successful, 1 otherwise.

        - __len__: Gets the number of lectures.

            Returns:
                - int: Number of lectures.

Class Path:
    - RofiLessonManager.path.Path

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to change the current root path, which is the path to
    all the classes.

    Attributes:
        - theme (json): The theme, which will be passed to rofi. It has the
            placeholder in it.
        - path (str): The current root path.

    Methods:
        - get_path: Get the current path.

            Returns:
                - str: The current path.

        - replace_path: Replace the current path with the new path.

        - __str__: Return the string representation of the class.

            Returns:
                - str: The string representation of the class.

Class Project:
    - RofiLessonManager.projects.Project

    This class inherits from the RofiLessonManager.Basis class.

    This class is used to hold information about a specific project. For
    example: Project(path-to-project). Then, it has all the information on that
    project from the project's yaml file, respectively.

    Attributes:
        path (str): The path to the project.
        chapters (list): A list of chapters.
        info (dict): The project's info from the info.yaml file.
        info_file (str): The path to the info.yaml file.
        name (str): The name of the project.
        status (str): The status of the project.
        rofi_name (str): The name of the project for rofi.

    Args:
        - path (str): The path to the project.

    Methods:
        - get_status: Returns the status of the project.

            Returns:
                str: The status of the project.

        - open_pdf: Opens the project's pdf.

        - open_source: Opens the project's source folder.

        - open_notes: Opens the project's notes.

        - open_chapter: Opens a chapter.

            Args:
                - n (int): The chapter number.

        - get_chapters: Returns a list of chapters.

            Returns:
                - list: A list of chapters.

        - add_chapter: Adds a chapter to the project.

            Args:
                - n (int): The chapter number.

        - remove_chapter: Removes a chapter from the project.

        - source_chapter: Sources a chapter.

        - copy_pdf_to_drive: Copies the project's pdf.

            Args:
                - user (str): The user's name.

        - mark_project: Marks a project.

            Args:
                - status (str): The status of the project.

        - delete: Deletes the project.

        - __str__: Returns a string representation of the project.

            Returns:
                str: A string representation of the project.

Class Projects:
    - RofiLessonManager.projects.Projects

    This class inherits from the RofiLessonManager.Basis class.
    This class inherits from the list class.

    This class holds a list of all the projects, which are located in the
    projects folder, which can be modified from the config.yaml file. Each
    project is an instance from the RofiLessonManager.projects.Project.

    Attributes:
        - names (list): A list of project names.
        - rofi_names (list): A list of project names formatted for rofi.
        - commands (list): A list of commands for the user to choose from.

    Methods:
        - read_files: This function reads the files in the projects directory.

            Returns:
                - list: A list of Project objects for each project.

        - run_func_based_on_command: This function runs the function based on
            the command.

            Args:
                - command (str): The command.
                - index (int): The index of the project.


Function chapter:
    - RofiLessonManager.utils.chapter

    This function creates a new chapter.
    It then asks the user if they want to open the new chapter in the
    text editor.

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
        - rofi_options (list): The rofi options.

Function check_if_assignment_is_due:
    - RofiLessonManager.utils.check_if_assignment_is_due

    Checks if an assignment is due or not. If it is due, it returns either if
    it' LATE, or if it's due TODAY, TOMORROW, or it returns the number of days
    left until the assignment is due.

    Args:
        - assignment_due_date (str): The date the assignment is due.
        - assignment_submitted (str): The assignment submitted (True/False).

    Returns:
        - str: Returns either:
            - "X DAYS LATE" if the assignment is late.
            - "YESTERDAY" if the assignment was due yesterday.
            - "TODAY" if the assignment is due today.
            - "TOMORROW" if the assignment is due tomorrow.
            - "X DAYS LEFT" if the assignment is due in X days.

Function copy_pdf:
    - RofiLessonManager.utils.copy_pdf

    This function copies the pdf of the project to the flash drive

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
        - rofi_options (list): The options for the rofi menu.
        - user (str): The user who is running the script.
"""

from rofi import Rofi
from pathlib import Path

import RofiLessonManager.utils as utils


class Basis(object):
    """
    All the classes within this module inherit from this class.
    It has all the basic information, which comes from the config.yaml file.

    Attributes:
        - data (json): The data from the config.yaml file, stored in json
            format.
        - calendar_id (str): The google calendar id.
        - code_dir (str): The location of the code directory.
        - editor (str): The text editor to use when opening lectures and
            assignments.
        - viewer (str): The pdf viewer to use when opening notes and
            assignments.
        - terminal (str): The terminal to use when opening the pdf viewer and
            editor.
        - notes_dir (str): The head location of the notes.
        - root (str): The location to the folder, which stores all my class
            notes for each term.
        - current_course (pathlib.Path): The location to the current course,
            which is a symlink to the root folder.
        - master_file (str): The location to the master.tex file.
        - projects_dir (str): The location to the projects folder.
        - assignments_dir (str): The location to the assignments folder, which
            is located in the current course.
        - assignments_latex_folder (str): The location to the folder where the
            LaTex source code is stored for the assignments.
        - assignments_pdf_folder (str): The location to the folder where the
            pdf files are stored for the assignments.
        - yaml_extensions (list): The extensions of the yaml files.
        - source_lectures_location (str): The location to the file where all
            the lectures are sourced.
        - home (str): The location to the home folder.
        - user (str): The name of the user.
        - lecture_regex (str): The regex, which is used to parse the needed
            information about each lecture.
        - rofi (rofi.Rofi): The rofi object, which is used to display the
            options.
        - LESSON_RANGE_NUMBER (int): A number, which is used in a for loop
            range to check if the lecture exists or not.
        - rofi_options (list): The arguments in a list, which are passed to the
            rofi object.
        - tex_types (list): The types of tex files.
        - discourage_folders (list): The folders to ignore.
        - placeholder (str): The placeholder, which is used when the user wants
            to replace the root folder.
        - date_format (str): The format of the date.

    Methods:
        - get_placeholder: Gets the current location to my classes, which will
            then be used as a placeholder for asking the user to enter a new
            location.

            Returns:
                - placeholder (str): The current location to my classes.
    """

    def __init__(self):
        """ Initializes the class. """

        # Load the data from the config file
        self.data = utils.load_data()

        # Assign the data to the variables
        self.calendar_id = self.data['calendar_id']
        self.code_dir = self.data['code_dir']
        self.editor = self.data['editor']
        self.viewer = self.data['viewer']
        self.terminal = self.data['terminal']
        self.notes_dir = self.data['notes_dir']
        self.root = self.data['root']
        self.current_course = Path(self.data['current_course']).expanduser()
        self.master_file = self.data['master_file']
        self.projects_dir = self.data['projects_dir']
        self.assignments_dir = self.data['assignments_dir']
        self.assignments_latex_folder = self.data['assignments_latex_folder']
        self.assignments_yaml_folder = self.data['assignments_yaml_folder']
        self.assignments_pdf_folder = self.data['assignments_pdf_folder']
        self.yaml_extensions = ['.yaml', '.yml']
        self.source_lectures_location = self.data['source_lessons_location']
        self.home = self.data['home']
        self.user = self.data['user']
        self.lecture_regex = r'lesson\{(.*?)\}\{(.*?)\}\{(.*)\}'
        self.rofi = Rofi()
        self.LESSON_RANGE_NUMBER = self.data['LESSON_RANGE_NUMBER']
        self.rofi_options = self.data['rofi_options']
        self.tex_types = self.data['tex_types']
        self.discourage_folders = self.data['discourage_folders']
        self.placeholder = self.get_placeholder()
        self.date_format = '%b %d %Y %a (%H:%M:%S)'

    def get_placeholder(self):
        """
        Gets the current location to my classes, which will then be used as a
        placeholder for asking the user to enter a new location.

        Returns:
            - placeholder (str): The current location to my classes.
        """

        len_of_notes_dir = int(len(self.notes_dir)+1)

        return self.root[len_of_notes_dir:]
