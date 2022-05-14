#!/usr/bin/env python3

from rofi import Rofi

from RofiLessonManager import Basis as Basis


class ChangePath(Basis):
    """
    Inheritance:
        This class inherits from the RofiLessonManager.Basis class.

    This class allows the user to change the path to the root directory.

    Attributes:
        theme: The theme for the placeholder.
        path:  The current path, which will be used as the placeholder.

    Methods:
        -----------------------------------------------------------------------
        | get_path: Get the current path.                                     |
        |                                                                     |
        | Returns:                                                            |
        |     str: The current path.                                          |
        -----------------------------------------------------------------------

        -----------------------------------------------------------------------
        | replace_path: Replace the current path with the new path.           |
        -----------------------------------------------------------------------
    """

    def __init__(self):
        """
        Initialize the class
        """

        Basis.__init__(self)

        self.theme = \
            'entry { placeholder: "' + self.placeholder + '"; ' + \
            'placeholder-color: grey; }'

        self.path = self.get_path()
        self.replace_path(self.placeholder, self.path)

    def get_path(self):
        """
        Get the current path.

        Returns:
            str: The current path.
        """

        options = ['-theme-str', self.theme]
        r = Rofi(rofi_args=options)

        return r.text_entry('New Path')

    def replace_path(self, placeholder, path):
        """
        Replace the current path with the new path.
        """

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
