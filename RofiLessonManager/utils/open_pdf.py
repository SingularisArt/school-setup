#!/usr/bin/env python3

"""
Function open_pdf:
    - RofiLessonManager.utils.open_pdf

    This function opens the pdf of the project.

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
"""

import os


def open_pdf(project_name, projects_dir):
    """
    This function opens the pdf of the project.

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
    """

    # Replace spaces with - and make it lowercase
    project_folder_name = project_name.replace(' ', '-').lower()

    # Open the pdf
    os.system('zathura {}/{}/master.pdf'.format(projects_dir,
                                                project_folder_name))
