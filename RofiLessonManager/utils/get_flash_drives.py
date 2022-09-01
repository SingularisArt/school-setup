#!/usr/bin/env python3

"""
Function get_flash_drives:
    - RofiLessonManager.utils.get_flash_drives

    Get the flash drives that are connected to the laptop/pc/etc.

    Args:
        - r (object): Rofi object.
        - project_name (str): Name of the project.
        - user (str): Username.

    Returns:
        - drives (list): List of drives.
        - drives_names (list): List of drives with rofi design.
"""

import os

import RofiLessonManager.utils as utils


def get_flash_drives(user):
    """
    Get the flash drives that are connected to the laptop/pc/etc.

    Args:
        - user (str): Username.

    Returns:
        - drives (list): List of drives.
        - drives_names (list): List of drives with rofi design.
    """

    # List all flash drives
    try:
        drives = [x for x in os.listdir('/run/media/{}'.format(user))]
    except Exception:
        utils.rofi.error_message('No flash drives found!')
        exit(1)

    drives_with_style = []

    for drive in drives:
        new_drive = '<span color="brown">{}</span>'.format(drive)
        drives_with_style.append(new_drive)

    return drives, drives_with_style
