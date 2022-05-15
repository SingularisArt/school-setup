#!/usr/bin/env python3

"""
Function open_source:
    - RofiLessonManager.utils.open_source

    This function opens the source of the project.

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
"""

import os


def open_source(project_name, projects_dir):
    """
    This function opens the source of the project.

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
    """

    # Replace spaces with - and make it lowercase
    project_folder_name = project_name.replace(' ', '-').lower()

    # Open source code
    os.system('xfce4-terminal -e "nvim {}/{}"'.format(projects_dir,
                                                      project_folder_name))
