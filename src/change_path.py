#!/usr/bin/env python3

"""
This file will use the RofiLessonManager.path module to change the current root
path to the one specified by the user, via rofi.
"""

import os

import RofiLessonManager.utils as utils
from RofiLessonManager.path import Path as Path


def main():
    """
    This function will run the RofiLessonManager.path module to replace the
    current root path.
    """

    change_path = Path()
    new_path = change_path.get_path()

    if new_path == '':
        return

    if os.path.exists(change_path.notes_dir + '/' + new_path):
        change_path.replace_path(change_path.placeholder, new_path)
        os.system('{}/init-config.sh'.format(change_path.code_dir))
    else:
        utils.error_message('The path you entered does not exist.')
        main()


if __name__ == "__main__":
    main()
