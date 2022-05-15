#!/usr/bin/env python3

"""
Function get_classes:
    - RofiLessonManager.utils.get_classes

    Get all classes in the root of your notes.

    Args:
        - root (str): The root of your notes.

    Returns:
        - list: A list of all classes in the root of your notes.
"""

import os


def get_classes(root):
    """
    Get all classes in the root of your notes.

    Args:
        - root (str): The root of your notes.

    Returns:
        - list: A list of all classes in the root of your notes.
    """

    return sorted([os.path.join(root, o)
                   for o in os.listdir(root)
                   if os.path.isdir(os.path.join(root, o))])
