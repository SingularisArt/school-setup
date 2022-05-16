#!/usr/bin/env python3
"""
This module contains the RofiLessonManager.Path class.

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
"""


from rofi import Rofi

from RofiLessonManager import Basis as Basis


class Path(Basis):
    """
    This class inherits from the RofiLessonManager.Basis class.

    This class is used to change the current root path, which is the path to
    all the classes.

    Attributes:
        - theme (json): The theme, which will be passed to rofi. It has the
            placeholder in it.
        - path (str): The current root path.

    Methods:
        - get_path: Ask the user for a new path.

            Returns:
                - str: The current path.

        - replace_path: Replace the current path with the new path.

        - __str__: Return the string representation of the class.

            Returns:
                - str: The string representation of the class.
    """

    def __init__(self):
        """ Initialize the class """

        Basis.__init__(self)

        self.theme = \
            'entry { placeholder: "' + self.placeholder + '"; ' + \
            'placeholder-color: grey; }'

    def get_path(self):
        """
        Ask the user for a new path.

        Returns:
            - str: The current path.
        """

        options = ['-theme-str', self.theme]

        r = Rofi()

        return r.text_entry('New Path', rofi_args=options)

    def replace_path(self, placeholder, path):
        """ Replace the current path with the new path. """

        file = open('{}/.config/zsh/exports.zsh'.format(self.home), 'r')
        replacement = ''

        for line in file:
            line = line.strip()
            changes = line.replace(placeholder, path)

            replacement += changes + '\n'

        file.close()

        fout = open('{}/.config/zsh/exports.zsh'.format(self.home), 'w')
        fout.write(replacement)
        fout.close()

    def __str__(self):
        """
        Return the string representation of the class.

        Returns:
            - str: The string representation of the class.
        """

        return '<Path: {}>'.format(self.path)
