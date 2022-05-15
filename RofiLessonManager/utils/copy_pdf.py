#!/usr/bin/env python3

"""
Function copy_pdf:
    - RofiLessonManager.utils.copy_pdf

    This function copies the pdf of the project to the flash drive

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
        - rofi_options (list): The options for the rofi menu.
        - user (str): The user who is running the script.
"""

import os
from rofi import Rofi

from RofiLessonManager.utils.get_flash_drives import get_flash_drives
from RofiLessonManager.utils.rofi import rofi


def copy_pdf(project_name, projects_dir, rofi_options, user):
    """
    This function copies the pdf of the project to the flash drive

    Args:
        - project_name (str): The name of the project.
        - projects_dir (str): The path to the projects directory.
        - rofi_options (list): The options for the rofi menu.
        - user (str): The user who is running the script.
    """

    # Get all flash drives
    rofi_output = Rofi()
    drives, drives_with_style = get_flash_drives(rofi_output, project_name, user)

    # Ask the user which drive to use via rofi
    _, index, _ = rofi('Select command',
                       drives_with_style,
                       rofi_options)

    project_name = project_name.replace(' ', '-').lower()

    master_path = '{}/{}/master.pdf'.format(projects_dir,
                                            project_name)
    drive_path = '/run/media/{}/{}/'.format(user, drives[index])

    try:
        os.system('cp -r {} {}'.format(master_path, drive_path))
    except Exception:
        rofi.error('Couldn\'t move master.pdf to {}'.format(drive_path))
        exit(1)

    rofi_output.status('Copied master.pdf to {}'.format(drive_path))
